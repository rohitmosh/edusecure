#!/usr/bin/env python3
"""
Install poppler for Windows to enable PDF processing
"""
import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil

def install_poppler_windows():
    """Install poppler for Windows"""
    print("Installing poppler for Windows...")
    
    # Check if running on Windows
    if os.name != 'nt':
        print("This script is for Windows only.")
        return False
    
    try:
        # Create poppler directory
        poppler_dir = os.path.join(os.getcwd(), 'poppler')
        if os.path.exists(poppler_dir):
            print("Poppler directory already exists. Removing...")
            shutil.rmtree(poppler_dir)
        
        os.makedirs(poppler_dir, exist_ok=True)
        
        # Download poppler for Windows
        poppler_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.01.0-0/Release-23.01.0-0.zip"
        zip_path = os.path.join(poppler_dir, "poppler.zip")
        
        print("Downloading poppler...")
        urllib.request.urlretrieve(poppler_url, zip_path)
        
        # Extract poppler
        print("Extracting poppler...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(poppler_dir)
        
        # Find the bin directory
        bin_dir = None
        for root, dirs, files in os.walk(poppler_dir):
            if 'bin' in dirs and 'pdftoppm.exe' in os.listdir(os.path.join(root, 'bin')):
                bin_dir = os.path.join(root, 'bin')
                break
        
        if not bin_dir:
            print("Could not find poppler bin directory")
            return False
        
        # Add to PATH
        current_path = os.environ.get('PATH', '')
        if bin_dir not in current_path:
            os.environ['PATH'] = bin_dir + os.pathsep + current_path
            print(f"Added {bin_dir} to PATH")
        
        # Clean up
        os.remove(zip_path)
        
        print("Poppler installed successfully!")
        print(f"Poppler bin directory: {bin_dir}")
        print("Note: You may need to restart your terminal/IDE for PATH changes to take effect.")
        
        return True
        
    except Exception as e:
        print(f"Error installing poppler: {e}")
        return False

def test_poppler():
    """Test if poppler is working"""
    try:
        result = subprocess.run(['pdftoppm', '-h'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Poppler is working correctly!")
            return True
        else:
            print("✗ Poppler test failed")
            return False
    except FileNotFoundError:
        print("✗ Poppler not found in PATH")
        return False

if __name__ == "__main__":
    print("EduSecure Poppler Installer for Windows")
    print("=" * 50)
    
    # Test if poppler is already installed
    if test_poppler():
        print("Poppler is already installed and working!")
        sys.exit(0)
    
    # Install poppler
    if install_poppler_windows():
        print("\nTesting installation...")
        if test_poppler():
            print("\n✓ Installation successful!")
        else:
            print("\n⚠ Installation completed but poppler test failed.")
            print("You may need to restart your terminal/IDE.")
    else:
        print("\n✗ Installation failed!")
        sys.exit(1)