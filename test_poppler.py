#!/usr/bin/env python3
"""
Test poppler integration
"""
import os
import sys
sys.path.append('backend')

from upload import convert_pdf_to_images

def test_poppler():
    """Test if poppler is working with our upload function"""
    print("Testing poppler integration...")
    
    # Find a test PDF
    test_pdf = None
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pdf'):
                test_pdf = os.path.join(root, file)
                break
        if test_pdf:
            break
    
    if not test_pdf:
        print("No PDF file found for testing")
        return False
    
    print(f"Testing with PDF: {test_pdf}")
    
    # Create temp output directory
    output_dir = 'temp_test'
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Test conversion
        images, error = convert_pdf_to_images(test_pdf, output_dir)
        
        if error:
            print(f"✗ Conversion failed: {error}")
            return False
        
        if images:
            print(f"✓ Conversion successful! Generated {len(images)} images:")
            for img in images:
                print(f"  - {img}")
            return True
        else:
            print("✗ No images generated")
            return False
            
    except Exception as e:
        print(f"✗ Exception during conversion: {e}")
        return False
    
    finally:
        # Clean up
        import shutil
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

if __name__ == "__main__":
    success = test_poppler()
    if success:
        print("\n✓ Poppler is working correctly!")
        print("You can now upload PDF files successfully.")
    else:
        print("\n✗ Poppler test failed.")
        print("Please check the installation and try again.")