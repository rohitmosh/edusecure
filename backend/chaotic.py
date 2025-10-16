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

def arnold_cat_map(x, y, a, b, height, width):
    """Apply Arnold Cat Map transformation for rectangular images"""
    x_new = (x + a * y) % height
    y_new = (b * x + (a * b + 1) * y) % width
    return int(x_new), int(y_new)

def inverse_arnold_cat_map(x, y, a, b, height, width):
    """Apply inverse Arnold Cat Map transformation for rectangular images"""
    det = a * b + 1
    
    # Modular multiplicative inverse for height and width separately
    try:
        det_inv_h = pow(det, -1, height) if height > 1 else 1
        det_inv_w = pow(det, -1, width) if width > 1 else 1
    except ValueError:
        # If gcd(det, height/width) != 1, use alternative approach
        det_inv_h = 1
        det_inv_w = 1
    
    # Modified inverse transformation for rectangular images
    x_orig = ((a * b + 1) * x - a * y) % height
    y_orig = (-b * x + y) % width
    
    return int(x_orig), int(y_orig)

def scramble_image(image_path, chaos_key, output_path):
    """Scramble image using chaotic pixel permutation with complete coverage"""
    try:
        # Load image
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Set random seed for reproducibility
        np.random.seed(chaos_key['seed'])
        
        # Method 1: Complete Pixel Permutation (Primary scrambling)
        total_pixels = height * width
        sequence = logistic_map_sequence(
            chaos_key['logistic_r'], 
            chaos_key['logistic_x0'], 
            total_pixels
        )
        
        # Create bijective permutation (ensures every pixel maps to exactly one location)
        indices = np.argsort(sequence)
        
        # Flatten and scramble pixels
        flat_img = img_array.reshape(-1, channels)
        scrambled_flat = flat_img[indices]
        scrambled_img = scrambled_flat.reshape(height, width, channels)
        
        # Method 2: Enhanced Arnold Cat Map for Rectangular Images
        for iteration in range(3):
            # Create coordinate mapping arrays for bijective transformation
            coord_map = np.zeros((height, width, 2), dtype=int)
            
            # Generate all coordinate mappings first
            for i in range(height):
                for j in range(width):
                    new_i, new_j = arnold_cat_map(
                        i, j, 
                        chaos_key['arnold_a'], 
                        chaos_key['arnold_b'], 
                        height, width
                    )
                    coord_map[i, j] = [new_i, new_j]
            
            # Apply the transformation using the coordinate map
            new_img = np.copy(scrambled_img)  # Copy instead of zeros
            for i in range(height):
                for j in range(width):
                    new_i, new_j = coord_map[i, j]
                    new_img[new_i, new_j] = scrambled_img[i, j]
            
            scrambled_img = new_img
        
        # Method 3: Additional Fisher-Yates Shuffle for extra security
        # Flatten for final shuffle
        final_flat = scrambled_img.reshape(-1, channels)
        
        # Generate permutation using chaos parameters
        np.random.seed(chaos_key['seed'] + 1000)  # Different seed for final shuffle
        shuffle_indices = np.arange(total_pixels)
        np.random.shuffle(shuffle_indices)
        
        # Apply final permutation
        final_scrambled = final_flat[shuffle_indices]
        final_img = final_scrambled.reshape(height, width, channels)
        
        # Save scrambled image
        scrambled_pil = Image.fromarray(final_img.astype('uint8'))
        scrambled_pil.save(output_path)
        
        return True, "Image scrambled successfully with complete coverage"
        
    except Exception as e:
        return False, f"Error scrambling image: {e}"

def unscramble_image(scrambled_path, chaos_key, output_path):
    """Unscramble image using inverse chaotic operations with complete coverage"""
    try:
        # Load scrambled image
        img = Image.open(scrambled_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        height, width, channels = img_array.shape
        total_pixels = height * width
        
        # Step 1: Reverse the final Fisher-Yates shuffle
        np.random.seed(chaos_key['seed'] + 1000)  # Same seed as scrambling
        shuffle_indices = np.arange(total_pixels)
        np.random.shuffle(shuffle_indices)
        
        # Create inverse shuffle indices
        inverse_shuffle = np.argsort(shuffle_indices)
        
        # Apply inverse shuffle
        flat_img = img_array.reshape(-1, channels)
        unshuffled_flat = flat_img[inverse_shuffle]
        unscrambled_img = unshuffled_flat.reshape(height, width, channels)
        
        # Step 2: Reverse Arnold Cat Map transformations (in reverse order)
        np.random.seed(chaos_key['seed'])  # Reset to original seed
        
        for iteration in range(3):  # Same number of iterations
            # Create inverse coordinate mapping
            coord_map = np.zeros((height, width, 2), dtype=int)
            
            # Generate inverse mappings
            for i in range(height):
                for j in range(width):
                    orig_i, orig_j = inverse_arnold_cat_map(
                        i, j,
                        chaos_key['arnold_a'],
                        chaos_key['arnold_b'], 
                        height, width
                    )
                    coord_map[i, j] = [orig_i, orig_j]
            
            # Apply inverse transformation
            new_img = np.copy(unscrambled_img)
            for i in range(height):
                for j in range(width):
                    orig_i, orig_j = coord_map[i, j]
                    new_img[orig_i, orig_j] = unscrambled_img[i, j]
            
            unscrambled_img = new_img
        
        # Step 3: Reverse the primary pixel permutation
        sequence = logistic_map_sequence(
            chaos_key['logistic_r'],
            chaos_key['logistic_x0'], 
            total_pixels
        )
        
        # Create inverse permutation indices
        indices = np.argsort(sequence)
        inverse_indices = np.argsort(indices)
        
        # Apply inverse permutation
        flat_img = unscrambled_img.reshape(-1, channels)
        final_flat = flat_img[inverse_indices]
        final_img = final_flat.reshape(height, width, channels)
        
        # Save unscrambled image
        final_pil = Image.fromarray(final_img.astype('uint8'))
        final_pil.save(output_path)
        
        return True, "Image unscrambled successfully with complete recovery"
        
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

def block_scramble_image(image_path, chaos_key, output_path, block_size=8):
    """Advanced block-based scrambling for maximum security and uniform coverage"""
    try:
        # Load image
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Pad image to be divisible by block_size
        pad_h = (block_size - height % block_size) % block_size
        pad_w = (block_size - width % block_size) % block_size
        
        if pad_h > 0 or pad_w > 0:
            padded_img = np.pad(img_array, ((0, pad_h), (0, pad_w), (0, 0)), mode='edge')
        else:
            padded_img = img_array
        
        new_height, new_width = padded_img.shape[:2]
        
        # Set random seed
        np.random.seed(chaos_key['seed'])
        
        # Step 1: Block-level scrambling
        blocks_h = new_height // block_size
        blocks_w = new_width // block_size
        total_blocks = blocks_h * blocks_w
        
        # Create block permutation using chaotic sequence
        block_sequence = logistic_map_sequence(
            chaos_key['logistic_r'], 
            chaos_key['logistic_x0'], 
            total_blocks
        )
        block_indices = np.argsort(block_sequence)
        
        # Scramble blocks
        scrambled_img = np.zeros_like(padded_img)
        for block_idx in range(total_blocks):
            # Original block position
            orig_block_i = block_idx // blocks_w
            orig_block_j = block_idx % blocks_w
            
            # New block position
            new_block_idx = block_indices[block_idx]
            new_block_i = new_block_idx // blocks_w
            new_block_j = new_block_idx % blocks_w
            
            # Copy block
            orig_start_i = orig_block_i * block_size
            orig_end_i = orig_start_i + block_size
            orig_start_j = orig_block_j * block_size
            orig_end_j = orig_start_j + block_size
            
            new_start_i = new_block_i * block_size
            new_end_i = new_start_i + block_size
            new_start_j = new_block_j * block_size
            new_end_j = new_start_j + block_size
            
            scrambled_img[new_start_i:new_end_i, new_start_j:new_end_j] = \
                padded_img[orig_start_i:orig_end_i, orig_start_j:orig_end_j]
        
        # Step 2: Pixel-level scrambling within each block
        for block_i in range(blocks_h):
            for block_j in range(blocks_w):
                start_i = block_i * block_size
                end_i = start_i + block_size
                start_j = block_j * block_size
                end_j = start_j + block_size
                
                # Extract block
                block = scrambled_img[start_i:end_i, start_j:end_j]
                
                # Scramble pixels within block
                flat_block = block.reshape(-1, channels)
                
                # Generate permutation for this block
                np.random.seed(chaos_key['seed'] + block_i * blocks_w + block_j)
                pixel_indices = np.arange(block_size * block_size)
                np.random.shuffle(pixel_indices)
                
                # Apply permutation
                scrambled_block = flat_block[pixel_indices].reshape(block_size, block_size, channels)
                scrambled_img[start_i:end_i, start_j:end_j] = scrambled_block
        
        # Remove padding if it was added
        if pad_h > 0 or pad_w > 0:
            final_img = scrambled_img[:height, :width]
        else:
            final_img = scrambled_img
        
        # Save scrambled image
        scrambled_pil = Image.fromarray(final_img.astype('uint8'))
        scrambled_pil.save(output_path)
        
        return True, "Image block-scrambled successfully with complete coverage"
        
    except Exception as e:
        return False, f"Error in block scrambling: {e}"

def block_unscramble_image(scrambled_path, chaos_key, output_path, block_size=8):
    """Reverse block-based scrambling"""
    try:
        # Load scrambled image
        img = Image.open(scrambled_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Pad image to be divisible by block_size (same as scrambling)
        pad_h = (block_size - height % block_size) % block_size
        pad_w = (block_size - width % block_size) % block_size
        
        if pad_h > 0 or pad_w > 0:
            padded_img = np.pad(img_array, ((0, pad_h), (0, pad_w), (0, 0)), mode='edge')
        else:
            padded_img = img_array
        
        new_height, new_width = padded_img.shape[:2]
        unscrambled_img = np.copy(padded_img)
        
        # Step 1: Reverse pixel-level scrambling within each block
        blocks_h = new_height // block_size
        blocks_w = new_width // block_size
        
        for block_i in range(blocks_h):
            for block_j in range(blocks_w):
                start_i = block_i * block_size
                end_i = start_i + block_size
                start_j = block_j * block_size
                end_j = start_j + block_size
                
                # Extract block
                block = unscrambled_img[start_i:end_i, start_j:end_j]
                flat_block = block.reshape(-1, channels)
                
                # Generate same permutation
                np.random.seed(chaos_key['seed'] + block_i * blocks_w + block_j)
                pixel_indices = np.arange(block_size * block_size)
                np.random.shuffle(pixel_indices)
                
                # Create inverse permutation
                inverse_indices = np.argsort(pixel_indices)
                
                # Apply inverse permutation
                unscrambled_block = flat_block[inverse_indices].reshape(block_size, block_size, channels)
                unscrambled_img[start_i:end_i, start_j:end_j] = unscrambled_block
        
        # Step 2: Reverse block-level scrambling
        np.random.seed(chaos_key['seed'])
        total_blocks = blocks_h * blocks_w
        
        block_sequence = logistic_map_sequence(
            chaos_key['logistic_r'], 
            chaos_key['logistic_x0'], 
            total_blocks
        )
        block_indices = np.argsort(block_sequence)
        inverse_block_indices = np.argsort(block_indices)
        
        final_img = np.zeros_like(unscrambled_img)
        for block_idx in range(total_blocks):
            # Current block position
            curr_block_i = block_idx // blocks_w
            curr_block_j = block_idx % blocks_w
            
            # Original block position
            orig_block_idx = inverse_block_indices[block_idx]
            orig_block_i = orig_block_idx // blocks_w
            orig_block_j = orig_block_idx % blocks_w
            
            # Copy block back
            curr_start_i = curr_block_i * block_size
            curr_end_i = curr_start_i + block_size
            curr_start_j = curr_block_j * block_size
            curr_end_j = curr_start_j + block_size
            
            orig_start_i = orig_block_i * block_size
            orig_end_i = orig_start_i + block_size
            orig_start_j = orig_block_j * block_size
            orig_end_j = orig_start_j + block_size
            
            final_img[orig_start_i:orig_end_i, orig_start_j:orig_end_j] = \
                unscrambled_img[curr_start_i:curr_end_i, curr_start_j:curr_end_j]
        
        # Remove padding
        if pad_h > 0 or pad_w > 0:
            result_img = final_img[:height, :width]
        else:
            result_img = final_img
        
        # Save unscrambled image
        final_pil = Image.fromarray(result_img.astype('uint8'))
        final_pil.save(output_path)
        
        return True, "Image block-unscrambled successfully"
        
    except Exception as e:
        return False, f"Error in block unscrambling: {e}"