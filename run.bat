@echo off
REM Quick start script for NextGen AI Assistant (Windows)

echo Starting NextGen AI Assistant...

REM Check if virtual environment exists
if not exist "env\" (
    echo Creating virtual environment...
    python -m venv env
)

REM Activate virtual environment
call env\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check for .env file
if not exist ".env" (
    echo Warning: .env file not found
    echo Creating from template...
    copy .env.example .env
    echo Please edit .env with your API keys
    pause
    exit /b 1
)

REM Start the application
echo Starting web server on http://localhost:5000
python app.py
