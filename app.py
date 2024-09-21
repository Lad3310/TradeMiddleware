import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, AuditLog, ProcessedTrade
from utils import process_trade_data, allowed_file, simulate_external_api_call, process_xml_data
import pandas as pd
import logging
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        try:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            logging.info(f"User {username} registered successfully")
            flash('Account created successfully')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = str(e)
            logging.error(f"Database error during registration: {error_msg}")
            flash(f'An error occurred during registration: {error_msg}. Please try again later.')
        except Exception as e:
            db.session.rollback()
            error_msg = str(e)
            logging.error(f"Unexpected error during registration: {error_msg}")
            flash(f'An unexpected error occurred: {error_msg}. Please try again later.')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('dashboard'))
    if file and allowed_file(file.filename):
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
                processed_data = process_trade_data(df)
            elif file.filename.endswith('.json'):
                df = pd.read_json(file)
                processed_data = process_trade_data(df)
            elif file.filename.endswith('.xml'):
                xml_content = file.read()
                processed_data = process_xml_data(xml_content)
            else:
                raise ValueError("Unsupported file format")
            
            # Simulate sending data to external API
            success = simulate_external_api_call(processed_data)
            
            # Log the file transmission
            audit_log = AuditLog(user_id=current_user.id, filename=file.filename, status='Success' if success else 'Failed')
            db.session.add(audit_log)
            
            # Log individual trades
            for _, row in processed_data.iterrows():
                processed_trade = ProcessedTrade(
                    audit_log_id=audit_log.id,
                    trade_id=row['trade_id'],
                    symbol=row['symbol'],
                    quantity=row['quantity'],
                    price=row['price'],
                    status='Processed' if success else 'Failed'
                )
                db.session.add(processed_trade)
            
            db.session.commit()
            flash('File processed and transmitted successfully' if success else 'File processed but transmission failed')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error processing file: {str(e)}")
            flash(f'Error processing file: {str(e)}')
    else:
        flash('File type not allowed')
    return redirect(url_for('dashboard'))

@app.route('/audit_trail')
@login_required
def audit_trail():
    logs = AuditLog.query.filter_by(user_id=current_user.id).order_by(AuditLog.timestamp.desc()).all()
    return render_template('audit_trail.html', logs=logs)

@app.route('/api/trades/<int:audit_log_id>')
@login_required
def get_processed_trades(audit_log_id):
    trades = ProcessedTrade.query.filter_by(audit_log_id=audit_log_id).all()
    return jsonify([{
        'trade_id': trade.trade_id,
        'symbol': trade.symbol,
        'quantity': trade.quantity,
        'price': trade.price,
        'status': trade.status
    } for trade in trades])

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logging.error(f"Internal Server Error: {str(error)}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
