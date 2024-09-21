import pandas as pd
from config import Config
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_trade_data(df):
    errors = []
    
    # Check for missing required columns
    required_columns = ['trade_id', 'symbol', 'quantity', 'price']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
    
    # Check for empty values in required columns
    for col in required_columns:
        if col in df.columns and df[col].isnull().any():
            errors.append(f"Column '{col}' contains empty values")
    
    # Validate data types and ranges
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
    
    if 'symbol' in df.columns:
        if not df['symbol'].str.match(r'^[A-Z]{1,5}$').all():
            errors.append("'symbol' must be 1-5 uppercase letters")
    
    if 'trade_id' in df.columns:
        if not df['trade_id'].is_unique:
            errors.append("'trade_id' must be unique")
    
    return errors

def process_trade_data(df):
    logging.info(f"Processing trade data with {len(df)} rows")
    
    # Normalize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Validate data
    errors = validate_trade_data(df)
    if errors:
        for error in errors:
            logging.error(error)
        raise ValueError("Data validation failed. Check logs for details.")
    
    # Convert quantity to integer and price to float
    df['quantity'] = df['quantity'].astype(int)
    df['price'] = df['price'].astype(float)
    
    # Add timestamp column
    df['timestamp'] = datetime.utcnow()
    
    logging.info("Trade data processed successfully")
    return df[['trade_id', 'symbol', 'quantity', 'price', 'timestamp']]

def simulate_external_api_call(trade_data):
    # Simulate an API call with potential failures
    import random
    success_rate = 0.9  # 90% success rate
    
    if random.random() < success_rate:
        logging.info("External API call successful")
        return True
    else:
        logging.error("External API call failed")
        return False
