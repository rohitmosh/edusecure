#!/usr/bin/env python3
"""
Simple backend runner for testing
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, 'backend')

# Change to project root directory
if os.path.basename(os.getcwd()) == 'backend':
    os.chdir('..')

# Import and run the app
from backend.app import app

if __name__ == '__main__':
    print("Starting EduSecure Backend Server...")
    print(f"Working directory: {os.getcwd()}")
    print(f"Upload folder: {os.path.abspath('papers')}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)