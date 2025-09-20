#!/usr/bin/env python3
"""
Complete workflow test for upload and preview functionality
"""
import requests
import json
import os
import time

BASE_URL = 'http://localhost:5000'

def test_login():
    """Test login functionality"""
    print("🔐 Testing login...")
    
    # Test faculty login
    response = requests.post(f'{BASE_URL}/api/login', json={
        'username': 'faculty1',
        'password': 'faculty123'
    })
    
    if response.status_code == 200:
        print("✅ Faculty login successful")
        return response.cookies
    else:
        print(f"❌ Faculty login failed: {response.text}")
        return None

def test_upload(cookies):
    """Test upload functionality"""
    print("📤 Testing upload...")
    
    if not os.path.exists('test.pdf'):
        print("❌ test.pdf not found. Please run create_test_pdf.py first.")
        return False
    
    print("📄 Using test.pdf")
    
    # Upload the file
    with open('test.pdf', 'rb') as f:
        files = {'file': f}
        data = {
            'exam_id': 'workflow_test',
            'scheduled_time': '2025-01-20T10:00:00'
        }
        
        print("⏳ Uploading file...")
        response = requests.post(f'{BASE_URL}/api/faculty/upload', 
                               files=files, 
                               data=data, 
                               cookies=cookies)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Upload successful!")
        print(f"   📊 Total pages: {result.get('total_pages', 'N/A')}")
        print(f"   🔒 Scrambled images: {result.get('scrambled_images', 'N/A')}")
        return True
    else:
        print(f"❌ Upload failed: {response.status_code}")
        try:
            error_data = response.json()
            print(f"   Error: {error_data.get('error', 'Unknown error')}")
        except:
            print(f"   Raw response: {response.text}")
        return False

def test_preview_info(cookies, exam_id):
    """Test preview info endpoint"""
    print(f"📋 Testing preview info for exam: {exam_id}")
    
    response = requests.get(f'{BASE_URL}/api/preview/info/{exam_id}', cookies=cookies)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Preview info retrieved!")
        print(f"   📄 Total pages: {data.get('total_pages', 0)}")
        print(f"   🔒 Scrambled pages: {len(data.get('scrambled_pages', []))}")
        print(f"   📖 Original pages: {len(data.get('original_pages', []))}")
        return data
    else:
        print(f"❌ Preview info failed: {response.status_code}")
        try:
            error_data = response.json()
            print(f"   Error: {error_data.get('error', 'Unknown error')}")
        except:
            print(f"   Raw response: {response.text}")
        return None

def test_preview_images(cookies, exam_id, page=1):
    """Test preview image endpoints"""
    print(f"🖼️  Testing preview images for exam: {exam_id}, page: {page}")
    
    # Test scrambled image
    print("   🔒 Testing scrambled image...")
    response = requests.get(f'{BASE_URL}/api/preview/scrambled/{exam_id}/{page}', cookies=cookies)
    if response.status_code == 200:
        print(f"   ✅ Scrambled image available ({len(response.content)} bytes)")
    else:
        print(f"   ❌ Scrambled image failed: {response.status_code}")
        try:
            error_data = response.json()
            print(f"      Error: {error_data.get('error', 'Unknown error')}")
        except:
            print(f"      Raw response: {response.text[:100]}...")
    
    # Test original image
    print("   📖 Testing original image...")
    response = requests.get(f'{BASE_URL}/api/preview/original/{exam_id}/{page}', cookies=cookies)
    if response.status_code == 200:
        print(f"   ✅ Original image available ({len(response.content)} bytes)")
    else:
        print(f"   ❌ Original image failed: {response.status_code}")
        try:
            error_data = response.json()
            print(f"      Error: {error_data.get('error', 'Unknown error')}")
        except:
            print(f"      Raw response: {response.text[:100]}...")

def check_file_system(exam_id):
    """Check the file system for uploaded files"""
    print(f"📁 Checking file system for exam: {exam_id}")
    
    exam_dir = f"papers/{exam_id}"
    if os.path.exists(exam_dir):
        print(f"   ✅ Exam directory exists: {exam_dir}")
        
        # Check for scrambled images
        scrambled_files = [f for f in os.listdir(exam_dir) if f.startswith('scrambled_page_')]
        print(f"   🔒 Scrambled files: {len(scrambled_files)}")
        
        # Check for temp directory with original images
        temp_dir = f"{exam_dir}/temp"
        if os.path.exists(temp_dir):
            original_files = [f for f in os.listdir(temp_dir) if f.startswith('page_')]
            print(f"   📖 Original files: {len(original_files)}")
        else:
            print(f"   ❌ Temp directory not found: {temp_dir}")
        
        # Check for metadata files
        metadata_file = f"{exam_dir}/metadata.json"
        if os.path.exists(metadata_file):
            print(f"   ✅ Metadata file exists")
        else:
            print(f"   ❌ Metadata file missing")
            
        chaos_key_file = f"{exam_dir}/chaos_key.enc"
        if os.path.exists(chaos_key_file):
            print(f"   ✅ Chaos key file exists")
        else:
            print(f"   ❌ Chaos key file missing")
            
    else:
        print(f"   ❌ Exam directory not found: {exam_dir}")

def main():
    print("🚀 EduSecure Complete Workflow Test")
    print("=" * 50)
    
    # Test login
    cookies = test_login()
    if not cookies:
        print("❌ Cannot proceed without login")
        return
    
    print()
    
    # Test upload
    if test_upload(cookies):
        print()
        
        # Wait a moment for file system operations
        time.sleep(1)
        
        # Check file system
        check_file_system('workflow_test')
        print()
        
        # Test preview info
        preview_info = test_preview_info(cookies, 'workflow_test')
        print()
        
        # Test preview images
        if preview_info and preview_info.get('total_pages', 0) > 0:
            test_preview_images(cookies, 'workflow_test', 1)
        else:
            print("❌ No pages available for preview testing")
    else:
        print("❌ Upload failed, skipping preview tests")

if __name__ == "__main__":
    main()