#!/usr/bin/env python3
"""
Create sample exam papers for demonstration
"""
import requests
import json
import os
import time
from PIL import Image, ImageDraw, ImageFont

def create_sample_pdf(filename, title, questions):
    """Create a sample PDF with exam content"""
    try:
        # Create multiple pages
        images = []
        width, height = 800, 600
        
        for page_num, question_set in enumerate(questions, 1):
            # Create a white background
            img = Image.new('RGB', (width, height), 'white')
            draw = ImageDraw.Draw(img)
            
            # Try to use a default font
            try:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            except:
                font_large = None
                font_small = None
            
            # Draw page content
            draw.rectangle([50, 50, width-50, height-50], outline='black', width=2)
            
            # Add header
            header_text = f"{title} - Page {page_num}"
            if font_large:
                draw.text((100, 80), header_text, fill='black', font=font_large)
            else:
                draw.text((100, 80), header_text, fill='black')
            
            # Add content
            y_pos = 130
            for line in question_set:
                if font_small:
                    draw.text((100, y_pos), line, fill='black', font=font_small)
                else:
                    draw.text((100, y_pos), line, fill='black')
                y_pos += 25
            
            # Add footer
            footer_text = f"Confidential Exam Material - Page {page_num}"
            if font_small:
                draw.text((100, height-100), footer_text, fill='gray', font=font_small)
            else:
                draw.text((100, height-100), footer_text, fill='gray')
            
            images.append(img)
        
        # Save as PDF
        if images:
            images[0].save(filename, save_all=True, append_images=images[1:])
            print(f"✅ Created {filename}")
            return True
        else:
            print(f"❌ Failed to create {filename}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating {filename}: {e}")
        return False

def login_as_faculty():
    """Login as faculty user"""
    try:
        response = requests.post('http://localhost:5000/api/login', 
                               json={'username': 'faculty1', 'password': 'faculty123'},
                               timeout=10)
        
        if response.status_code == 200:
            print("✅ Faculty login successful")
            return response.cookies
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def upload_exam(cookies, filename, exam_title):
    """Upload an exam paper"""
    try:
        exam_id = exam_title.lower().replace(' ', '_') + '_' + str(int(time.time()))
        
        with open(filename, 'rb') as f:
            files = {'file': f}
            data = {
                'exam_id': exam_id,
                'scheduled_time': '2025-01-22T10:00:00'
            }
            
            print(f"📤 Uploading {exam_title}...")
            response = requests.post('http://localhost:5000/api/faculty/upload', 
                                   files=files, 
                                   data=data, 
                                   cookies=cookies,
                                   timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✅ {exam_title} uploaded successfully!")
                    print(f"   📊 Pages: {result.get('total_pages', 'N/A')}")
                    return exam_id
                else:
                    print(f"❌ Upload failed: {result.get('error', 'Unknown error')}")
                    return None
            else:
                print(f"❌ Upload failed with status {response.status_code}")
                return None
                
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def main():
    print("📚 Creating Sample Exam Papers")
    print("=" * 40)
    
    # Create sample exam papers
    exam1_questions = [
        [
            "MATHEMATICS FINAL EXAMINATION",
            "",
            "Instructions: Answer all questions. Show your work.",
            "",
            "Question 1: Solve for x in the equation 2x + 5 = 15",
            "A) x = 5    B) x = 10    C) x = 7.5    D) x = 2.5",
            "",
            "Question 2: What is the derivative of f(x) = x² + 3x?",
            "A) 2x + 3    B) x + 3    C) 2x    D) x²",
            "",
            "Question 3: Calculate the area of a circle with radius 4 cm",
            "A) 16π cm²    B) 8π cm²    C) 4π cm²    D) 12π cm²"
        ],
        [
            "MATHEMATICS FINAL EXAMINATION - Page 2",
            "",
            "Question 4: Solve the system of equations:",
            "2x + y = 7",
            "x - y = 2",
            "",
            "A) x=3, y=1    B) x=2, y=3    C) x=1, y=5    D) x=4, y=-1",
            "",
            "Question 5: What is the integral of 2x dx?",
            "A) x² + C    B) 2x² + C    C) x²/2 + C    D) 2x + C",
            "",
            "Question 6: Find the slope of the line passing through",
            "points (2,3) and (4,7)",
            "A) 2    B) 1    C) 4    D) 3"
        ]
    ]
    
    exam2_questions = [
        [
            "COMPUTER SCIENCE MIDTERM EXAM",
            "",
            "Instructions: Choose the best answer for each question.",
            "",
            "Question 1: Which data structure uses LIFO principle?",
            "A) Queue    B) Stack    C) Array    D) Linked List",
            "",
            "Question 2: What is the time complexity of binary search?",
            "A) O(n)    B) O(log n)    C) O(n²)    D) O(1)",
            "",
            "Question 3: Which sorting algorithm has O(n log n) complexity?",
            "A) Bubble Sort    B) Selection Sort    C) Merge Sort    D) Insertion Sort"
        ],
        [
            "COMPUTER SCIENCE MIDTERM EXAM - Page 2",
            "",
            "Question 4: What does SQL stand for?",
            "A) Structured Query Language",
            "B) Simple Query Language", 
            "C) Standard Query Language",
            "D) Sequential Query Language",
            "",
            "Question 5: Which is NOT a programming paradigm?",
            "A) Object-Oriented    B) Functional    C) Procedural    D) Alphabetical",
            "",
            "Question 6: What is the purpose of a constructor in OOP?",
            "A) Destroy objects    B) Initialize objects",
            "C) Copy objects    D) Compare objects"
        ]
    ]
    
    # Create first PDF file
    pdf1_created = create_sample_pdf('math_final_exam.pdf', 'Mathematics Final Exam', exam1_questions)
    
    # Check if test.pdf exists for second exam
    pdf2_exists = os.path.exists('test.pdf')
    
    if not pdf1_created:
        print("❌ Failed to create Mathematics Final Exam PDF")
        return
    
    if not pdf2_exists:
        print("❌ test.pdf not found. Creating it...")
        # Create test.pdf if it doesn't exist
        import subprocess
        try:
            subprocess.run(['python', 'create_test_pdf.py'], check=True, timeout=30)
            pdf2_exists = os.path.exists('test.pdf')
            if pdf2_exists:
                print("✅ Created test.pdf")
            else:
                print("❌ Failed to create test.pdf")
                return
        except:
            print("❌ Failed to create test.pdf")
            return
    
    # Check if backend is running
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code != 200:
            print("❌ Backend server is not running. Please start it first:")
            print("   python run_backend.py")
            return
    except:
        print("❌ Cannot connect to backend server. Please start it first:")
        print("   python run_backend.py")
        return
    
    # Login and upload exams
    cookies = login_as_faculty()
    if not cookies:
        print("❌ Cannot login as faculty")
        return
    
    # Upload both exams
    exam1_id = upload_exam(cookies, 'math_final_exam.pdf', 'Mathematics Final Exam')
    time.sleep(2)  # Wait between uploads
    exam2_id = upload_exam(cookies, 'test.pdf', 'Test Exam Paper')
    
    if exam1_id and exam2_id:
        print("\n🎉 Sample exams created successfully!")
        print(f"📚 Exam 1: {exam1_id}")
        print(f"📚 Exam 2: {exam2_id}")
        print("\n🎯 Now you can:")
        print("1. Login to the Exam Center portal")
        print("2. View both exam papers")
        print("3. Use 'Simulate Unlock' to demonstrate key release")
        print("4. Download both scrambled and original versions")
    else:
        print("❌ Failed to upload some exams")
    
    # Clean up temporary PDF files (keep test.pdf)
    try:
        os.remove('math_final_exam.pdf')
        print("🧹 Cleaned up temporary PDF files (kept test.pdf)")
    except:
        pass

if __name__ == "__main__":
    main()