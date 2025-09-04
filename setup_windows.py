#!/usr/bin/env python3
"""
Windows-Specific Setup for EduSecure-HE
Handles common Windows dependency issues
"""

import os
import sys
import subprocess
import time

def print_banner():
    print("🪟 EduSecure-HE Windows Setup")
    print("=" * 40)
    print("Fixing common Windows dependency issues...")
    print("=" * 40)

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("📦 Upgrading pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Pip upgrade failed, continuing anyway...")
        return False

def install_dependencies_step_by_step():
    """Install dependencies one by one to handle issues"""
    print("\n📦 Installing dependencies step by step...")
    
    # Core dependencies first
    core_deps = [
        "Flask",
        "Flask-Login", 
        "Flask-CORS",
        "requests"
    ]
    
    print("🔧 Installing core dependencies...")
    for dep in core_deps:
        try:
            print(f"   Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
        except subprocess.CalledProcessError:
            print(f"   ⚠️ Failed to install {dep}, trying to continue...")
    
    # Image processing dependencies
    image_deps = [
        "Pillow",
        "pdf2image"
    ]
    
    print("🖼️ Installing image processing dependencies...")
    for dep in image_deps:
        try:
            print(f"   Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
        except subprocess.CalledProcessError:
            print(f"   ⚠️ Failed to install {dep}")
            if dep == "Pillow":
                print("   💡 Trying alternative Pillow installation...")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "Pillow"], check=True)
                except:
                    print("   ❌ Pillow installation failed - you may need to install manually")
    
    # Scientific dependencies
    sci_deps = [
        "numpy",
    ]
    
    print("🔬 Installing scientific dependencies...")
    for dep in sci_deps:
        try:
            print(f"   Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
        except subprocess.CalledProcessError:
            print(f"   ⚠️ Failed to install {dep}")
    
    # Crypto dependencies
    crypto_deps = [
        "phe",
        "pycryptodome"
    ]
    
    print("🔐 Installing cryptographic dependencies...")
    for dep in crypto_deps:
        try:
            print(f"   Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
        except subprocess.CalledProcessError:
            print(f"   ⚠️ Failed to install {dep}")
            if dep == "pycryptodome":
                print("   💡 Trying alternative crypto installation...")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "pycrypto"], check=True)
                except:
                    print("   💡 Trying pycryptodome with --only-binary...")
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", "--only-binary=all", "pycryptodome"], check=True)
                    except:
                        print("   ❌ Crypto installation failed")
    
    # Optional dependencies
    optional_deps = [
        "python-docx",
        "pytest"
    ]
    
    print("📄 Installing optional dependencies...")
    for dep in optional_deps:
        try:
            print(f"   Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
        except subprocess.CalledProcessError:
            print(f"   ⚠️ Failed to install {dep} (optional)")

def check_installations():
    """Check which packages were successfully installed"""
    print("\n🔍 Checking installations...")
    
    required_packages = [
        "flask",
        "flask_login", 
        "flask_cors",
        "PIL",  # Pillow
        "numpy",
        "phe",
        "requests"
    ]
    
    installed = []
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            installed.append(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"   ❌ {package}")
    
    print(f"\n📊 Summary: {len(installed)} installed, {len(missing)} missing")
    
    if missing:
        print("\n⚠️ Missing packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n💡 You can try installing missing packages manually:")
        for pkg in missing:
            print(f"   pip install {pkg}")
    
    return len(missing) == 0

def create_minimal_app():
    """Create a minimal version that works with available packages"""
    print("\n🔧 Creating minimal application version...")
    
    minimal_app = '''
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import os
import json
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = "demo_secret_key_2025"
CORS(app, supports_credentials=True)

# Simple user data
USERS = {
    "admin1": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "admin"},
    "faculty1": {"password": hashlib.sha256("faculty123".encode()).hexdigest(), "role": "faculty"},
    "center1": {"password": hashlib.sha256("center123".encode()).hexdigest(), "role": "exam_center"}
}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in USERS:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if USERS[username]["password"] == hashed_password:
            session['user'] = username
            session['role'] = USERS[username]["role"]
            return jsonify({
                'success': True,
                'role': USERS[username]["role"],
                'username': username
            })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/admin/papers', methods=['GET'])
def admin_papers():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'papers': []})

@app.route('/api/faculty/upload', methods=['POST'])
def faculty_upload():
    if session.get('role') != 'faculty':
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'success': True, 'message': 'Upload simulation - full features require all dependencies'})

@app.route('/api/examcenter/papers', methods=['GET'])
def examcenter_papers():
    if session.get('role') != 'exam_center':
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({'papers': []})

if __name__ == '__main__':
    print("🔐 EduSecure-HE Minimal Version")
    print("=" * 40)
    print("✅ Basic authentication working")
    print("⚠️ Full crypto features require all dependencies")
    print("🌐 Server running at http://localhost:5000")
    print("=" * 40)
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    # Save minimal app
    os.makedirs("backend", exist_ok=True)
    with open("backend/minimal_app.py", "w") as f:
        f.write(minimal_app)
    
    print("✅ Minimal app created: backend/minimal_app.py")
    print("💡 You can run it with: python backend/minimal_app.py")

def main():
    print_banner()
    
    # Upgrade pip first
    upgrade_pip()
    
    # Install dependencies step by step
    install_dependencies_step_by_step()
    
    # Check what was installed
    all_installed = check_installations()
    
    if not all_installed:
        print("\n⚠️ Some dependencies failed to install")
        print("🔧 Creating minimal version that works with available packages...")
        create_minimal_app()
        
        print("\n💡 Options to continue:")
        print("1. Run minimal version: python backend/minimal_app.py")
        print("2. Install missing packages manually and try full version")
        print("3. Use online Python environment (Replit, Colab, etc.)")
    else:
        print("\n🎉 All dependencies installed successfully!")
        print("✅ You can now run the full application")
    
    print("\n📋 Next steps:")
    print("1. Install frontend: npm install")
    print("2. Start backend: python backend/run.py (or minimal_app.py)")
    print("3. Start frontend: npm run dev")
    print("4. Open browser: http://localhost:5173")

if __name__ == "__main__":
    main()