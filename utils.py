import logging
import pandas as pd
from lxml import etree
import traceback
import io
import time
import random
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import aiohttp
import json

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

def exponential_backoff(attempt, base_delay=1, max_delay=60, factor=2, jitter=0.1):
    delay = min(base_delay * (factor ** attempt), max_delay)
    jitter_value = random.uniform(0, jitter * delay)
    return delay + jitter_value

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=30):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure_time = None
        self.state = "CLOSED"

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_failure_time = time.time()

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def allow_request(self):
        if self.state == "CLOSED":
            return True
        elif self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF-OPEN"
                return True
        return False

async def async_process_chunk(session, chunk, timeout, circuit_breaker):
    if not circuit_breaker.allow_request():
        logging.warning("Circuit breaker is open. Skipping request.")
        return False

    try:
        async with session.post('https://httpbin.org/post', json=chunk, timeout=timeout) as response:
            if response.status == 200:
                await response.json()
                circuit_breaker.record_success()
                return True
            else:
                logging.warning(f"API call failed with status code: {response.status}")
                circuit_breaker.record_failure()
                return False
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logging.warning(f"API call failed: {str(e)}")
        circuit_breaker.record_failure()
        return False

def json_serial(obj):
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} not serializable')

def simulate_external_api_call(trade_data, max_retries=5, timeout=30, chunk_size=10, total_timeout=300):
    trade_data_json = trade_data.to_dict(orient='records')
    trade_data_serializable = json.loads(json.dumps(trade_data_json, default=json_serial))
    return asyncio.run(async_simulate_external_api_call(trade_data_serializable, max_retries, timeout, chunk_size, total_timeout))

async def async_simulate_external_api_call(trade_data, max_retries=5, timeout=30, chunk_size=10, total_timeout=300):
    total_rows = len(trade_data)
    processed_rows = 0
    failed_rows = 0
    total_attempts = 0
    total_delay = 0
    start_time = time.time()

    circuit_breaker = CircuitBreaker()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(0, total_rows, chunk_size):
            chunk = trade_data[i:i+chunk_size]
            task = asyncio.create_task(process_chunk_with_retry(session, chunk, max_retries, timeout, circuit_breaker))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

    for result in results:
        processed_rows += result['processed']
        failed_rows += result['failed']
        total_attempts += result['attempts']
        total_delay += result['delay']

    success_rate = processed_rows / total_rows if total_rows > 0 else 0
    status = 'success' if success_rate > 0.8 else 'partial_success' if success_rate > 0 else 'failure'

    result = {
        'status': status,
        'success_rate': success_rate,
        'processed_rows': processed_rows,
        'failed_rows': failed_rows,
        'total_attempts': total_attempts,
        'total_delay': total_delay,
        'message': f"Processed {processed_rows}/{total_rows} rows. {failed_rows} rows failed."
    }
    logging.info(f"API simulation completed. Result: {result}")
    return result

async def process_chunk_with_retry(session, chunk, max_retries, timeout, circuit_breaker):
    attempts = 0
    delay = 0
    processed = 0
    failed = 0

    while attempts < max_retries:
        attempts += 1
        try:
            success = await async_process_chunk(session, chunk, timeout, circuit_breaker)
            if success:
                processed = len(chunk)
                logging.info(f"Successfully processed chunk of {processed} rows")
                return {'processed': processed, 'failed': 0, 'attempts': attempts, 'delay': delay}
        except Exception as e:
            logging.warning(f"Attempt {attempts} failed. Error: {str(e)}")
        
        delay += exponential_backoff(attempts)
        logging.info(f"Retrying after {delay} seconds")
        await asyncio.sleep(delay)

    failed = len(chunk)
    logging.error(f"Failed to process chunk of {failed} rows after {attempts} attempts")
    return {'processed': 0, 'failed': failed, 'attempts': attempts, 'delay': delay}

def process_xml_data(xml_content, chunk_size=1000, progress_callback=None):
    logging.info("Starting XML data processing")
    try:
        logging.debug(f"Raw XML content (first 200 chars): {xml_content[:200].decode('utf-8')}")
        
        context = etree.iterparse(io.BytesIO(xml_content), events=('end',), tag='Trade')
        
        data = []
        total_trades = sum(1 for _ in context)
        context = etree.iterparse(io.BytesIO(xml_content), events=('end',), tag='Trade')  # Reset iterator
        processed_trades = 0
        
        start_time = time.time()
        
        def process_trade_chunk(chunk):
            nonlocal processed_trades
            chunk_data = []
            for trade_elem in chunk:
                try:
                    trade_data = {
                        'trade_id': trade_elem.findtext('TradeID'),
                        'symbol': trade_elem.findtext('Security'),
                        'quantity': trade_elem.findtext('Quantity'),
                        'price': trade_elem.findtext('Price')
                    }
                    
                    missing_fields = [field for field, value in trade_data.items() if value is None]
                    if missing_fields:
                        logging.warning(f"Trade is missing required fields: {', '.join(missing_fields)}")
                        logging.warning(f"Skipping trade: {etree.tostring(trade_elem, encoding='unicode')}")
                        continue
                    
                    try:
                        trade_data['quantity'] = int(trade_data['quantity'])
                        trade_data['price'] = float(trade_data['price'])
                    except ValueError as e:
                        logging.error(f"Error converting data types: {e}")
                        logging.error(f"Problematic trade element: {etree.tostring(trade_elem, encoding='unicode')}")
                        continue
                    
                    chunk_data.append(trade_data)
                    processed_trades += 1
                    
                    if processed_trades % 10 == 0:  # Update progress more frequently
                        elapsed_time = time.time() - start_time
                        logging.info(f"Processed {processed_trades}/{total_trades} trades in {elapsed_time:.2f} seconds")
                        if progress_callback:
                            progress_callback(processed_trades, total_trades)
                    
                except Exception as e:
                    logging.error(f"Error processing trade element: {e}")
                    logging.error(f"Problematic trade element: {etree.tostring(trade_elem, encoding='unicode')}")
                    logging.error(f"Traceback: {traceback.format_exc()}")
                
                trade_elem.clear()
            
            return chunk_data
        
        chunk = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for event, elem in context:
                if elem.tag == 'Trade':
                    chunk.append(elem)
                    
                    if len(chunk) == chunk_size:
                        futures.append(executor.submit(process_trade_chunk, chunk))
                        chunk = []
            
            if chunk:
                futures.append(executor.submit(process_trade_chunk, chunk))
            
            for future in as_completed(futures):
                data.extend(future.result())
        
        if not data:
            logging.error("No valid trade data found in the XML file")
            raise ValueError("No valid trade data found in the XML file")
        
        logging.info(f"Creating DataFrame with {len(data)} trades")
        df = pd.DataFrame(data)
        logging.info(f"Total trades in XML: {total_trades}, Processed trades: {processed_trades}")
        
        # Ensure final progress update
        if progress_callback:
            progress_callback(processed_trades, total_trades)
        
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