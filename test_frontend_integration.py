#!/usr/bin/env python3
"""
Test script to verify frontend-backend integration
"""
import requests
import json
import os
import time

BASE_URL = 'http://localhost:5000'

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f'{BASE_URL}/api/health')
        if response.status_code == 200:
            print("✅ Backend server is running")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_login_endpoints():
    """Test all login endpoints"""
    print("\n🔐 Testing Login Endpoints")
    
    users = [
        {'username': 'admin1', 'password': 'admin123', 'role': 'admin'},
        {'username': 'faculty1', 'password': 'faculty123', 'role': 'faculty'},
        {'username': 'center1', 'password': 'center123', 'role': 'exam_center'}
    ]
    
    cookies_dict = {}
    
    for user in users:
        response = requests.post(f'{BASE_URL}/api/login', json={
            'username': user['username'],
            'password': user['password']
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {user['role']} login successful")
            cookies_dict[user['role']] = response.cookies
        else:
            print(f"❌ {user['role']} login failed: {response.text}")
    
    return cookies_dict

def test_faculty_upload(cookies):
    """Test faculty upload functionality"""
    print("\n📤 Testing Faculty Upload")
    
    if 'faculty' not in cookies:
        print("❌ Faculty login required")
        return None
    
    if not os.path.exists('test.pdf'):
        print("❌ test.pdf not found. Creating one...")
        os.system('python create_test_pdf.py')
    
    exam_id = f'frontend_test_{int(time.time())}'
    
    with open('test.pdf', 'rb') as f:
        files = {'file': f}
        data = {
            'exam_id': exam_id,
            'scheduled_time': '2025-01-21T10:00:00'
        }
        
        response = requests.post(f'{BASE_URL}/api/faculty/upload', 
                               files=files, 
                               data=data, 
                               cookies=cookies['faculty'])
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Upload successful: {result.get('message', 'No message')}")
        print(f"   📊 Pages: {result.get('total_pages', 'N/A')}")
        print(f"   🔒 Scrambled: {result.get('scrambled_images', 'N/A')}")
        return exam_id
    else:
        print(f"❌ Upload failed: {response.status_code}")
        try:
            error_data = response.json()
            print(f"   Error: {error_data.get('error', 'Unknown error')}")
        except:
            print(f"   Raw response: {response.text}")
        return None

def test_preview_endpoints(cookies, exam_id):
    """Test preview endpoints"""
    print(f"\n🖼️  Testing Preview Endpoints for {exam_id}")
    
    if 'faculty' not in cookies:
        print("❌ Faculty login required")
        return
    
    # Test preview info
    response = requests.get(f'{BASE_URL}/api/preview/info/{exam_id}', 
                           cookies=cookies['faculty'])
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Preview info: {data.get('total_pages', 0)} pages")
        
        if data.get('total_pages', 0) > 0:
            # Test scrambled image
            response = requests.get(f'{BASE_URL}/api/preview/scrambled/{exam_id}/1', 
                                   cookies=cookies['faculty'])
            if response.status_code == 200:
                print(f"✅ Scrambled image: {len(response.content)} bytes")
            else:
                print(f"❌ Scrambled image failed: {response.status_code}")
            
            # Test original image
            response = requests.get(f'{BASE_URL}/api/preview/original/{exam_id}/1', 
                                   cookies=cookies['faculty'])
            if response.status_code == 200:
                print(f"✅ Original image: {len(response.content)} bytes")
            else:
                print(f"❌ Original image failed: {response.status_code}")
        
    else:
        print(f"❌ Preview info failed: {response.status_code}")

def test_admin_endpoints(cookies, exam_id):
    """Test admin endpoints"""
    print(f"\n👑 Testing Admin Endpoints")
    
    if 'admin' not in cookies:
        print("❌ Admin login required")
        return
    
    # Test get papers
    response = requests.get(f'{BASE_URL}/api/admin/papers', 
                           cookies=cookies['admin'])
    
    if response.status_code == 200:
        data = response.json()
        papers = data.get('papers', [])
        print(f"✅ Admin can see {len(papers)} papers")
        
        # Test integrity verification if exam exists
        if exam_id:
            response = requests.get(f'{BASE_URL}/api/admin/verify_integrity/{exam_id}', 
                                   cookies=cookies['admin'])
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Integrity check: {'PASSED' if result.get('valid') else 'FAILED'}")
            else:
                print(f"❌ Integrity check failed: {response.status_code}")
    else:
        print(f"❌ Admin papers failed: {response.status_code}")

def test_exam_center_endpoints(cookies, exam_id):
    """Test exam center endpoints"""
    print(f"\n🏢 Testing Exam Center Endpoints")
    
    if 'exam_center' not in cookies:
        print("❌ Exam center login required")
        return
    
    # Test get papers
    response = requests.get(f'{BASE_URL}/api/examcenter/papers', 
                           cookies=cookies['exam_center'])
    
    if response.status_code == 200:
        data = response.json()
        papers = data.get('papers', [])
        print(f"✅ Exam center can see {len(papers)} papers")
        
        # Test download if exam exists
        if exam_id:
            response = requests.get(f'{BASE_URL}/api/examcenter/download/{exam_id}', 
                                   cookies=cookies['exam_center'])
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Download successful: {result.get('message', 'No message')}")
            else:
                print(f"❌ Download failed: {response.status_code}")
    else:
        print(f"❌ Exam center papers failed: {response.status_code}")

def main():
    print("🚀 Frontend-Backend Integration Test")
    print("=" * 50)
    
    # Test backend health
    if not test_health():
        print("\n❌ Backend is not running. Please start it first:")
        print("   python run_backend.py")
        return
    
    # Test login endpoints
    cookies = test_login_endpoints()
    if not cookies:
        print("\n❌ No successful logins")
        return
    
    # Test faculty upload
    exam_id = test_faculty_upload(cookies)
    
    # Test preview endpoints
    if exam_id:
        test_preview_endpoints(cookies, exam_id)
        test_admin_endpoints(cookies, exam_id)
        test_exam_center_endpoints(cookies, exam_id)
    
    print("\n🎉 Integration test completed!")
    print("\nTo test the frontend:")
    print("1. Start the React development server: npm run dev")
    print("2. Open http://localhost:5173 in your browser")
    print("3. Login with:")
    print("   - Faculty: faculty1 / faculty123")
    print("   - Admin: admin1 / admin123") 
    print("   - Exam Center: center1 / center123")

if __name__ == "__main__":
    main()