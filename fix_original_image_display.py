#!/usr/bin/env python3
"""
Comprehensive fix for original image display issues
"""
import requests
import json
import os
import time

BASE_URL = 'http://localhost:5000'

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f'{BASE_URL}/api/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def login_as_faculty():
    """Login as faculty to upload a test exam"""
    try:
        response = requests.post(f'{BASE_URL}/api/login', 
                               json={'username': 'faculty1', 'password': 'faculty123'},
                               timeout=10)
        
        if response.status_code == 200:
            print("✅ Faculty login successful")
            return response.cookies
        else:
            print(f"❌ Faculty login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Faculty login error: {e}")
        return None

def login_as_exam_center():
    """Login as exam center user"""
    try:
        response = requests.post(f'{BASE_URL}/api/login', 
                               json={'username': 'center1', 'password': 'center123'},
                               timeout=10)
        
        if response.status_code == 200:
            print("✅ Exam center login successful")
            return response.cookies
        else:
            print(f"❌ Exam center login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Exam center login error: {e}")
        return None

def upload_test_exam(faculty_cookies):
    """Upload a test exam to ensure we have data"""
    try:
        if not os.path.exists('test.pdf'):
            print("📄 Creating test PDF...")
            os.system('python create_test_pdf.py')
        
        exam_id = f'image_test_{int(time.time())}'
        
        with open('test.pdf', 'rb') as f:
            files = {'file': f}
            data = {
                'exam_id': exam_id,
                'scheduled_time': '2025-01-22T10:00:00'
            }
            
            print(f"📤 Uploading test exam: {exam_id}")
            response = requests.post(f'{BASE_URL}/api/faculty/upload', 
                                   files=files, 
                                   data=data, 
                                   cookies=faculty_cookies,
                                   timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✅ Test exam uploaded: {exam_id}")
                    return exam_id
                else:
                    print(f"❌ Upload failed: {result.get('error')}")
                    return None
            else:
                print(f"❌ Upload failed with status {response.status_code}")
                return None
                
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def test_image_endpoints(exam_center_cookies, exam_id):
    """Test both scrambled and original image endpoints"""
    print(f"\n🖼️  Testing image endpoints for: {exam_id}")
    
    # Test preview info
    try:
        response = requests.get(f'{BASE_URL}/api/preview/info/{exam_id}', 
                               cookies=exam_center_cookies, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Preview info: {data.get('total_pages', 0)} pages available")
            
            if data.get('total_pages', 0) > 0:
                # Test scrambled image
                response = requests.get(f'{BASE_URL}/api/preview/scrambled/{exam_id}/1', 
                                       cookies=exam_center_cookies, timeout=10)
                if response.status_code == 200:
                    print(f"✅ Scrambled image: {len(response.content)} bytes")
                else:
                    print(f"❌ Scrambled image failed: {response.status_code}")
                
                # Test original image
                response = requests.get(f'{BASE_URL}/api/preview/original/{exam_id}/1', 
                                       cookies=exam_center_cookies, timeout=10)
                if response.status_code == 200:
                    print(f"✅ Original image: {len(response.content)} bytes")
                    return True
                else:
                    print(f"❌ Original image failed: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data.get('error')}")
                    except:
                        print(f"   Raw response: {response.text}")
                    return False
            else:
                print("❌ No pages available")
                return False
        else:
            print(f"❌ Preview info failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Image test error: {e}")
        return False

def check_file_system(exam_id):
    """Check if files exist on the file system"""
    print(f"\n📁 Checking file system for: {exam_id}")
    
    exam_dir = f"papers/{exam_id}"
    if os.path.exists(exam_dir):
        print(f"✅ Exam directory exists: {exam_dir}")
        
        # Check temp directory
        temp_dir = f"{exam_dir}/temp"
        if os.path.exists(temp_dir):
            temp_files = os.listdir(temp_dir)
            original_images = [f for f in temp_files if f.startswith('page_') and f.endswith('.png')]
            print(f"✅ Original images in temp: {len(original_images)} files")
            
            if original_images:
                # Check first image
                first_image = os.path.join(temp_dir, 'page_1.png')
                if os.path.exists(first_image):
                    size = os.path.getsize(first_image)
                    print(f"✅ First original image: {size} bytes")
                    return True
                else:
                    print("❌ First original image not found")
                    return False
            else:
                print("❌ No original images found in temp directory")
                return False
        else:
            print(f"❌ Temp directory not found: {temp_dir}")
            return False
    else:
        print(f"❌ Exam directory not found: {exam_dir}")
        return False

def main():
    print("🔧 Fixing Original Image Display Issues")
    print("=" * 50)
    
    # Check backend
    if not check_backend():
        print("❌ Backend is not running. Please start it first:")
        print("   python run_backend.py")
        return
    
    # Login as faculty and upload test exam
    faculty_cookies = login_as_faculty()
    if not faculty_cookies:
        return
    
    exam_id = upload_test_exam(faculty_cookies)
    if not exam_id:
        print("❌ Failed to upload test exam")
        return
    
    # Wait for processing
    time.sleep(2)
    
    # Check file system
    if not check_file_system(exam_id):
        print("❌ File system check failed")
        return
    
    # Login as exam center and test access
    exam_center_cookies = login_as_exam_center()
    if not exam_center_cookies:
        return
    
    # Test image endpoints
    if test_image_endpoints(exam_center_cookies, exam_id):
        print("\n🎉 SUCCESS! Original image access is working!")
        print("\n📋 Next steps:")
        print("1. Open the frontend: http://localhost:5173")
        print("2. Login as center1 / center123")
        print("3. Find the uploaded exam paper")
        print("4. Click 'Simulate Unlock' if needed")
        print("5. Click 'Show Original' in the preview")
        print("6. The original image should now display in the green box")
    else:
        print("\n❌ Original image access is still not working")
        print("Check the backend logs for more details")

if __name__ == "__main__":
    main()