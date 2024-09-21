from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    filename = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False)

class ProcessedTrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    audit_log_id = db.Column(db.Integer, db.ForeignKey('audit_log.id'), nullable=False)
    trade_id = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
