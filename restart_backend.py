#!/usr/bin/env python3
"""
Restart the backend server with updated configuration
"""
import os
import sys
import subprocess
import time

def restart_backend():
    """Restart the Flask backend"""
    print("Restarting EduSecure Backend...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.getcwd(), 'backend')
    
    # Set environment variable for poppler path
    poppler_path = os.path.join(os.getcwd(), 'poppler')
    if os.path.exists(poppler_path):
        for root, dirs, files in os.walk(poppler_path):
            if 'pdftoppm.exe' in files:
                os.environ['PATH'] = root + os.pathsep + os.environ.get('PATH', '')
                print(f"Added poppler to PATH: {root}")
                break
    
    # Start the backend
    try:
        print("Starting Flask backend...")
        os.chdir(backend_dir)
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\nBackend stopped by user")
    except Exception as e:
        print(f"Error starting backend: {e}")

if __name__ == "__main__":
    restart_backend()