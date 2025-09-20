import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
from pdf2image import convert_from_path
from chaotic import generate_chaos_key, scramble_image, save_encrypted_chaos_key
from hashing import compute_sha256
from phe_wrapper import encrypt_metadata

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_pdf_to_images(pdf_path, output_dir):
    """Convert PDF pages to images using pdf2image"""
    try:
        # Try to find poppler path
        poppler_path = None
        
        # Check if poppler is in the project directory
        project_poppler = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'poppler')
        if os.path.exists(project_poppler):
            for root, dirs, files in os.walk(project_poppler):
                if 'pdftoppm.exe' in files:
                    poppler_path = root
                    break
        
        # Convert PDF to images with poppler path
        if poppler_path:
            pages = convert_from_path(pdf_path, dpi=200, fmt='PNG', poppler_path=poppler_path)
        else:
            # Try without specifying path (in case it's in system PATH)
            pages = convert_from_path(pdf_path, dpi=200, fmt='PNG')
        
        images = []
        for i, page in enumerate(pages):
            image_path = os.path.join(output_dir, f'page_{i + 1}.png')
            page.save(image_path, 'PNG')
            images.append(image_path)
        
        return images, None
        
    except Exception as e:
        return None, f"Error converting PDF: {e}. Make sure poppler is installed by running 'python install_poppler_windows.py' and restart your terminal."

def process_single_image(image_path, output_dir):
    """Process a single image file"""
    try:
        # Copy image to output directory
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)
        
        # Open and save image (ensures consistent format)
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(output_path)
        
        return [output_path], None
        
    except Exception as e:
        return None, f"Error processing image: {e}"

def process_upload(file, exam_id, uploader, scheduled_time, upload_folder):
    """Process uploaded exam paper"""
    try:
        if not file or not allowed_file(file.filename):
            return {'success': False, 'error': 'Invalid file type'}
        
        # Create exam directory
        exam_dir = os.path.join(upload_folder, exam_id)
        os.makedirs(exam_dir, exist_ok=True)
        
        # Create temp directory for original images
        temp_dir = os.path.join(exam_dir, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_file_path = os.path.join(temp_dir, filename)
        file.save(temp_file_path)
        
        # Convert to images based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext == 'pdf':
            original_images, error = convert_pdf_to_images(temp_file_path, temp_dir)
        elif file_ext in ['png', 'jpg', 'jpeg']:
            original_images, error = process_single_image(temp_file_path, temp_dir)
        else:
            return {'success': False, 'error': 'Unsupported file format'}
        
        if error:
            return {'success': False, 'error': error}
        
        # Generate chaos key for scrambling
        chaos_key = generate_chaos_key()
        
        # Scramble each image and compute hashes
        scrambled_images = []
        page_hashes = {}
        
        for i, img_path in enumerate(original_images):
            # Scramble image
            scrambled_path = os.path.join(exam_dir, f'scrambled_page_{i + 1}.png')
            success, message = scramble_image(img_path, chaos_key, scrambled_path)
            
            if not success:
                return {'success': False, 'error': f'Scrambling failed: {message}'}
            
            scrambled_images.append(scrambled_path)
            
            # Compute SHA-256 hash of scrambled image
            page_hash = compute_sha256(scrambled_path)
            page_hashes[f'page_{i + 1}'] = page_hash
        
        # Save encrypted chaos key
        chaos_key_path = os.path.join(exam_dir, 'chaos_key.enc')
        if not save_encrypted_chaos_key(chaos_key, chaos_key_path):
            return {'success': False, 'error': 'Failed to save chaos key'}
        
        # Create metadata
        metadata = {
            'exam_id': exam_id,
            'uploader': uploader,
            'upload_time': datetime.now().isoformat(),
            'scheduled_time': scheduled_time,
            'total_pages': len(original_images),
            'key_released': False,
            'release_time': None
        }
        
        # Encrypt metadata using Paillier
        encrypted_metadata = encrypt_metadata(metadata, page_hashes)
        
        # Save metadata
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(encrypted_metadata, f, indent=2)
        
        # Save plain hashes for integrity verification
        integrity_path = os.path.join(exam_dir, 'integrity.sha256')
        with open(integrity_path, 'w') as f:
            for page, hash_val in page_hashes.items():
                f.write(f"{page}: {hash_val}\n")
        
        # Clean up temp directory
        import shutil
        shutil.rmtree(temp_dir)
        
        return {
            'success': True,
            'exam_id': exam_id,
            'total_pages': len(original_images),
            'scrambled_images': len(scrambled_images),
            'message': 'Exam paper uploaded and scrambled successfully'
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Upload processing failed: {e}'}

def get_upload_info(exam_id, upload_folder):
    """Get information about uploaded exam"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        
        if not os.path.exists(metadata_path):
            return None
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Count scrambled images
        scrambled_count = 0
        for file in os.listdir(exam_dir):
            if file.startswith('scrambled_page_') and file.endswith('.png'):
                scrambled_count += 1
        
        return {
            'exam_id': exam_id,
            'metadata': metadata,
            'scrambled_images_count': scrambled_count,
            'chaos_key_exists': os.path.exists(os.path.join(exam_dir, 'chaos_key.enc')),
            'integrity_file_exists': os.path.exists(os.path.join(exam_dir, 'integrity.sha256'))
        }
        
    except Exception as e:
        print(f"Error getting upload info: {e}")
        return None