#!/usr/bin/env python3
"""
Debug script to test the upload process directly
"""
import requests
import json
import os

BASE_URL = 'http://localhost:5000'

def test_login():
    """Test login functionality"""
    print("Testing login...")
    
    # Test faculty login
    response = requests.post(f'{BASE_URL}/api/login', json={
        'username': 'faculty1',
        'password': 'faculty123'
    })
    
    if response.status_code == 200:
        print("✓ Faculty login successful")
        return response.cookies
    else:
        print(f"✗ Faculty login failed: {response.text}")
        return None

def test_upload(cookies):
    """Test upload functionality"""
    print("Testing upload...")
    
    # Find a PDF file to test with
    test_files = ['test.pdf', 'sample.pdf', 'exam.pdf']
    test_file = None
    
    for filename in test_files:
        if os.path.exists(filename):
            test_file = filename
            break
    
    if not test_file:
        print("No test PDF file found. Please create a test.pdf file.")
        return False
    
    print(f"Using test file: {test_file}")
    
    # Upload the file
    with open(test_file, 'rb') as f:
        files = {'file': f}
        data = {
            'exam_id': 'test_upload_debug',
            'scheduled_time': '2025-01-20T10:00:00'
        }
        
        response = requests.post(f'{BASE_URL}/api/faculty/upload', 
                               files=files, 
                               data=data, 
                               cookies=cookies)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Upload successful: {json.dumps(result, indent=2)}")
        return True
    else:
        print(f"✗ Upload failed: {response.status_code} - {response.text}")
        return False

def test_preview_info(cookies, exam_id):
    """Test preview info endpoint"""
    print(f"Testing preview info for exam: {exam_id}")
    
    response = requests.get(f'{BASE_URL}/api/preview/info/{exam_id}', cookies=cookies)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Preview info retrieved: {json.dumps(data, indent=2)}")
        return data
    else:
        print(f"✗ Preview info failed: {response.text}")
        return None

def main():
    print("EduSecure Upload Debug Test")
    print("=" * 40)
    
    # Test login
    cookies = test_login()
    if not cookies:
        print("Cannot proceed without login")
        return
    
    print()
    
    # Test upload
    if test_upload(cookies):
        print()
        # Test preview info
        test_preview_info(cookies, 'test_upload_debug')

if __name__ == "__main__":
    main()