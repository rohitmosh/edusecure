#!/usr/bin/env python3
"""
Complete system startup script
"""
import os
import sys
import subprocess
import time
import threading
import requests

def create_test_files():
    """Create test files if they don't exist"""
    print("📄 Creating test files...")
    
    if not os.path.exists('test.pdf'):
        try:
            subprocess.run([sys.executable, 'create_test_pdf.py'], check=True)
            print("✅ Created test.pdf")
        except subprocess.CalledProcessError:
            print("❌ Failed to create test.pdf")

def start_backend():
    """Start the backend server"""
    print("🔧 Starting backend server...")
    
    try:
        # Start backend in a separate process
        backend_process = subprocess.Popen([
            sys.executable, 'run_backend.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for backend to start
        for i in range(10):
            try:
                response = requests.get('http://localhost:5000/api/health', timeout=2)
                if response.status_code == 200:
                    print("✅ Backend server started successfully")
                    return backend_process
            except:
                pass
            time.sleep(1)
        
        print("❌ Backend server failed to start")
        backend_process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def test_system():
    """Test the complete system"""
    print("🧪 Testing system integration...")
    
    try:
        result = subprocess.run([sys.executable, 'test_frontend_integration.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ System integration test passed")
            return True
        else:
            print("❌ System integration test failed")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ System test timed out")
        return False
    except Exception as e:
        print(f"❌ Error running system test: {e}")
        return False

def start_frontend():
    """Start the frontend development server"""
    print("🌐 Starting frontend development server...")
    
    try:
        # Check if node_modules exists
        if not os.path.exists('node_modules'):
            print("📦 Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        # Start frontend server
        print("🚀 Starting React development server...")
        print("   Frontend will be available at: http://localhost:5173")
        print("   Backend API is running at: http://localhost:5000")
        print("\n📋 Login Credentials:")
        print("   Faculty: faculty1 / faculty123")
        print("   Admin: admin1 / admin123")
        print("   Exam Center: center1 / center123")
        print("\n🎯 Test the upload functionality:")
        print("   1. Login as faculty1")
        print("   2. Upload the test.pdf file")
        print("   3. View the scrambled and original images in preview")
        print("   4. Login as admin to manage papers")
        print("   5. Login as exam center to download papers")
        
        subprocess.run(['npm', 'run', 'dev'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting frontend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Shutting down frontend server...")
        return True

def main():
    print("🚀 EduSecure Complete System Startup")
    print("=" * 50)
    
    # Create test files
    create_test_files()
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Cannot start system without backend")
        return
    
    try:
        # Test system
        if test_system():
            print("\n✅ System is ready!")
            
            # Start frontend
            start_frontend()
        else:
            print("\n❌ System test failed. Check the backend logs.")
            
    except KeyboardInterrupt:
        print("\n👋 Shutting down system...")
    finally:
        # Clean up backend process
        if backend_process:
            print("🔧 Stopping backend server...")
            backend_process.terminate()
            backend_process.wait()

if __name__ == "__main__":
    main()