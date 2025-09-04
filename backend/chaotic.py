import numpy as np
from PIL import Image
import json
import os
import secrets
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64

def generate_chaos_key():
    """Generate chaos parameters for pixel scrambling"""
    # Logistic map parameters
    r = np.random.uniform(3.57, 4.0)  # Chaotic regime
    x0 = np.random.uniform(0.1, 0.9)  # Initial condition
    
    # Arnold Cat Map parameters  
    a = np.random.randint(1, 10)
    b = np.random.randint(1, 10)
    
    return {
        'logistic_r': r,
        'logistic_x0': x0,
        'arnold_a': a,
        'arnold_b': b,
        'seed': secrets.randbelow(1000000)
    }

def logistic_map_sequence(r, x0, length):
    """Generate chaotic sequence using logistic map"""
    sequence = []
    x = x0
    
    for _ in range(length):
        x = r * x * (1 - x)
        sequence.append(x)
    
    return np.array(sequence)

def arnold_cat_map(x, y, a, b, N):
    """Apply Arnold Cat Map transformation"""
    x_new = (x + a * y) % N
    y_new = (b * x + (a * b + 1) * y) % N
    return int(x_new), int(y_new)

def inverse_arnold_cat_map(x, y, a, b, N):
    """Apply inverse Arnold Cat Map transformation"""
    det = a * b + 1
    # Modular multiplicative inverse
    det_inv = pow(det, -1, N)
    
    x_orig = ((a * b + 1) * x - a * y) * det_inv % N
    y_orig = (-b * x + y) * det_inv % N
    
    return int(x_orig), int(y_orig)

def scramble_image(image_path, chaos_key, output_path):
    """Scramble image using chaotic pixel permutation"""
    try:
        # Load image
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Set random seed for reproducibility
        np.random.seed(chaos_key['seed'])
        
        # Generate chaotic sequence for pixel positions
        total_pixels = height * width
        sequence = logistic_map_sequence(
            chaos_key['logistic_r'], 
            chaos_key['logistic_x0'], 
            total_pixels
        )
        
        # Create scrambling indices using chaotic sequence
        indices = np.argsort(sequence)
        
        # Flatten image for scrambling
        flat_img = img_array.reshape(-1, channels)
        
        # Scramble pixels
        scrambled_flat = flat_img[indices]
        
        # Apply Arnold Cat Map for additional scrambling
        scrambled_img = scrambled_flat.reshape(height, width, channels)
        
        # Arnold Cat Map on coordinates
        for iteration in range(3):  # Multiple iterations for better scrambling
            new_img = np.zeros_like(scrambled_img)
            for i in range(height):
                for j in range(width):
                    new_i, new_j = arnold_cat_map(
                        i, j, 
                        chaos_key['arnold_a'], 
                        chaos_key['arnold_b'], 
                        min(height, width)
                    )
                    new_i = new_i % height
                    new_j = new_j % width
                    new_img[new_i, new_j] = scrambled_img[i, j]
            scrambled_img = new_img
        
        # Save scrambled image
        scrambled_pil = Image.fromarray(scrambled_img.astype('uint8'))
        scrambled_pil.save(output_path)
        
        return True, "Image scrambled successfully"
        
    except Exception as e:
        return False, f"Error scrambling image: {e}"

def unscramble_image(scrambled_path, chaos_key, output_path):
    """Unscramble image using inverse chaotic operations"""
    try:
        # Load scrambled image
        img = Image.open(scrambled_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Set same random seed
        np.random.seed(chaos_key['seed'])
        
        # Apply inverse Arnold Cat Map
        unscrambled_img = img_array.copy()
        
        for iteration in range(3):  # Same number of iterations, reverse order
            new_img = np.zeros_like(unscrambled_img)
            for i in range(height):
                for j in range(width):
                    orig_i, orig_j = inverse_arnold_cat_map(
                        i, j,
                        chaos_key['arnold_a'],
                        chaos_key['arnold_b'], 
                        min(height, width)
                    )
                    orig_i = orig_i % height
                    orig_j = orig_j % width
                    new_img[orig_i, orig_j] = unscrambled_img[i, j]
            unscrambled_img = new_img
        
        # Generate same chaotic sequence
        total_pixels = height * width
        sequence = logistic_map_sequence(
            chaos_key['logistic_r'],
            chaos_key['logistic_x0'], 
            total_pixels
        )
        
        # Create inverse scrambling indices
        indices = np.argsort(sequence)
        inverse_indices = np.argsort(indices)
        
        # Flatten and unscramble pixels
        flat_img = unscrambled_img.reshape(-1, channels)
        unscrambled_flat = flat_img[inverse_indices]
        
        # Reshape back to original
        final_img = unscrambled_flat.reshape(height, width, channels)
        
        # Save unscrambled image
        final_pil = Image.fromarray(final_img.astype('uint8'))
        final_pil.save(output_path)
        
        return True, "Image unscrambled successfully"
        
    except Exception as e:
        return False, f"Error unscrambling image: {e}"

def get_or_create_rsa_keys():
    """Get or create RSA key pair for admin"""
    keys_dir = '../config'
    private_key_path = os.path.join(keys_dir, 'admin_private_key.pem')
    public_key_path = os.path.join(keys_dir, 'admin_public_key.pem')
    
    os.makedirs(keys_dir, exist_ok=True)
    
    if os.path.exists(private_key_path) and os.path.exists(public_key_path):
        # Load existing keys
        with open(private_key_path, 'rb') as f:
            private_key = RSA.import_key(f.read())
        with open(public_key_path, 'rb') as f:
            public_key = RSA.import_key(f.read())
    else:
        # Generate new RSA key pair
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()
        
        # Save keys
        with open(private_key_path, 'wb') as f:
            f.write(private_key.export_key())
        with open(public_key_path, 'wb') as f:
            f.write(public_key.export_key())
    
    return private_key, public_key

def encrypt_chaos_key(chaos_key):
    """Encrypt chaos key using RSA for Admin"""
    try:
        # Convert chaos key to JSON string
        key_json = json.dumps(chaos_key)
        key_bytes = key_json.encode()
        
        # Get RSA public key
        _, public_key = get_or_create_rsa_keys()
        
        # Encrypt with RSA
        cipher_rsa = PKCS1_OAEP.new(public_key)
        
        # RSA can only encrypt small amounts of data, so we use hybrid encryption
        # Generate AES key for actual data encryption
        aes_key = get_random_bytes(32)
        
        # Encrypt the chaos key data with AES
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        
        cipher_aes = AES.new(aes_key, AES.MODE_CBC)
        padded_data = pad(key_bytes, AES.block_size)
        encrypted_data = cipher_aes.encrypt(padded_data)
        
        # Encrypt the AES key with RSA
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        
        # Combine everything
        result = {
            'encrypted_aes_key': base64.b64encode(encrypted_aes_key).decode(),
            'encrypted_data': base64.b64encode(encrypted_data).decode(),
            'iv': base64.b64encode(cipher_aes.iv).decode()
        }
        
        return json.dumps(result).encode()
        
    except Exception as e:
        print(f"Error encrypting chaos key: {e}")
        return None

def decrypt_chaos_key(encrypted_key_data):
    """Decrypt chaos key using RSA (Admin only)"""
    try:
        # Parse the encrypted data
        encrypted_data_json = json.loads(encrypted_key_data.decode())
        
        encrypted_aes_key = base64.b64decode(encrypted_data_json['encrypted_aes_key'])
        encrypted_data = base64.b64decode(encrypted_data_json['encrypted_data'])
        iv = base64.b64decode(encrypted_data_json['iv'])
        
        # Get RSA private key
        private_key, _ = get_or_create_rsa_keys()
        
        # Decrypt AES key with RSA
        cipher_rsa = PKCS1_OAEP.new(private_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        
        # Decrypt data with AES
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_padded = cipher_aes.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_padded, AES.block_size)
        
        # Parse back to dictionary
        key_json = decrypted_data.decode()
        chaos_key = json.loads(key_json)
        
        return chaos_key
        
    except Exception as e:
        print(f"Error decrypting chaos key: {e}")
        return None

def save_encrypted_chaos_key(chaos_key, file_path):
    """Save encrypted chaos key to file"""
    try:
        encrypted_key = encrypt_chaos_key(chaos_key)
        if encrypted_key:
            with open(file_path, 'wb') as f:
                f.write(encrypted_key)
            return True
        return False
        
    except Exception as e:
        print(f"Error saving encrypted chaos key: {e}")
        return False

def load_encrypted_chaos_key(file_path):
    """Load and decrypt chaos key from file"""
    try:
        with open(file_path, 'rb') as f:
            encrypted_key = f.read()
        
        chaos_key = decrypt_chaos_key(encrypted_key)
        return chaos_key
        
    except Exception as e:
        print(f"Error loading encrypted chaos key: {e}")
        return None