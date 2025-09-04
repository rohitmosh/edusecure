@echo off
echo 🔐 EduSecure-HE: Secure Exam Paper Management System
echo ============================================================
echo Starting application setup...
echo ============================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.10+ first.
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js 18+ first.
    pause
    exit /b 1
)

echo ✅ Python and Node.js found

REM Setup backend
echo.
echo 📦 Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔧 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo 📥 Installing Python packages...
call venv\Scripts\activate.bat
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Backend dependencies installed

REM Go back to root directory
cd ..

REM Setup frontend
echo.
echo 📦 Setting up frontend...
echo 📥 Installing Node.js packages...
call npm install

if errorlevel 1 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo ✅ Frontend dependencies installed

REM Ask about security demo
echo.
set /p demo="🔐 Would you like to run the security features demo first? (y/n): "
if /i "%demo%"=="y" (
    echo.
    echo 🚀 Running security demonstration...
    python demo_security_features.py
    echo.
    echo ✅ Security demo completed!
    pause
)

REM Start the application
echo.
echo 🚀 Starting EduSecure-HE application...
echo.
echo 📱 Frontend will be available at: http://localhost:5173
echo 🔧 Backend API will be available at: http://localhost:5000
echo.
echo 👥 Demo Credentials:
echo    Admin: admin1 / admin123
echo    Faculty: faculty1 / faculty123
echo    Exam Center: center1 / center123
echo.
echo ⚠️  Press Ctrl+C to stop the servers
echo ============================================================

REM Start backend in background
echo 🚀 Starting backend server...
cd backend
start "EduSecure Backend" cmd /k "venv\Scripts\activate.bat && python run.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Go back and start frontend
cd ..
echo 🚀 Starting frontend server...
start "EduSecure Frontend" cmd /k "npm run dev"

REM Wait a moment then open browser
timeout /t 5 /nobreak >nul
echo 🌐 Opening browser...
start http://localhost:5173

echo.
echo 🎉 EduSecure-HE is now running!
echo Close this window or press any key to exit setup.
pause >nul