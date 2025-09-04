import hashlib
import os
import json

def compute_sha256(file_path):
    """Compute SHA-256 hash of a file"""
    try:
        sha256_hash = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
        
    except Exception as e:
        print(f"Error computing SHA-256: {e}")
        return None

def compute_string_hash(text):
    """Compute SHA-256 hash of a string"""
    try:
        return hashlib.sha256(text.encode()).hexdigest()
    except Exception as e:
        print(f"Error computing string hash: {e}")
        return None

def verify_integrity(exam_id, upload_folder):
    """Verify integrity of scrambled exam papers"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        integrity_path = os.path.join(exam_dir, 'integrity.sha256')
        
        if not os.path.exists(integrity_path):
            return {'valid': False, 'error': 'Integrity file not found'}
        
        # Read stored hashes
        stored_hashes = {}
        with open(integrity_path, 'r') as f:
            for line in f:
                if ':' in line:
                    page, hash_val = line.strip().split(': ', 1)
                    stored_hashes[page] = hash_val
        
        # Verify each scrambled image
        verification_results = {}
        all_valid = True
        
        for page, stored_hash in stored_hashes.items():
            page_num = page.split('_')[1]
            scrambled_file = os.path.join(exam_dir, f'scrambled_page_{page_num}.png')
            
            if os.path.exists(scrambled_file):
                current_hash = compute_sha256(scrambled_file)
                is_valid = current_hash == stored_hash
                
                verification_results[page] = {
                    'stored_hash': stored_hash,
                    'current_hash': current_hash,
                    'valid': is_valid
                }
                
                if not is_valid:
                    all_valid = False
            else:
                verification_results[page] = {
                    'stored_hash': stored_hash,
                    'current_hash': None,
                    'valid': False,
                    'error': 'File not found'
                }
                all_valid = False
        
        return {
            'valid': all_valid,
            'exam_id': exam_id,
            'verification_results': verification_results,
            'total_pages': len(stored_hashes)
        }
        
    except Exception as e:
        return {'valid': False, 'error': f'Verification failed: {e}'}

def create_hash_chain_entry(prev_hash, data):
    """Create a hash chain entry for tamper-proof logs"""
    try:
        # Combine previous hash with current data
        combined = f"{prev_hash}{json.dumps(data, sort_keys=True)}"
        return compute_string_hash(combined)
        
    except Exception as e:
        print(f"Error creating hash chain entry: {e}")
        return None

def verify_hash_chain(log_entries):
    """Verify the integrity of a hash chain"""
    try:
        if not log_entries:
            return True
        
        # First entry should have prev_hash of "0000" or similar
        if log_entries[0].get('prev_hash') != "0000":
            return False
        
        # Verify each subsequent entry
        for i in range(len(log_entries)):
            entry = log_entries[i]
            
            # Create data without the hash field for verification
            data_for_hash = {
                'id': entry['id'],
                'event': entry['event'],
                'user': entry['user'],
                'exam_id': entry.get('exam_id'),
                'timestamp': entry['timestamp'],
                'details': entry.get('details', '')
            }
            
            prev_hash = entry['prev_hash']
            expected_hash = create_hash_chain_entry(prev_hash, data_for_hash)
            
            if expected_hash != entry['hash']:
                return False
            
            # Check if prev_hash matches previous entry's hash (except for first entry)
            if i > 0 and prev_hash != log_entries[i-1]['hash']:
                return False
        
        return True
        
    except Exception as e:
        print(f"Error verifying hash chain: {e}")
        return False

def compute_metadata_hash(metadata):
    """Compute hash of metadata for integrity verification"""
    try:
        # Sort keys to ensure consistent hashing
        metadata_str = json.dumps(metadata, sort_keys=True)
        return compute_string_hash(metadata_str)
        
    except Exception as e:
        print(f"Error computing metadata hash: {e}")
        return None

def verify_file_integrity_batch(file_paths):
    """Verify integrity of multiple files at once"""
    try:
        results = {}
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                file_hash = compute_sha256(file_path)
                results[file_path] = {
                    'exists': True,
                    'hash': file_hash,
                    'size': os.path.getsize(file_path)
                }
            else:
                results[file_path] = {
                    'exists': False,
                    'hash': None,
                    'size': 0
                }
        
        return results
        
    except Exception as e:
        print(f"Error in batch integrity verification: {e}")
        return {}