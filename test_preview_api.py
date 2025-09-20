#!/usr/bin/env python3
"""
Test script to verify the preview API endpoints are working
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_login():
    """Test login functionality"""
    print("Testing login...")
    
    # Test admin login
    response = requests.post(f'{BASE_URL}/api/login', json={
        'username': 'admin1',
        'password': 'admin123'
    })
    
    if response.status_code == 200:
        print("✓ Admin login successful")
        return response.cookies
    else:
        print(f"✗ Admin login failed: {response.text}")
        return None

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

def test_preview_images(cookies, exam_id, page=1):
    """Test preview image endpoints"""
    print(f"Testing preview images for exam: {exam_id}, page: {page}")
    
    # Test scrambled image
    response = requests.get(f'{BASE_URL}/api/preview/scrambled/{exam_id}/{page}', cookies=cookies)
    if response.status_code == 200:
        print(f"✓ Scrambled image available (size: {len(response.content)} bytes)")
    else:
        print(f"✗ Scrambled image failed: {response.status_code} - {response.text}")
    
    # Test original image
    response = requests.get(f'{BASE_URL}/api/preview/original/{exam_id}/{page}', cookies=cookies)
    if response.status_code == 200:
        print(f"✓ Original image available (size: {len(response.content)} bytes)")
    else:
        print(f"✗ Original image failed: {response.status_code} - {response.text}")

def main():
    print("EduSecure Preview API Test")
    print("=" * 40)
    
    # Test login
    cookies = test_login()
    if not cookies:
        print("Cannot proceed without login")
        return
    
    print()
    
    # List available exams
    print("Getting available exams...")
    response = requests.get(f'{BASE_URL}/api/admin/papers', cookies=cookies)
    if response.status_code == 200:
        papers = response.json().get('papers', [])
        print(f"Found {len(papers)} papers")
        
        if papers:
            exam_id = papers[0]['exam_id']
            print(f"Testing with exam: {exam_id}")
            print()
            
            # Test preview info
            preview_info = test_preview_info(cookies, exam_id)
            print()
            
            # Test preview images
            if preview_info and preview_info.get('total_pages', 0) > 0:
                test_preview_images(cookies, exam_id, 1)
            else:
                print("No pages available for preview")
        else:
            print("No papers found. Upload a paper first.")
    else:
        print(f"Failed to get papers: {response.text}")

if __name__ == "__main__":
    main()