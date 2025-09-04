#!/usr/bin/env python3
"""
EduSecure-HE Quick Start (No Virtual Environment)
Simple startup script that uses system Python
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print application banner"""
    print("🔐 EduSecure-HE: Quick Start")
    print("=" * 40)
    print("🎯 Simple startup without virtual environment")
    print("=" * 40)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_backend_deps():
    """Install backend dependencies using system pip"""
    print("\n📦 Installing backend dependencies...")
    
    try:
        # Install requirements directly with system pip
        requirements_file = Path("backend/requirements.txt")
        if requirements_file.exists():
            print("📥 Installing Python packages...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], 
                         check=True)
            print("✅ Backend dependencies installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        print("💡 Try running: pip install -r backend/requirements.txt")
        return False

def install_frontend_deps():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    
    try:
        print("📥 Installing Node.js packages...")
        subprocess.run(["npm", "install"], check=True)
        print("✅ Frontend dependencies installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install frontend dependencies: {e}")
        return False

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting backend server...")
    
    try:
        # Start backend server using system Python
        backend_process = subprocess.Popen(
            [sys.executable, "run.py"],
            cwd="backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print("✅ Backend server starting at http://localhost:5000")
        return backend_process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend server"""
    print("\n🚀 Starting frontend server...")
    
    try:
        # Start frontend server
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print("✅ Frontend server starting at http://localhost:5173")
        return frontend_process
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def main():
    """Main function"""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        print("\n💡 Please install Python 3.10+ and try again")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Install dependencies
    print("\n🔧 Installing dependencies...")
    if not install_backend_deps():
        print("\n💡 Please install backend dependencies manually:")
        print("   pip install -r backend/requirements.txt")
        input("Press Enter to exit...")
        sys.exit(1)
    
    if not install_frontend_deps():
        print("\n💡 Please install Node.js and run: npm install")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Start servers
    backend_process = start_backend()
    if not backend_process:
        input("Press Enter to exit...")
        sys.exit(1)
    
    time.sleep(3)  # Give backend time to start
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Wait and open browser
    print("\n⏳ Waiting for servers to start...")
    time.sleep(5)
    
    print("\n🌐 Opening browser...")
    webbrowser.open("http://localhost:5173")
    
    print("\n" + "=" * 60)
    print("🎉 EduSecure-HE is now running!")
    print("📱 Frontend: http://localhost:5173")
    print("🔧 Backend API: http://localhost:5000")
    print("\n👥 Demo Credentials:")
    print("   Admin: admin1 / admin123")
    print("   Faculty: faculty1 / faculty123") 
    print("   Exam Center: center1 / center123")
    print("\n⚠️  Press Ctrl+C to stop all servers")
    print("=" * 60)
    
    try:
        # Keep both processes running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("\n❌ Backend server stopped unexpectedly")
                break
                
            if frontend_process.poll() is not None:
                print("\n❌ Frontend server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        # Wait for clean shutdown
        time.sleep(2)
        
        print("👋 EduSecure-HE stopped successfully")

if __name__ == "__main__":
    main()