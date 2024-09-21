import pandas as pd
from config import Config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def process_trade_data(df):
    # Normalize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Ensure required columns exist
    required_columns = ['trade_id', 'symbol', 'quantity', 'price']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Convert quantity to integer and price to float
    df['quantity'] = df['quantity'].astype(int)
    df['price'] = df['price'].astype(float)
    
    # Validate data
    df = df[df['quantity'] > 0]
    df = df[df['price'] > 0]
    
    return df[required_columns]
