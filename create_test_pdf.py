#!/usr/bin/env python3
"""
Create a simple test PDF file for testing upload
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_pdf():
    """Create a simple test PDF with a few pages"""
    try:
        # Create a simple image with text
        width, height = 800, 600
        
        # Create multiple pages
        images = []
        
        for page_num in range(1, 4):  # Create 3 pages
            # Create a white background
            img = Image.new('RGB', (width, height), 'white')
            draw = ImageDraw.Draw(img)
            
            # Draw some content
            try:
                # Try to use a default font
                font = ImageFont.load_default()
            except:
                font = None
            
            # Draw page content
            draw.rectangle([50, 50, width-50, height-50], outline='black', width=2)
            
            # Add text
            text_lines = [
                f"Test Exam Paper - Page {page_num}",
                "",
                "Question 1: What is the capital of France?",
                "A) London  B) Berlin  C) Paris  D) Madrid",
                "",
                "Question 2: What is 2 + 2?",
                "A) 3  B) 4  C) 5  D) 6",
                "",
                f"This is page {page_num} of the test exam paper.",
                "This PDF is created for testing the upload functionality."
            ]
            
            y_pos = 100
            for line in text_lines:
                if font:
                    draw.text((100, y_pos), line, fill='black', font=font)
                else:
                    draw.text((100, y_pos), line, fill='black')
                y_pos += 30
            
            images.append(img)
        
        # Save as PDF
        if images:
            images[0].save('test.pdf', save_all=True, append_images=images[1:])
            print("✓ Created test.pdf with 3 pages")
            return True
        else:
            print("✗ Failed to create images")
            return False
            
    except Exception as e:
        print(f"✗ Error creating test PDF: {e}")
        return False

if __name__ == "__main__":
    create_test_pdf()