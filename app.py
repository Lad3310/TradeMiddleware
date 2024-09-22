import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, AuditLog, ProcessedTrade
from utils import process_trade_data, allowed_file, simulate_external_api_call, process_xml_data
import pandas as pd
import logging
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
import traceback
import io
from lxml import etree

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.debug(f"Login attempt for username: {username}")
        try:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                logging.info(f"User {username} logged in successfully")
                return redirect(url_for('dashboard'))
            else:
                logging.warning(f"Failed login attempt for username: {username}")
                flash('Invalid username or password')
        except SQLAlchemyError as e:
            logging.error(f"Database error during login: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            flash('An error occurred during login. Please try again later.')
        except Exception as e:
            logging.error(f"Unexpected error during login: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            flash('An unexpected error occurred. Please try again later.')
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
            logging.info(f"Processing file: {file.filename}")
            file_content = file.read()
            file_extension = file.filename.rsplit('.', 1)[1].lower()

            if file_extension == 'csv':
                df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
                processed_data = process_trade_data(df)
            elif file_extension == 'json':
                df = pd.read_json(io.StringIO(file_content.decode('utf-8')))
                processed_data = process_trade_data(df)
            elif file_extension == 'xml':
                try:
                    processed_data = process_xml_data(file_content)
                except ValueError as xml_error:
                    logging.error(f"XML processing error: {str(xml_error)}")
                    flash(f'Error processing XML file: {str(xml_error)}. Please check the file format and try again.')
                    return redirect(url_for('dashboard'))
                except etree.XMLSyntaxError as xml_syntax_error:
                    logging.error(f"XML syntax error: {str(xml_syntax_error)}")
                    flash(f'Invalid XML format: {str(xml_syntax_error)}. Please check the file and try again.')
                    return redirect(url_for('dashboard'))
            else:
                raise ValueError("Unsupported file format")
            
            success = simulate_external_api_call(processed_data)
            
            audit_log = AuditLog(user_id=current_user.id, filename=file.filename, status='Success' if success else 'Failed')
            db.session.add(audit_log)
            
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
        except ValueError as e:
            db.session.rollback()
            logging.error(f"Error processing file {file.filename}: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            flash(f'Error processing file: {str(e)}. Please check the file format and try again.')
        except pd.errors.EmptyDataError:
            db.session.rollback()
            logging.error(f"Empty file error: {file.filename}")
            flash('The uploaded file is empty. Please upload a file with data.')
        except pd.errors.ParserError as e:
            db.session.rollback()
            logging.error(f"Parser error for file {file.filename}: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            flash(f'Error parsing file: {str(e)}. Please check the file format and try again.')
        except Exception as e:
            db.session.rollback()
            logging.error(f"Unexpected error processing file {file.filename}: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            flash(f'An unexpected error occurred while processing the file: {str(e)}. Please try again later.')
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
    app.run(host='0.0.0.0', port=5000, debug=True)
