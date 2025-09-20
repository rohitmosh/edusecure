#!/usr/bin/env python3
"""
Refresh demo data with correct PDFs
"""
import os
import shutil
import requests
import time

def clear_existing_papers():
    """Clear existing papers directory"""
    papers_dir = 'papers'
    if os.path.exists(papers_dir):
        try:
            shutil.rmtree(papers_dir)
            print("✅ Cleared existing papers directory")
        except Exception as e:
            print(f"⚠️  Could not clear papers directory: {e}")
    
    # Recreate empty papers directory
    os.makedirs(papers_dir, exist_ok=True)

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🔄 Refreshing Demo Data")
    print("=" * 30)
    
    # Check backend
    if not check_backend():
        print("❌ Backend server is not running. Please start it first:")
        print("   python run_backend.py")
        return
    
    # Clear existing data
    print("🧹 Clearing existing exam papers...")
    clear_existing_papers()
    
    # Wait a moment
    time.sleep(1)
    
    # Create fresh sample exams
    print("📚 Creating fresh sample exams...")
    try:
        import subprocess
        result = subprocess.run(['python', 'create_sample_exams.py'], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Fresh demo data created successfully!")
            print("\n📋 Demo now includes:")
            print("1. Mathematics Final Exam (custom created)")
            print("2. Test Exam Paper (from test.pdf)")
            print("\n🎯 Ready for demonstration!")
        else:
            print("❌ Failed to create sample exams")
            print(result.stdout)
            print(result.stderr)
    
    except Exception as e:
        print(f"❌ Error creating sample exams: {e}")

if __name__ == "__main__":
    main()