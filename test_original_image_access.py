#!/usr/bin/env python3
"""
Test script to verify original image access for exam center users
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_exam_center_login():
    """Test exam center login"""
    try:
        response = requests.post(f'{BASE_URL}/api/login', 
                               json={'username': 'center1', 'password': 'center123'},
                               timeout=10)
        
        if response.status_code == 200:
            print("✅ Exam center login successful")
            return response.cookies
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_original_image_access(cookies):
    """Test access to original images"""
    try:
        # First get list of available papers
        response = requests.get(f'{BASE_URL}/api/examcenter/papers', 
                               cookies=cookies, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            papers = data.get('papers', [])
            
            if papers:
                exam_id = papers[0]['exam_id']
                print(f"📄 Testing with exam: {exam_id}")
                
                # Test original image access
                response = requests.get(f'{BASE_URL}/api/preview/original/{exam_id}/1', 
                                       cookies=cookies, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Original image accessible: {len(response.content)} bytes")
                    return True
                else:
                    print(f"❌ Original image access failed: {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   Error: {error_data.get('error', 'Unknown error')}")
                    except:
                        print(f"   Raw response: {response.text}")
                    return False
            else:
                print("❌ No papers available for testing")
                return False
        else:
            print(f"❌ Failed to get papers: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    print("🔍 Testing Original Image Access for Exam Center")
    print("=" * 50)
    
    # Test login
    cookies = test_exam_center_login()
    if not cookies:
        print("❌ Cannot proceed without login")
        return
    
    # Test original image access
    if test_original_image_access(cookies):
        print("\n✅ Original image access is working!")
        print("The 'Show Original' button should now work in the frontend.")
    else:
        print("\n❌ Original image access is still blocked.")
        print("Check backend logs for more details.")

if __name__ == "__main__":
    main()