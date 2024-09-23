from app import db
from sqlalchemy import inspect

inspector = inspect(db.engine)
columns = inspector.get_columns('audit_log')
column_names = [column['name'] for column in columns]

print("Columns in audit_log table:", column_names)
