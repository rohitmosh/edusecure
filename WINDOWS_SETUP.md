# 🪟 Windows Setup Guide for EduSecure

If you're having issues with the automated startup scripts, follow this manual setup guide.

## 📋 Prerequisites

1. **Python 3.10+** - Download from [python.org](https://www.python.org/downloads/)
2. **Node.js 18+** - Download from [nodejs.org](https://nodejs.org/)
3. **Git** (optional) - For cloning the repository

## 🚀 Quick Setup Options

### Option 1: Windows Batch File (Easiest)
```cmd
start.bat
```
Double-click the `start.bat` file or run it from Command Prompt.

### Option 2: Simple Python Script
```cmd
python quick_start.py
```
This uses your system Python without virtual environments.

### Option 3: Manual Setup (Most Control)

#### Step 1: Setup Backend
```cmd
cd backend
python -m pip install -r requirements.txt
python run.py
```
Keep this terminal open - backend will run at http://localhost:5000

#### Step 2: Setup Frontend (New Terminal)
```cmd
npm install
npm run dev
```
Keep this terminal open - frontend will run at http://localhost:5173

#### Step 3: Open Browser
Navigate to: http://localhost:5173

## 🔧 Troubleshooting

### Python Issues
- **"Python not found"**: Install Python from python.org and add to PATH
- **"pip not found"**: Run `python -m ensurepip --upgrade`
- **Permission errors**: Run Command Prompt as Administrator

### Node.js Issues
- **"npm not found"**: Install Node.js from nodejs.org
- **"node not found"**: Restart Command Prompt after Node.js installation

### Dependency Issues
- **Backend dependencies fail**: Try `python -m pip install --upgrade pip` first
- **Frontend dependencies fail**: Try `npm cache clean --force` then `npm install`

### Port Issues
- **Port 5000 busy**: Kill process using `netstat -ano | findstr :5000` then `taskkill /PID <PID> /F`
- **Port 5173 busy**: Kill process using `netstat -ano | findstr :5173` then `taskkill /PID <PID> /F`

## 🎯 Demo Credentials

Once running, use these credentials to test different roles:

| Role | Username | Password | Access |
|------|----------|----------|---------|
| **Admin** | `admin1` | `admin123` | Full control, key management |
| **Faculty** | `faculty1` | `faculty123` | Upload exam papers |
| **Exam Center** | `center1` | `center123` | Download & decrypt papers |

## 🔐 Security Features Demo

To see all cryptographic features in action:
```cmd
python demo_security_features.py
```

This will demonstrate:
- Chaotic pixel scrambling
- RSA key protection
- Homomorphic encryption
- SHA-256 integrity verification
- Tamper-proof logging
- Time-lock access control

## 📁 Project Structure

```
edusecure/
├── backend/           # Python Flask API
├── src/              # React frontend
├── start.py          # Automated startup (with venv)
├── quick_start.py    # Simple startup (system Python)
├── start.bat         # Windows batch file
└── demo_security_features.py  # Security demo
```

## 💡 Tips

1. **Use Command Prompt or PowerShell** - Don't use Git Bash for Windows-specific commands
2. **Run as Administrator** if you encounter permission issues
3. **Check Windows Defender** - It might block some operations
4. **Use the batch file** for the easiest setup experience
5. **Keep terminals open** - Both backend and frontend need to stay running

## 🆘 Still Having Issues?

1. Try the **batch file method** first: `start.bat`
2. If that fails, try **quick start**: `python quick_start.py`
3. As a last resort, use **manual setup** with the step-by-step commands above

The application should open automatically in your browser at http://localhost:5173 once both servers are running.