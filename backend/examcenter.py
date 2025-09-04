import os
import json
from datetime import datetime
from chaotic import load_encrypted_chaos_key, unscramble_image
from timelock import check_release_time
import zipfile
import tempfile

def download_scrambled_paper(exam_id, upload_folder):
    """Download scrambled exam paper for exam center"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        
        if not os.path.exists(exam_dir):
            return {'success': False, 'error': 'Exam not found'}
        
        # Check if exam exists and get metadata
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        if not os.path.exists(metadata_path):
            return {'success': False, 'error': 'Exam metadata not found'}
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Get all scrambled images
        scrambled_images = []
        for file in os.listdir(exam_dir):
            if file.startswith('scrambled_page_') and file.endswith('.png'):
                scrambled_images.append(os.path.join(exam_dir, file))
        
        if not scrambled_images:
            return {'success': False, 'error': 'No scrambled images found'}
        
        # Sort images by page number
        scrambled_images.sort(key=lambda x: int(x.split('_page_')[1].split('.')[0]))
        
        return {
            'success': True,
            'exam_id': exam_id,
            'total_pages': len(scrambled_images),
            'scrambled_images': scrambled_images,
            'scheduled_time': metadata.get('scheduled_time'),
            'key_released': metadata.get('key_released', False),
            'message': 'Scrambled paper downloaded successfully'
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Download failed: {e}'}

def create_scrambled_package(exam_id, upload_folder, output_path=None):
    """Create a ZIP package of scrambled images for distribution"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        
        if not os.path.exists(exam_dir):
            return {'success': False, 'error': 'Exam not found'}
        
        # Create output path if not provided
        if not output_path:
            output_path = os.path.join(exam_dir, f'{exam_id}_scrambled_package.zip')
        
        # Get scrambled images
        scrambled_images = []
        for file in os.listdir(exam_dir):
            if file.startswith('scrambled_page_') and file.endswith('.png'):
                scrambled_images.append(os.path.join(exam_dir, file))
        
        if not scrambled_images:
            return {'success': False, 'error': 'No scrambled images found'}
        
        # Create ZIP package
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for img_path in scrambled_images:
                filename = os.path.basename(img_path)
                zipf.write(img_path, filename)
            
            # Add metadata (without sensitive information)
            metadata_path = os.path.join(exam_dir, 'metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                # Create safe metadata for exam centers
                safe_metadata = {
                    'exam_id': metadata.get('exam_id'),
                    'total_pages': metadata.get('total_pages'),
                    'scheduled_time': metadata.get('scheduled_time'),
                    'package_created': datetime.now().isoformat()
                }
                
                # Add safe metadata to ZIP
                zipf.writestr('exam_info.json', json.dumps(safe_metadata, indent=2))
        
        return {
            'success': True,
            'package_path': output_path,
            'total_pages': len(scrambled_images),
            'message': 'Scrambled package created successfully'
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Package creation failed: {e}'}

def decrypt_paper(exam_id, upload_folder):
    """Decrypt scrambled paper when chaos key is released"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        
        if not os.path.exists(exam_dir):
            return {'success': False, 'error': 'Exam not found'}
        
        # Check metadata
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        if not os.path.exists(metadata_path):
            return {'success': False, 'error': 'Exam metadata not found'}
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Check if it's time to release the key
        scheduled_time = metadata.get('scheduled_time')
        if not scheduled_time:
            return {'success': False, 'error': 'No scheduled time found'}
        
        if not check_release_time(scheduled_time):
            return {'success': False, 'error': 'Not yet time to decrypt paper'}
        
        # Check if chaos key exists
        chaos_key_path = os.path.join(exam_dir, 'chaos_key.enc')
        if not os.path.exists(chaos_key_path):
            return {'success': False, 'error': 'Chaos key not found'}
        
        # Load chaos key
        chaos_key = load_encrypted_chaos_key(chaos_key_path)
        if not chaos_key:
            return {'success': False, 'error': 'Failed to load chaos key'}
        
        # Create decrypted directory
        decrypted_dir = os.path.join(exam_dir, 'decrypted')
        os.makedirs(decrypted_dir, exist_ok=True)
        
        # Decrypt all scrambled images
        decrypted_images = []
        scrambled_images = []
        
        for file in os.listdir(exam_dir):
            if file.startswith('scrambled_page_') and file.endswith('.png'):
                scrambled_images.append(file)
        
        # Sort by page number
        scrambled_images.sort(key=lambda x: int(x.split('_page_')[1].split('.')[0]))
        
        for scrambled_file in scrambled_images:
            scrambled_path = os.path.join(exam_dir, scrambled_file)
            
            # Create decrypted filename
            page_num = scrambled_file.split('_page_')[1].split('.')[0]
            decrypted_file = f'page_{page_num}.png'
            decrypted_path = os.path.join(decrypted_dir, decrypted_file)
            
            # Unscramble image
            success, message = unscramble_image(scrambled_path, chaos_key, decrypted_path)
            
            if success:
                decrypted_images.append(decrypted_path)
            else:
                return {'success': False, 'error': f'Failed to decrypt {scrambled_file}: {message}'}
        
        # Update metadata to mark as decrypted
        metadata['decrypted'] = True
        metadata['decryption_time'] = datetime.now().isoformat()
        metadata['decrypted_images_count'] = len(decrypted_images)
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            'success': True,
            'exam_id': exam_id,
            'decrypted_images': decrypted_images,
            'total_pages': len(decrypted_images),
            'decrypted_dir': decrypted_dir,
            'message': 'Paper decrypted successfully'
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Decryption failed: {e}'}

def get_exam_status(exam_id, upload_folder):
    """Get current status of exam for exam center"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        
        if not os.path.exists(exam_dir):
            return {'success': False, 'error': 'Exam not found'}
        
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        if not os.path.exists(metadata_path):
            return {'success': False, 'error': 'Exam metadata not found'}
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Check various status indicators
        scheduled_time = metadata.get('scheduled_time')
        key_released = metadata.get('key_released', False)
        decrypted = metadata.get('decrypted', False)
        
        # Check if chaos key exists
        chaos_key_exists = os.path.exists(os.path.join(exam_dir, 'chaos_key.enc'))
        
        # Check if decrypted images exist
        decrypted_dir = os.path.join(exam_dir, 'decrypted')
        decrypted_images_exist = os.path.exists(decrypted_dir) and len(os.listdir(decrypted_dir)) > 0
        
        # Count scrambled images
        scrambled_count = 0
        for file in os.listdir(exam_dir):
            if file.startswith('scrambled_page_') and file.endswith('.png'):
                scrambled_count += 1
        
        # Determine current status
        current_time = datetime.now()
        can_decrypt = False
        status_message = "Exam not ready"
        
        if scheduled_time:
            if check_release_time(scheduled_time):
                can_decrypt = True
                if decrypted:
                    status_message = "Exam completed - paper decrypted"
                else:
                    status_message = "Ready for decryption"
            else:
                status_message = f"Waiting for scheduled time: {scheduled_time}"
        
        return {
            'success': True,
            'exam_id': exam_id,
            'scheduled_time': scheduled_time,
            'current_time': current_time.isoformat(),
            'key_released': key_released,
            'decrypted': decrypted,
            'can_decrypt': can_decrypt,
            'chaos_key_exists': chaos_key_exists,
            'decrypted_images_exist': decrypted_images_exist,
            'scrambled_images_count': scrambled_count,
            'status_message': status_message,
            'total_pages': metadata.get('total_pages', 0)
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Status check failed: {e}'}

def verify_scrambled_integrity(exam_id, upload_folder):
    """Verify integrity of scrambled images before decryption"""
    try:
        from hashing import verify_integrity
        
        result = verify_integrity(exam_id, upload_folder)
        
        return {
            'success': True,
            'integrity_check': result,
            'message': 'Integrity verification completed'
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Integrity verification failed: {e}'}

def list_available_exams(upload_folder):
    """List all available exams for exam center"""
    try:
        available_exams = []
        
        if not os.path.exists(upload_folder):
            return {'success': True, 'exams': []}
        
        for exam_folder in os.listdir(upload_folder):
            exam_path = os.path.join(upload_folder, exam_folder)
            if os.path.isdir(exam_path):
                status = get_exam_status(exam_folder, upload_folder)
                if status['success']:
                    available_exams.append({
                        'exam_id': exam_folder,
                        'status': status
                    })
        
        # Sort by scheduled time
        available_exams.sort(key=lambda x: x['status'].get('scheduled_time', ''))
        
        return {
            'success': True,
            'exams': available_exams,
            'total_count': len(available_exams)
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Failed to list exams: {e}'}