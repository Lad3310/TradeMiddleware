import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from utils import process_trade_data, process_xml_data, allowed_file, simulate_external_api_call
import pandas as pd
import io
import logging
import traceback
from flask_socketio import SocketIO
import time
from lxml import etree
from sqlalchemy import func
from models import db, User, AuditLog, ProcessedTrade

app = Flask(__name__)
app.config.from_object(Config)

# Add UPLOAD_FOLDER configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# Create 'uploads' directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)

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
        user_agent = request.headers.get('User-Agent')
        is_mobile = 'Mobile' in user_agent
        logging.debug(f"Login attempt for username: {username}")
        logging.debug(f"User Agent: {user_agent}")
        logging.debug(f"Is Mobile: {is_mobile}")
        try:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                logging.info(f"User {username} logged in successfully (Mobile: {is_mobile})")
                return redirect(url_for('dashboard'))
            else:
                logging.warning(f"Failed login attempt for username: {username} (Mobile: {is_mobile})")
                flash('Invalid username or password')
        except Exception as e:
            logging.error(f"Unexpected error during login: {str(e)} (Mobile: {is_mobile})")
            logging.error(f"Traceback: {traceback.format_exc()}")
            flash('An unexpected error occurred. Please try again later.')
            return render_template('login.html'), 500
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
        return jsonify({'status': 'error', 'message': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})
    if file and allowed_file(file.filename):
        try:
            logging.info(f"Processing file: {file.filename}")
            file_content = file.read()
            file_extension = file.filename.rsplit('.', 1)[1].lower()

            start_time = time.time()
            timeout = 300  # 5 minutes timeout

            log_filename = f"processing_log_{int(time.time())}.txt"
            log_filepath = os.path.join(app.config['UPLOAD_FOLDER'], log_filename)

            with open(log_filepath, 'w') as log_file:
                log_file.write(f"Processing started for file: {file.filename}\n")

                if file_extension == 'csv':
                    df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
                    processed_data = process_trade_data(df)
                elif file_extension == 'json':
                    df = pd.read_json(io.StringIO(file_content.decode('utf-8')))
                    processed_data = process_trade_data(df)
                elif file_extension == 'xml':
                    try:
                        def progress_callback(processed, total):
                            progress = (processed / total) * 100
                            log_file.write(f"XML Processing Progress: {progress:.2f}%\n")
                            log_file.flush()
                            socketio.emit('processing_progress', {'processed': processed, 'total': total})

                        processed_data = process_xml_data(file_content, progress_callback=progress_callback)
                    except ValueError as xml_error:
                        log_file.write(f"XML processing error: {str(xml_error)}\n")
                        return jsonify({'status': 'error', 'message': f'Error processing XML file: {str(xml_error)}. Please check the file format and try again.'})
                    except etree.XMLSyntaxError as xml_syntax_error:
                        log_file.write(f"XML syntax error: {str(xml_syntax_error)}\n")
                        return jsonify({'status': 'error', 'message': f'Invalid XML format: {str(xml_syntax_error)}. Please check the file and try again.'})
                else:
                    return jsonify({'status': 'error', 'message': 'Unsupported file format'})
                
                processing_time = time.time() - start_time
                log_file.write(f"File processed successfully. Rows: {len(processed_data)}. Processing time: {processing_time:.2f} seconds\n")
                
                if time.time() - start_time > timeout:
                    log_file.write("Processing timeout. Please try with a smaller file or contact support.\n")
                    return jsonify({'status': 'error', 'message': 'Processing timeout. Please try with a smaller file or contact support.'})
                
                api_result = simulate_external_api_call(processed_data, max_retries=5, timeout=30, chunk_size=10, total_timeout=300)
                log_file.write(f"API Simulation Result: {api_result}\n")

            audit_log = AuditLog(user_id=current_user.id, filename=file.filename, status=api_result['status'], log_file=log_filename)
            db.session.add(audit_log)
            db.session.flush()
            
            if audit_log.id is None:
                raise ValueError("Failed to generate audit_log_id")
            
            logging.info(f"Created AuditLog entry with id: {audit_log.id}")
            
            for _, row in processed_data.iterrows():
                processed_trade = ProcessedTrade(
                    audit_log_id=audit_log.id,
                    trade_id=row['trade_id'],
                    symbol=row['symbol'],
                    quantity=row['quantity'],
                    price=row['price'],
                    status='Processed' if _ < api_result['processed_rows'] else 'Failed'
                )
                db.session.add(processed_trade)
            
            db.session.commit()
            logging.info(f"Processed trades saved to database. Total trades: {len(processed_data)}")
            return jsonify({
                'status': api_result['status'],
                'message': api_result['message'],
                'details': {
                    'success_rate': api_result['success_rate'],
                    'processed_rows': api_result['processed_rows'],
                    'failed_rows': api_result['failed_rows'],
                    'total_attempts': api_result['total_attempts'],
                    'total_delay': api_result['total_delay']
                },
                'log_file': log_filename
            })
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error processing file {file.filename}: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            return jsonify({'status': 'error', 'message': f'An error occurred while processing the file: {str(e)}. Please try again later.'})
    else:
        return jsonify({'status': 'error', 'message': 'File type not allowed'})

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

@app.route('/api/dashboard_stats')
@login_required
def dashboard_stats():
    total_files = AuditLog.query.filter_by(user_id=current_user.id).count()
    successful_uploads = AuditLog.query.filter_by(user_id=current_user.id, status='success').count()
    failed_uploads = AuditLog.query.filter_by(user_id=current_user.id, status='failure').count()
    
    recent_uploads = AuditLog.query.filter_by(user_id=current_user.id).order_by(AuditLog.timestamp.desc()).limit(5).all()
    recent_uploads_data = [{
        'id': log.id,
        'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'filename': log.filename,
        'status': log.status
    } for log in recent_uploads]

    return jsonify({
        'total_files': total_files,
        'successful_uploads': successful_uploads,
        'failed_uploads': failed_uploads,
        'recent_uploads': recent_uploads_data
    })

@app.route('/download_log/<filename>')
@login_required
def download_log(filename):
    log_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(log_filepath):
        return send_file(log_filepath, as_attachment=True)
    else:
        flash('Log file not found', 'error')
        return redirect(url_for('dashboard'))

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
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)