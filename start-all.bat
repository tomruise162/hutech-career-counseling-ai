@echo off
echo Starting HUTECH Career Counseling System...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)
echo Python: 
python --version

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)
echo Node.js: 
node --version

REM Create .env file if not exists
if not exist "backend\.env" (
    echo Creating .env file...
    copy "env.example" "backend\.env"
    echo Please update OPENAI_API_KEY in backend\.env file
)

REM Install/Update Python dependencies
echo Installing Python dependencies...
cd backend
pip install -r requirements.txt --upgrade
python init_data.py
cd ..

REM Start backend
echo Starting backend server...
start "Backend Server" cmd /k "cd backend && python main.py"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend
echo Starting frontend server...
start "Frontend Server" cmd /k "cd frontend/hutech-consultation && npm start"

echo.
echo System started successfully!
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo HuNext AI Career Counseling is ready!
echo.
echo To stop the system, close the opened command windows
echo Support: tuyensinh@hutech.edu.vn ^| 028 5445 7777
echo.
pause
