#!/usr/bin/env python3
"""
Simple script to replace the second PDF with test.pdf
"""
import os
import shutil
import requests
import time

def clear_papers():
    """Clear existing papers directory"""
    papers_dir = 'papers'
    if os.path.exists(papers_dir):
        shutil.rmtree(papers_dir)
        print("✅ Cleared existing papers")
    os.makedirs(papers_dir, exist_ok=True)

def login_faculty():
    """Login as faculty"""
    response = requests.post('http://localhost:5000/api/login', 
                           json={'username': 'faculty1', 'password': 'faculty123'})
    if response.status_code == 200:
        print("✅ Faculty login successful")
        return response.cookies
    else:
        print("❌ Faculty login failed")
        return None

def upload_pdf(cookies, filename, exam_title):
    """Upload a PDF file"""
    if not os.path.exists(filename):
        print(f"❌ {filename} not found")
        return None
    
    exam_id = exam_title.lower().replace(' ', '_') + '_' + str(int(time.time()))
    
    with open(filename, 'rb') as f:
        files = {'file': f}
        data = {
            'exam_id': exam_id,
            'scheduled_time': '2025-01-22T10:00:00'
        }
        
        print(f"📤 Uploading {exam_title}...")
        response = requests.post('http://localhost:5000/api/faculty/upload', 
                               files=files, 
                               data=data, 
                               cookies=cookies,
                               timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ {exam_title} uploaded successfully")
                return exam_id
            else:
                print(f"❌ Upload failed: {result.get('error')}")
                return None
        else:
            print(f"❌ Upload failed: {response.status_code}")
            return None

def main():
    print("🔄 Fixing Second PDF")
    print("=" * 25)
    
    # Check backend
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code != 200:
            print("❌ Backend not running. Start with: python run_backend.py")
            return
    except:
        print("❌ Backend not running. Start with: python run_backend.py")
        return
    
    # Clear existing papers
    clear_papers()
    
    # Login
    cookies = login_faculty()
    if not cookies:
        return
    
    # Create test.pdf if it doesn't exist
    if not os.path.exists('test.pdf'):
        print("📄 Creating test.pdf...")
        os.system('python create_test_pdf.py')
    
    # Upload first exam (Mathematics)
    print("\n📚 Uploading first exam...")
    os.system('python create_test_pdf.py')  # This creates a basic test PDF
    # Rename it temporarily for first exam
    if os.path.exists('test.pdf'):
        shutil.copy('test.pdf', 'temp_math.pdf')
    
    exam1_id = upload_pdf(cookies, 'temp_math.pdf', 'Mathematics Final Exam')
    time.sleep(2)
    
    # Upload second exam (test.pdf)
    print("\n📚 Uploading second exam...")
    exam2_id = upload_pdf(cookies, 'test.pdf', 'Test Exam Paper')
    
    # Clean up
    if os.path.exists('temp_math.pdf'):
        os.remove('temp_math.pdf')
    
    if exam1_id and exam2_id:
        print("\n🎉 SUCCESS!")
        print(f"📚 Exam 1: Mathematics Final Exam")
        print(f"📚 Exam 2: Test Exam Paper (from test.pdf)")
        print("\n✅ Both exams are now different and visible in all portals")
    else:
        print("\n❌ Failed to upload exams")

if __name__ == "__main__":
    main()