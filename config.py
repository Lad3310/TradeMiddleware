import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"postgresql://{os.environ.get('PGUSER')}:{os.environ.get('PGPASSWORD')}@{os.environ.get('PGHOST')}:{os.environ.get('PGPORT')}/{os.environ.get('PGDATABASE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
from dotenv import load_dotenv

load_dotenv()  # This line loads the .env file

print("PGUSER:", os.environ.get('PGUSER'))
print("PGPASSWORD:", os.environ.get('PGPASSWORD'))
print("PGHOST:", os.environ.get('PGHOST'))
print("PGPORT:", os.environ.get('PGPORT'))
print("PGDATABASE:", os.environ.get('PGDATABASE'))
