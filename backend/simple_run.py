#!/usr/bin/env python3
"""
Simple EduSecure Backend Server
Runs without strict dependency checking
"""

import os
import sys

def setup_directories():
    """Create necessary directories"""
    directories = [
        '../papers',
        '../users', 
        '../logs',
        '../config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directory created/verified: {directory}")

def main():
    """Main function to start the server"""
    print("🔐 EduSecure Backend Server (Simple Mode)")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    # Start the Flask server
    print("\n🚀 Starting Flask server...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\n💡 Try installing missing dependencies:")
        print("   pip install Flask Flask-CORS Flask-Login")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()