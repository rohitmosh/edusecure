import json
import hashlib
import os

# Get the absolute path to users.json
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'users', 'users.json')

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate user credentials"""
    try:
        if not os.path.exists(USERS_FILE):
            return None
        
        with open(USERS_FILE, 'r') as f:
            users_data = json.load(f)
        
        hashed_password = hash_password(password)
        
        for user in users_data.get('users', []):
            if user['username'] == username and user['password'] == hashed_password:
                return user
        
        return None
        
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def get_user_role(username):
    """Get user role by username"""
    try:
        if not os.path.exists(USERS_FILE):
            return None
        
        with open(USERS_FILE, 'r') as f:
            users_data = json.load(f)
        
        for user in users_data.get('users', []):
            if user['username'] == username:
                return user['role']
        
        return None
        
    except Exception as e:
        print(f"Error getting user role: {e}")
        return None

def create_user(username, password, role):
    """Create a new user (admin only function)"""
    try:
        users_data = {"users": []}
        
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                users_data = json.load(f)
        
        # Check if user already exists
        for user in users_data.get('users', []):
            if user['username'] == username:
                return False, "User already exists"
        
        # Add new user
        new_user = {
            "username": username,
            "password": hash_password(password),
            "role": role
        }
        
        users_data['users'].append(new_user)
        
        with open(USERS_FILE, 'w') as f:
            json.dump(users_data, f, indent=2)
        
        return True, "User created successfully"
        
    except Exception as e:
        return False, f"Error creating user: {e}"

def validate_role(role):
    """Validate if role is valid"""
    valid_roles = ['admin', 'faculty', 'exam_center']
    return role in valid_roles