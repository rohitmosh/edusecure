from flask import Flask, request, jsonify, session, send_file
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import hashlib
import secrets

# Import our custom modules
from auth import authenticate_user, get_user_role, hash_password
from upload import process_upload, convert_pdf_to_images
from chaotic import scramble_image, unscramble_image, generate_chaos_key
from hashing import compute_sha256, verify_integrity
from phe_wrapper import encrypt_metadata, decrypt_metadata, increment_counter
from timelock import check_release_time, schedule_release
from logs import append_log, verify_log_chain
from examcenter import download_scrambled_paper, decrypt_paper

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app, supports_credentials=True)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username, role):
        self.id = username
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    # Load user from users.json
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                users_data = json.load(f)
            
            for user in users_data.get('users', []):
                if user['username'] == user_id:
                    return User(user['username'], user['role'])
    except:
        pass
    return None

# Configuration
UPLOAD_FOLDER = '../papers'
USERS_FILE = '../users/users.json'
LOGS_FILE = '../logs/logs.json'
CONFIG_FILE = '../config/system_config.json'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('../users', exist_ok=True)
os.makedirs('../logs', exist_ok=True)
os.makedirs('../config', exist_ok=True)

# Add poppler to PATH if it exists in project directory
poppler_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'poppler')
if os.path.exists(poppler_path):
    for root, dirs, files in os.walk(poppler_path):
        if 'pdftoppm.exe' in files:
            current_path = os.environ.get('PATH', '')
            if root not in current_path:
                os.environ['PATH'] = root + os.pathsep + current_path
            break

@app.route('/api/login', methods=['POST'])
def login():
    """User authentication endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user_data = authenticate_user(username, password)
        if user_data:
            user = User(username, user_data['role'])
            login_user(user)
            
            # Log the login event
            append_log('login', username, None, f"User {username} logged in")
            
            return jsonify({
                'success': True,
                'role': user_data['role'],
                'username': username
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """User logout endpoint"""
    username = current_user.username
    append_log('logout', username, None, f"User {username} logged out")
    logout_user()
    return jsonify({'success': True})

@app.route('/api/faculty/upload', methods=['POST'])
@login_required
def faculty_upload():
    """Faculty upload endpoint for exam papers"""
    try:
        if current_user.role != 'faculty':
            return jsonify({'error': 'Unauthorized'}), 403
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        exam_id = request.form.get('exam_id')
        scheduled_time = request.form.get('scheduled_time')
        
        if not exam_id or not scheduled_time:
            return jsonify({'error': 'Exam ID and scheduled time required'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Process the upload
        result = process_upload(
            file, 
            exam_id, 
            current_user.username, 
            scheduled_time,
            app.config['UPLOAD_FOLDER']
        )
        
        if result['success']:
            # Log the upload event
            append_log('upload', current_user.username, exam_id, 
                      f"Exam paper {exam_id} uploaded and scrambled")
            
            return jsonify(result)
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/papers', methods=['GET'])
@login_required
def admin_get_papers():
    """Admin endpoint to view all uploaded papers"""
    try:
        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        papers = []
        papers_dir = app.config['UPLOAD_FOLDER']
        
        if os.path.exists(papers_dir):
            for exam_folder in os.listdir(papers_dir):
                exam_path = os.path.join(papers_dir, exam_folder)
                if os.path.isdir(exam_path):
                    metadata_path = os.path.join(exam_path, 'metadata.json')
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                            papers.append(metadata)
        
        return jsonify({'papers': papers})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/release_key/<exam_id>', methods=['POST'])
@login_required
def admin_release_key(exam_id):
    """Admin endpoint to release chaos key at scheduled time"""
    try:
        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        exam_path = os.path.join(app.config['UPLOAD_FOLDER'], exam_id)
        if not os.path.exists(exam_path):
            return jsonify({'error': 'Exam not found'}), 404
        
        # Check if it's time to release
        metadata_path = os.path.join(exam_path, 'metadata.json')
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        if not check_release_time(metadata['scheduled_time']):
            return jsonify({'error': 'Not yet time to release key'}), 403
        
        # Release the key (decrypt chaos_key.enc)
        chaos_key_path = os.path.join(exam_path, 'chaos_key.enc')
        if os.path.exists(chaos_key_path):
            # Mark as released in metadata
            metadata['key_released'] = True
            metadata['release_time'] = datetime.now().isoformat()
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Log the key release
            append_log('key_release', current_user.username, exam_id,
                      f"Chaos key released for exam {exam_id}")
            
            return jsonify({'success': True, 'message': 'Key released successfully'})
        else:
            return jsonify({'error': 'Chaos key not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/verify_integrity/<exam_id>', methods=['GET'])
@login_required
def admin_verify_integrity(exam_id):
    """Admin endpoint to verify paper integrity"""
    try:
        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        result = verify_integrity(exam_id, app.config['UPLOAD_FOLDER'])
        
        # Log the verification
        append_log('verify', current_user.username, exam_id,
                  f"Integrity verification for exam {exam_id}: {'PASSED' if result['valid'] else 'FAILED'}")
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/logs', methods=['GET'])
@login_required
def admin_get_logs():
    """Admin endpoint to view tamper-proof logs"""
    try:
        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        if os.path.exists(LOGS_FILE):
            with open(LOGS_FILE, 'r') as f:
                logs = json.load(f)
            
            # Verify log chain integrity
            chain_valid = verify_log_chain(logs)
            
            return jsonify({
                'logs': logs,
                'chain_valid': chain_valid
            })
        else:
            return jsonify({'logs': [], 'chain_valid': True})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examcenter/papers', methods=['GET'])
@login_required
def examcenter_get_papers():
    """Exam center endpoint to view available papers"""
    try:
        if current_user.role != 'exam_center':
            return jsonify({'error': 'Unauthorized'}), 403
        
        papers = []
        papers_dir = app.config['UPLOAD_FOLDER']
        
        if os.path.exists(papers_dir):
            for exam_folder in os.listdir(papers_dir):
                exam_path = os.path.join(papers_dir, exam_folder)
                if os.path.isdir(exam_path):
                    metadata_path = os.path.join(exam_path, 'metadata.json')
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                            # Only show basic info to exam centers
                            papers.append({
                                'exam_id': metadata['exam_id'],
                                'scheduled_time': metadata['scheduled_time'],
                                'key_released': metadata.get('key_released', False)
                            })
        
        return jsonify({'papers': papers})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examcenter/download/<exam_id>', methods=['GET'])
@login_required
def examcenter_download(exam_id):
    """Exam center endpoint to download scrambled papers"""
    try:
        if current_user.role != 'exam_center':
            return jsonify({'error': 'Unauthorized'}), 403
        
        result = download_scrambled_paper(exam_id, app.config['UPLOAD_FOLDER'])
        
        if result['success']:
            # Log the download
            append_log('download', current_user.username, exam_id,
                      f"Scrambled paper {exam_id} downloaded by exam center")
            
            return jsonify(result)
        else:
            return jsonify({'error': result['error']}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examcenter/decrypt/<exam_id>', methods=['POST'])
@login_required
def examcenter_decrypt(exam_id):
    """Exam center endpoint to decrypt papers when key is released"""
    try:
        if current_user.role != 'exam_center':
            return jsonify({'error': 'Unauthorized'}), 403
        
        result = decrypt_paper(exam_id, app.config['UPLOAD_FOLDER'])
        
        if result['success']:
            # Increment access counter homomorphically
            increment_counter(exam_id, app.config['UPLOAD_FOLDER'])
            
            # Log the decryption
            append_log('decrypt', current_user.username, exam_id,
                      f"Paper {exam_id} decrypted by exam center")
            
            return jsonify(result)
        else:
            return jsonify({'error': result['error']}), 403
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview/original/<exam_id>/<int:page>', methods=['GET'])
@login_required
def preview_original(exam_id, page):
    """Serve original page image for preview"""
    try:
        if current_user.role not in ['admin', 'faculty']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Look for original image in temp directory
        temp_dir = os.path.join(UPLOAD_FOLDER, exam_id, 'temp')
        image_path = os.path.join(temp_dir, f'page_{page}.png')
        
        if not os.path.exists(image_path):
            return jsonify({'error': 'Original image not found'}), 404
        
        return send_file(image_path, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview/scrambled/<exam_id>/<int:page>', methods=['GET'])
@login_required
def preview_scrambled(exam_id, page):
    """Serve scrambled page image for preview"""
    try:
        if current_user.role not in ['admin', 'faculty', 'exam_center']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Look for scrambled image
        image_path = os.path.join(UPLOAD_FOLDER, exam_id, f'scrambled_page_{page}.png')
        
        if not os.path.exists(image_path):
            return jsonify({'error': 'Scrambled image not found'}), 404
        
        return send_file(image_path, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview/info/<exam_id>', methods=['GET'])
@login_required
def preview_info(exam_id):
    """Get preview information for an exam"""
    try:
        if current_user.role not in ['admin', 'faculty', 'exam_center']:
            return jsonify({'error': 'Unauthorized'}), 403
        
        exam_dir = os.path.join(UPLOAD_FOLDER, exam_id)
        if not os.path.exists(exam_dir):
            return jsonify({'error': 'Exam not found'}), 404
        
        # Count pages
        scrambled_pages = []
        original_pages = []
        
        # Check scrambled pages
        for file in os.listdir(exam_dir):
            if file.startswith('scrambled_page_') and file.endswith('.png'):
                page_num = int(file.replace('scrambled_page_', '').replace('.png', ''))
                scrambled_pages.append(page_num)
        
        # Check original pages in temp directory
        temp_dir = os.path.join(exam_dir, 'temp')
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                if file.startswith('page_') and file.endswith('.png'):
                    page_num = int(file.replace('page_', '').replace('.png', ''))
                    original_pages.append(page_num)
        
        scrambled_pages.sort()
        original_pages.sort()
        
        return jsonify({
            'exam_id': exam_id,
            'scrambled_pages': scrambled_pages,
            'original_pages': original_pages,
            'total_pages': max(len(scrambled_pages), len(original_pages))
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Initialize system if needed
    if not os.path.exists(USERS_FILE):
        # Create default users
        default_users = {
            "users": [
                {
                    "username": "admin1",
                    "password": hash_password("admin123"),
                    "role": "admin"
                },
                {
                    "username": "faculty1", 
                    "password": hash_password("faculty123"),
                    "role": "faculty"
                },
                {
                    "username": "center1",
                    "password": hash_password("center123"), 
                    "role": "exam_center"
                }
            ]
        }
        
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=2)
    
    app.run(debug=True, host='0.0.0.0', port=5000)