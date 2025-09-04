#!/usr/bin/env python3
"""
EduSecure-HE Application Launcher
This script helps you start both backend and frontend servers
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def print_banner():
    """Print application banner"""
    print("🔐 EduSecure-HE: Secure Exam Paper Management System")
    print("=" * 60)
    print("🎯 Features:")
    print("  • Chaotic Pixel Scrambling")
    print("  • Homomorphic Encryption") 
    print("  • Time-Lock Access Control")
    print("  • Tamper-Proof Logging")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_node():
    """Check if Node.js is available"""
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Node.js version: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js not found. Please install Node.js 18+")
        return False

def install_backend_deps():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    try:
        # Check if virtual environment exists
        venv_dir = backend_dir / "venv"
        if not venv_dir.exists():
            print("🔧 Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], 
                         check=True, cwd=backend_dir)
        
        # Determine pip path
        if os.name == 'nt':  # Windows
            pip_path = venv_dir / "Scripts" / "pip.exe"
            python_path = venv_dir / "Scripts" / "python.exe"
        else:  # Unix/Linux/macOS
            pip_path = venv_dir / "bin" / "pip"
            python_path = venv_dir / "bin" / "python"
        
        # Install requirements
        requirements_file = backend_dir / "requirements.txt"
        if requirements_file.exists():
            print("📥 Installing Python packages...")
            # Try pip first, then fallback to python -m pip
            try:
                subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], 
                             check=True, cwd=backend_dir)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("   🔄 Trying alternative pip installation method...")
                subprocess.run([str(python_path), "-m", "pip", "install", "-r", "requirements.txt"], 
                             check=True, cwd=backend_dir)
            print("✅ Backend dependencies installed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        return False

def install_frontend_deps():
    """Install frontend dependencies"""
    print("\n📦 Installing frontend dependencies...")
    
    package_json = Path("package.json")
    if not package_json.exists():
        print("❌ package.json not found")
        return False
    
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
    backend_dir = Path("backend")
    
    # Determine python path in virtual environment
    venv_dir = backend_dir / "venv"
    if os.name == 'nt':  # Windows
        python_path = venv_dir / "Scripts" / "python.exe"
    else:  # Unix/Linux/macOS
        python_path = venv_dir / "bin" / "python"
    
    try:
        # Start backend server
        backend_process = subprocess.Popen(
            [str(python_path), "run.py"],
            cwd=backend_dir,
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

def wait_for_servers():
    """Wait for servers to be ready and open browser"""
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

def run_security_demo():
    """Run the security features demonstration"""
    print("\n🔐 Would you like to run the security features demo first? (y/n): ", end="")
    try:
        choice = input().lower().strip()
        if choice in ['y', 'yes']:
            print("\n🚀 Running security demonstration...")
            try:
                subprocess.run([sys.executable, "demo_security_features.py"], check=True)
                print("\n✅ Security demo completed!")
                print("Press Enter to continue with the web application...")
                input()
            except subprocess.CalledProcessError:
                print("❌ Security demo failed, but continuing with web app...")
            except KeyboardInterrupt:
                print("\n🛑 Demo interrupted by user")
                return False
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        return False
    
    return True

def main():
    """Main function"""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_node():
        sys.exit(1)
    
    # Install dependencies
    if not install_backend_deps():
        sys.exit(1)
    
    if not install_frontend_deps():
        sys.exit(1)
    
    # Optional security demo
    if not run_security_demo():
        sys.exit(1)
    
    # Start servers
    backend_process = start_backend()
    if not backend_process:
        sys.exit(1)
    
    time.sleep(2)  # Give backend time to start
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        sys.exit(1)
    
    # Wait and open browser
    wait_for_servers()
    
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