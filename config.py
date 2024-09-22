import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Config:
    SECRET_KEY = os.urandom(32)
    try:
        required_env_vars = ['PGUSER', 'PGPASSWORD', 'PGHOST', 'PGPORT', 'PGDATABASE']
        missing_vars = [var for var in required_env_vars if var not in os.environ]
        
        if missing_vars:
            raise KeyError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['PGUSER']}:{os.environ['PGPASSWORD']}@{os.environ['PGHOST']}:{os.environ['PGPORT']}/{os.environ['PGDATABASE']}"
        logging.info("Database configuration loaded successfully")
        logging.debug(f"Database URI: {SQLALCHEMY_DATABASE_URI.replace(os.environ['PGPASSWORD'], '********')}")
    except KeyError as e:
        logging.error(f"Environment variable error: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in config: {str(e)}")
        raise

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = {'csv', 'json', 'xml'}
