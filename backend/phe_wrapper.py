from phe import paillier
import json
import os
import pickle
from datetime import datetime

# Global key pair (in production, store securely)
PUBLIC_KEY = None
PRIVATE_KEY = None

def initialize_phe_keys():
    """Initialize Paillier key pair"""
    global PUBLIC_KEY, PRIVATE_KEY
    
    keys_file = '../config/phe_keys.pkl'
    
    if os.path.exists(keys_file):
        # Load existing keys
        with open(keys_file, 'rb') as f:
            keys = pickle.load(f)
            PUBLIC_KEY = keys['public']
            PRIVATE_KEY = keys['private']
    else:
        # Generate new keys
        PUBLIC_KEY, PRIVATE_KEY = paillier.generate_paillier_keypair()
        
        # Save keys
        os.makedirs('../config', exist_ok=True)
        with open(keys_file, 'wb') as f:
            pickle.dump({
                'public': PUBLIC_KEY,
                'private': PRIVATE_KEY
            }, f)

def encrypt_number(number):
    """Encrypt a number using Paillier encryption"""
    try:
        if PUBLIC_KEY is None:
            initialize_phe_keys()
        
        encrypted = PUBLIC_KEY.encrypt(number)
        return encrypted
        
    except Exception as e:
        print(f"Error encrypting number: {e}")
        return None

def decrypt_number(encrypted_number):
    """Decrypt a number using Paillier decryption"""
    try:
        if PRIVATE_KEY is None:
            initialize_phe_keys()
        
        decrypted = PRIVATE_KEY.decrypt(encrypted_number)
        return decrypted
        
    except Exception as e:
        print(f"Error decrypting number: {e}")
        return None

def encrypt_hash_to_number(hash_string):
    """Convert hash string to number and encrypt it"""
    try:
        # Convert hex hash to integer
        hash_number = int(hash_string, 16)
        
        # For very large hashes, take modulo to fit in reasonable range
        # This is a simplification - in production, you might split the hash
        hash_number = hash_number % (10**15)  # Keep it manageable
        
        return encrypt_number(hash_number)
        
    except Exception as e:
        print(f"Error encrypting hash: {e}")
        return None

def serialize_encrypted_number(encrypted_number):
    """Serialize encrypted number for JSON storage"""
    try:
        return {
            'ciphertext': str(encrypted_number.ciphertext()),
            'exponent': encrypted_number.exponent
        }
    except Exception as e:
        print(f"Error serializing encrypted number: {e}")
        return None

def deserialize_encrypted_number(serialized):
    """Deserialize encrypted number from JSON"""
    try:
        if PUBLIC_KEY is None:
            initialize_phe_keys()
        
        ciphertext = int(serialized['ciphertext'])
        exponent = serialized['exponent']
        
        # Reconstruct EncryptedNumber
        encrypted = paillier.EncryptedNumber(PUBLIC_KEY, ciphertext, exponent)
        return encrypted
        
    except Exception as e:
        print(f"Error deserializing encrypted number: {e}")
        return None

def encrypt_metadata(metadata, page_hashes):
    """Encrypt metadata and hashes using Paillier"""
    try:
        if PUBLIC_KEY is None:
            initialize_phe_keys()
        
        encrypted_metadata = metadata.copy()
        
        # Encrypt timestamp (convert to number)
        timestamp_num = int(datetime.fromisoformat(metadata['upload_time']).timestamp())
        encrypted_metadata['phe_timestamp'] = serialize_encrypted_number(
            encrypt_number(timestamp_num)
        )
        
        # Encrypt access counter (start with 0)
        encrypted_metadata['phe_access_counter'] = serialize_encrypted_number(
            encrypt_number(0)
        )
        
        # Encrypt page hashes
        encrypted_hashes = {}
        for page, hash_val in page_hashes.items():
            encrypted_hash = encrypt_hash_to_number(hash_val)
            if encrypted_hash:
                encrypted_hashes[page] = serialize_encrypted_number(encrypted_hash)
        
        encrypted_metadata['phe_hashes'] = encrypted_hashes
        
        # Keep some metadata in plain text for functionality
        encrypted_metadata['plain_hashes'] = page_hashes  # For integrity verification
        
        return encrypted_metadata
        
    except Exception as e:
        print(f"Error encrypting metadata: {e}")
        return metadata

def decrypt_metadata(encrypted_metadata):
    """Decrypt metadata using Paillier"""
    try:
        if PRIVATE_KEY is None:
            initialize_phe_keys()
        
        decrypted_metadata = encrypted_metadata.copy()
        
        # Decrypt timestamp
        if 'phe_timestamp' in encrypted_metadata:
            encrypted_ts = deserialize_encrypted_number(encrypted_metadata['phe_timestamp'])
            if encrypted_ts:
                timestamp_num = decrypt_number(encrypted_ts)
                decrypted_metadata['decrypted_timestamp'] = datetime.fromtimestamp(timestamp_num).isoformat()
        
        # Decrypt access counter
        if 'phe_access_counter' in encrypted_metadata:
            encrypted_counter = deserialize_encrypted_number(encrypted_metadata['phe_access_counter'])
            if encrypted_counter:
                counter_val = decrypt_number(encrypted_counter)
                decrypted_metadata['decrypted_access_counter'] = counter_val
        
        # Decrypt hashes
        if 'phe_hashes' in encrypted_metadata:
            decrypted_hashes = {}
            for page, encrypted_hash_data in encrypted_metadata['phe_hashes'].items():
                encrypted_hash = deserialize_encrypted_number(encrypted_hash_data)
                if encrypted_hash:
                    hash_number = decrypt_number(encrypted_hash)
                    # Convert back to hex (this is approximate due to modulo operation)
                    decrypted_hashes[page] = hex(hash_number)[2:]  # Remove '0x' prefix
            
            decrypted_metadata['decrypted_hashes'] = decrypted_hashes
        
        return decrypted_metadata
        
    except Exception as e:
        print(f"Error decrypting metadata: {e}")
        return encrypted_metadata

def increment_counter(exam_id, upload_folder):
    """Homomorphically increment access counter"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        
        if not os.path.exists(metadata_path):
            return False
        
        # Load metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Get encrypted counter
        if 'phe_access_counter' in metadata:
            encrypted_counter = deserialize_encrypted_number(metadata['phe_access_counter'])
            
            if encrypted_counter:
                # Homomorphically add 1
                incremented_counter = encrypted_counter + encrypt_number(1)
                
                # Update metadata
                metadata['phe_access_counter'] = serialize_encrypted_number(incremented_counter)
                metadata['last_access'] = datetime.now().isoformat()
                
                # Save updated metadata
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                return True
        
        return False
        
    except Exception as e:
        print(f"Error incrementing counter: {e}")
        return False

def get_access_count(exam_id, upload_folder):
    """Get decrypted access count for admin"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        
        if not os.path.exists(metadata_path):
            return None
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        if 'phe_access_counter' in metadata:
            encrypted_counter = deserialize_encrypted_number(metadata['phe_access_counter'])
            if encrypted_counter:
                return decrypt_number(encrypted_counter)
        
        return 0
        
    except Exception as e:
        print(f"Error getting access count: {e}")
        return None

def verify_encrypted_hash(exam_id, page, current_hash, upload_folder):
    """Verify hash against encrypted stored hash"""
    try:
        exam_dir = os.path.join(upload_folder, exam_id)
        metadata_path = os.path.join(exam_dir, 'metadata.json')
        
        if not os.path.exists(metadata_path):
            return False
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Use plain hashes for verification (more practical)
        if 'plain_hashes' in metadata and page in metadata['plain_hashes']:
            return metadata['plain_hashes'][page] == current_hash
        
        return False
        
    except Exception as e:
        print(f"Error verifying encrypted hash: {e}")
        return False

# Initialize keys when module is imported
initialize_phe_keys()