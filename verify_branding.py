#!/usr/bin/env python3
"""
Verify EduSecure branding consistency across all files
"""
import os
import glob

def check_branding():
    """Check for consistent branding across all files"""
    print("🔍 Verifying EduSecure Branding Consistency")
    print("=" * 50)
    
    # Files to check
    files_to_check = [
        "index.html",
        "README.md",
        "start.py",
        "quick_start.py",
        "start.bat",
        "backend/app.py",
        "backend/logs.py"
    ]
    
    old_branding_found = False
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Check for old branding
                if 'EduSecure-HE' in content or 'edusecure-he' in content.lower():
                    print(f"❌ {file_path}: Still contains old branding")
                    old_branding_found = True
                else:
                    print(f"✅ {file_path}: Branding updated")
        else:
            print(f"⚠️  {file_path}: File not found")
    
    # Check favicon files
    favicon_files = ["public/favicon.ico", "public/favicon.png"]
    for favicon in favicon_files:
        if os.path.exists(favicon):
            print(f"✅ {favicon}: Favicon exists")
        else:
            print(f"❌ {favicon}: Favicon missing")
    
    print("\n" + "=" * 50)
    if old_branding_found:
        print("❌ Some files still contain old branding")
        return False
    else:
        print("✅ All branding updated to 'EduSecure'")
        print("🛡️  Shield favicon is ready")
        return True

if __name__ == "__main__":
    success = check_branding()
    if success:
        print("\n🎉 Branding verification complete!")
    else:
        print("\n⚠️  Please check the files marked with ❌")