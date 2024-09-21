import os

class Config:
    SECRET_KEY = os.urandom(32)
    try:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['PGUSER']}:{os.environ['PGPASSWORD']}@{os.environ['PGHOST']}:{os.environ['PGPORT']}/{os.environ['PGDATABASE']}"
    except KeyError as e:
        raise KeyError(f"Missing required environment variable: {str(e)}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = {'csv', 'json', 'xml'}
