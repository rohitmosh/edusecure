# EduSecure: Secure Exam Paper Management System

A comprehensive secure exam paper management system that uses chaotic pixel scrambling, homomorphic encryption, and tamper-proof logging to protect exam papers until their scheduled release time.

## 🔐 Security Features

- **Chaotic Pixel Scrambling**: Uses logistic maps and Arnold Cat maps to make exam papers unreadable
- **Homomorphic Encryption**: Paillier encryption for privacy-preserving metadata operations
- **SHA-256 Hashing**: Ensures integrity verification of scrambled papers
- **Time-Lock Access Control**: Papers can only be decrypted at scheduled exam times
- **Tamper-Proof Logs**: Hash-chained audit logs for complete accountability
- **Role-Based Access**: Separate interfaces for Admin, Faculty, and Exam Centers

## 🏗️ Architecture

### Backend (Python Flask)
- **Chaotic Scrambling**: Custom implementation using NumPy
- **Homomorphic Encryption**: Using the `phe` library (Paillier)
- **File-Based Storage**: No database required - uses JSON files and filesystem
- **PDF Processing**: Converts PDFs to images for scrambling

### Frontend (React + TypeScript)
- **Modern UI**: Built with shadcn/ui components
- **Role-Based Views**: Different interfaces for each user type
- **Real-Time Updates**: Automatic polling for status changes
- **Responsive Design**: Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### One-Command Launch (Recommended)

```bash
python start.py
```

This will:
- ✅ Check system requirements
- 📦 Install all dependencies automatically
- 🔐 Optionally run security features demo
- 🚀 Start both backend and frontend servers
- 🌐 Open your browser automatically

### Manual Setup (Alternative)

#### Backend Setup:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

#### Frontend Setup:
```bash
npm install
npm run dev
```

### Security Features Demo

Run the comprehensive security demonstration:
```bash
python demo_security_features.py
```

This showcases all cryptographic features with visual examples.

## 👥 User Roles & Demo Credentials

### Administrator
- **Username**: `admin1`
- **Password**: `admin123`
- **Capabilities**: 
  - View all uploaded papers
  - Release chaos keys at scheduled times
  - Verify paper integrity
  - Monitor security logs

### Faculty
- **Username**: `faculty1`
- **Password**: `faculty123`
- **Capabilities**:
  - Upload exam papers (PDF/DOCX)
  - View scrambling process
  - Cannot decrypt or access papers after upload

### Exam Center
- **Username**: `center1`
- **Password**: `center123`
- **Capabilities**:
  - Download scrambled papers
  - Decrypt papers when keys are released
  - View only - cannot upload or manage

## 📋 Usage Workflow

### 1. Faculty Upload Process
1. Login as faculty user
2. Select exam paper (PDF or DOCX)
3. Enter exam title and optional description
4. Click "Secure Upload"
5. System automatically:
   - Converts PDF to images
   - Applies chaotic pixel scrambling
   - Computes SHA-256 hashes
   - Encrypts metadata with Paillier
   - Stores encrypted chaos key

### 2. Admin Management
1. Login as admin user
2. View all uploaded papers in dashboard
3. Verify paper integrity using SHA-256 hashes
4. Release chaos keys at scheduled exam times
5. Monitor all system activity through security logs

### 3. Exam Center Access
1. Login as exam center user
2. Download scrambled papers (unreadable)
3. Wait for admin to release chaos key
4. Decrypt papers when key becomes available
5. Access original readable exam papers

## 🔧 Technical Implementation

### Cryptographic Components

#### Chaotic Pixel Scrambling
```python
# Logistic Map for pixel permutation
x_new = r * x * (1 - x)

# Arnold Cat Map for coordinate transformation
x_new = (x + a * y) % N
y_new = (b * x + (a * b + 1) * y) % N
```

#### Homomorphic Encryption
- Uses Paillier encryption for metadata
- Allows encrypted counter increments
- Preserves privacy of access patterns

#### Hash Chain Logging
```python
hash_new = SHA256(prev_hash + log_data)
```

### File Structure
```
edusecure/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── auth.py             # User authentication
│   ├── chaotic.py          # Pixel scrambling algorithms
│   ├── upload.py           # File upload processing
│   ├── hashing.py          # SHA-256 operations
│   ├── phe_wrapper.py      # Homomorphic encryption
│   ├── timelock.py         # Time-based access control
│   ├── logs.py             # Tamper-proof logging
│   └── examcenter.py       # Exam center operations
├── papers/                 # Encrypted exam papers
├── users/                  # User credentials
├── logs/                   # Security audit logs
├── config/                 # System configuration
└── src/                    # React frontend
```

## 🧪 Demo Scenarios

### 1. Unauthorized Early Access
- Exam center downloads scrambled file
- Attempts to view before scheduled time
- Paper remains unreadable without chaos key
- Access attempt logged in security audit

### 2. Integrity Verification
- Admin runs integrity check
- System recomputes SHA-256 hashes
- Compares with stored values
- Detects any tampering attempts

### 3. Time-Lock Release
- Papers uploaded with future schedule time
- Decryption denied before scheduled time
- Admin releases key at exact scheduled time
- Papers become readable for exam centers

### 4. Tamper Detection
- Modify any log entry manually
- System detects broken hash chain
- Alerts admin of tampering attempt
- Maintains audit trail integrity

## 🔍 Security Analysis

### Confidentiality
- Chaotic scrambling makes papers unreadable
- Chaos keys encrypted with strong cryptography
- Time-lock prevents premature access

### Integrity
- SHA-256 hashing detects any modifications
- Hash chain prevents log tampering
- Cryptographic signatures ensure authenticity

### Availability
- File-based storage (no database dependencies)
- Redundant verification mechanisms
- Graceful error handling and recovery

### Auditability
- Complete activity logging
- Tamper-proof hash chains
- Role-based access tracking
- Cryptographic proof of operations

## 🛠️ Development

### Adding New Features
1. Backend: Add new endpoints in `app.py`
2. Frontend: Create new components in `src/components/`
3. Security: Update logging in relevant modules
4. Testing: Add test cases for new functionality

### Configuration
- User credentials: `users/users.json`
- System settings: `config/system_config.json`
- Paillier keys: `config/phe_keys.pkl`

## 📚 Dependencies

### Backend
- Flask 3.0.0 - Web framework
- Flask-Login 0.6.3 - Session management
- pdf2image 1.16.3 - PDF to image conversion
- Pillow 10.1.0 - Image processing
- NumPy 1.24.3 - Numerical operations
- phe 1.5.0 - Homomorphic encryption (Paillier)
- PyCryptodome 3.19.0 - RSA key protection

### Frontend
- React 18.3.1 - UI framework
- TypeScript 5.8.3 - Type safety
- Vite 5.4.19 - Build tool
- shadcn/ui - UI components
- Tailwind CSS - Styling

## 🙏 Acknowledgments

- Paillier homomorphic encryption implementation
- Arnold Cat Map and Logistic Map research
- shadcn/ui for beautiful React components
- Flask community for excellent documentation

---

**Note**: This is a demonstration system for educational purposes. For production use, additional security measures and thorough security auditing would be required.
