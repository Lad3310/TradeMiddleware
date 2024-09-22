import logging
import pandas as pd
from lxml import etree
import traceback
import io
import time
import random
import requests
from requests.exceptions import RequestException, Timeout

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_trade_data(df):
    errors = []
    
    required_columns = ['trade_id', 'symbol', 'quantity', 'price']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    for col in required_columns:
        if col in df.columns and df[col].isnull().any():
            errors.append(f"Column '{col}' contains empty values")
    
    if 'quantity' in df.columns:
        if not pd.api.types.is_numeric_dtype(df['quantity']):
            errors.append("'quantity' column must contain numeric values")
        elif (df['quantity'] <= 0).any():
            errors.append("'quantity' must be greater than 0")

    if 'price' in df.columns:
        if not pd.api.types.is_numeric_dtype(df['price']):
            errors.append("'price' column must contain numeric values")
        elif (df['price'] <= 0).any():
            errors.append("'price' must be greater than 0")
    
    return errors

def process_trade_data(df):
    logging.info(f"Processing trade data with {len(df)} rows")
    
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    errors = validate_trade_data(df)
    if errors:
        for error in errors:
            logging.error(error)
        raise ValueError("Data validation failed. Check logs for details.")
    
    df['quantity'] = df['quantity'].astype(int)
    df['price'] = df['price'].astype(float)
    
    df['timestamp'] = pd.Timestamp.now()
    
    logging.info("Trade data processed successfully")
    return df

def exponential_backoff(attempt, base_delay=1, max_delay=60):
    delay = min(base_delay * (2 ** attempt), max_delay)
    jitter = random.uniform(0, 0.1 * delay)
    return delay + jitter

def simulate_external_api_call(trade_data, max_retries=5, timeout=30, chunk_size=10):
    def process_chunk(chunk):
        time.sleep(random.uniform(0.1, 0.5))
        try:
            # Simulate an API call with a potential timeout
            response = requests.get('https://api.example.com/process', params={'data': chunk.to_json()}, timeout=timeout)
            response.raise_for_status()
            return True
        except (RequestException, Timeout) as e:
            logging.warning(f"API call failed: {str(e)}")
            raise

    total_rows = len(trade_data)
    processed_rows = 0
    failed_rows = 0
    total_attempts = 0
    total_delay = 0

    for i in range(0, total_rows, chunk_size):
        chunk = trade_data[i:i+chunk_size]
        chunk_processed = False
        attempts = 0

        while not chunk_processed and attempts < max_retries:
            attempts += 1
            total_attempts += 1
            try:
                success = process_chunk(chunk)
                if success:
                    processed_rows += len(chunk)
                    chunk_processed = True
                    logging.info(f"Processed chunk {i//chunk_size + 1}/{(total_rows + chunk_size - 1)//chunk_size}")
                else:
                    raise RequestException("Chunk processing failed")
            except (RequestException, Timeout) as e:
                delay = exponential_backoff(attempts - 1)
                total_delay += delay
                logging.warning(f"Attempt {attempts} failed for chunk {i//chunk_size + 1}. Retrying in {delay:.2f} seconds. Error: {str(e)}")
                time.sleep(delay)

        if not chunk_processed:
            failed_rows += len(chunk)
            logging.error(f"Failed to process chunk {i//chunk_size + 1} after {max_retries} attempts")

    success_rate = processed_rows / total_rows
    status = 'success' if success_rate > 0.8 else 'partial_success' if success_rate > 0 else 'failure'

    return {
        'status': status,
        'success_rate': success_rate,
        'processed_rows': processed_rows,
        'failed_rows': failed_rows,
        'total_attempts': total_attempts,
        'total_delay': total_delay,
        'message': f"Processed {processed_rows}/{total_rows} rows. {failed_rows} rows failed."
    }

def process_xml_data(xml_content):
    logging.info("Starting XML data processing")
    try:
        logging.debug(f"Raw XML content (first 200 chars): {xml_content[:200].decode('utf-8')}")
        
        root = etree.fromstring(xml_content)
        logging.info(f"XML root element: {root.tag}")
        
        data = []
        for trade in root.findall('Trade'):
            logging.debug(f"Processing trade element: {etree.tostring(trade, encoding='unicode')}")
            try:
                trade_data = {
                    'trade_id': trade.findtext('TradeID'),
                    'symbol': trade.findtext('Security'),
                    'quantity': trade.findtext('Quantity'),
                    'price': trade.findtext('Price')
                }
                
                missing_fields = [field for field, value in trade_data.items() if value is None]
                if missing_fields:
                    logging.warning(f"Trade is missing required fields: {', '.join(missing_fields)}")
                    logging.warning(f"Skipping trade: {etree.tostring(trade, encoding='unicode')}")
                    continue
                
                try:
                    trade_data['quantity'] = int(trade_data['quantity'])
                    trade_data['price'] = float(trade_data['price'])
                except ValueError as e:
                    logging.error(f"Error converting data types: {e}")
                    logging.error(f"Problematic trade element: {etree.tostring(trade, encoding='unicode')}")
                    continue
                
                logging.debug(f"Processed trade data: {trade_data}")
                data.append(trade_data)
            except Exception as e:
                logging.error(f"Error processing trade element: {e}")
                logging.error(f"Problematic trade element: {etree.tostring(trade, encoding='unicode')}")
                logging.error(f"Traceback: {traceback.format_exc()}")
        
        if not data:
            logging.error("No valid trade data found in the XML file")
            raise ValueError("No valid trade data found in the XML file")
        
        logging.info(f"Creating DataFrame with {len(data)} trades")
        df = pd.DataFrame(data)
        return process_trade_data(df)
    except etree.XMLSyntaxError as e:
        logging.error(f"XML Syntax Error: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise ValueError(f"Invalid XML format: {e}")
    except Exception as e:
        logging.error(f"Unexpected error processing XML data: {e}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise ValueError(f"Error processing XML data: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'json', 'xml'}
