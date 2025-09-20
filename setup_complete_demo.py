#!/usr/bin/env python3
"""
Complete demo setup script for EduSecure system
"""
import subprocess
import sys
import time
import requests
import os

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ {description} timed out")
        return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🚀 EduSecure Complete Demo Setup")
    print("=" * 50)
    
    # Step 1: Create test PDFs
    print("\n📚 Step 1: Creating test PDF files")
    if not run_command(f"{sys.executable} create_test_pdf.py", "Creating basic test PDF"):
        print("⚠️  Continuing without basic test PDF...")
    
    # Step 2: Check if backend is running
    print("\n🔧 Step 2: Checking backend server")
    if not check_backend():
        print("❌ Backend server is not running!")
        print("Please start the backend server first:")
        print("   python run_backend.py")
        print("\nThen run this script again.")
        return False
    else:
        print("✅ Backend server is running")
    
    # Step 3: Create sample exam papers
    print("\n📝 Step 3: Creating sample exam papers")
    if not run_command(f"{sys.executable} create_sample_exams.py", "Creating sample exams"):
        print("⚠️  Sample exams creation failed, but continuing...")
    
    # Step 4: Test the complete system
    print("\n🧪 Step 4: Testing system integration")
    if not run_command(f"{sys.executable} test_frontend_integration.py", "Testing system integration"):
        print("⚠️  Some tests failed, but system should still work")
    
    print("\n🎉 Demo Setup Complete!")
    print("\n" + "=" * 50)
    print("🎯 DEMO INSTRUCTIONS")
    print("=" * 50)
    
    print("\n1. 📱 START FRONTEND:")
    print("   npm run dev")
    print("   Open: http://localhost:5173")
    
    print("\n2. 👥 LOGIN CREDENTIALS:")
    print("   Faculty:     faculty1  / faculty123")
    print("   Admin:       admin1    / admin123")
    print("   Exam Center: center1   / center123")
    
    print("\n3. 📚 FACULTY DEMO:")
    print("   • Login as faculty1")
    print("   • Upload test.pdf or any PDF file")
    print("   • Watch real-time processing")
    print("   • View scrambled vs original images")
    
    print("\n4. 🏢 EXAM CENTER DEMO:")
    print("   • Login as center1")
    print("   • View 2+ exam papers")
    print("   • Click 'Simulate Unlock' for demo")
    print("   • Download scrambled images")
    print("   • Download original images (after unlock)")
    print("   • View real image previews")
    
    print("\n5. 👑 ADMIN DEMO:")
    print("   • Login as admin1")
    print("   • View all uploaded papers")
    print("   • Release chaos keys")
    print("   • Verify paper integrity")
    print("   • View audit logs")
    
    print("\n6. 🔄 REAL-TIME UPDATES:")
    print("   • Upload from Faculty → Updates in Admin & Exam Center")
    print("   • Key release from Admin → Updates in Exam Center")
    print("   • All portals sync automatically")
    
    print("\n" + "=" * 50)
    print("🎬 Ready for demonstration!")
    print("=" * 50)

if __name__ == "__main__":
    main()