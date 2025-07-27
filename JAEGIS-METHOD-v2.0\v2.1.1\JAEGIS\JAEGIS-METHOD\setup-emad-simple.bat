@echo off
REM Simple eJAEGIS Setup - Alternative to Windows Service
cd /d "%~dp0"

echo 🚀 eJAEGIS Simple Setup (Background Runner)
echo ========================================
echo Current Directory: %CD%
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

echo ✅ Python is available

REM Check required packages
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Installing requests...
    pip install requests
    if %errorlevel% neq 0 (
        echo ❌ Failed to install requests
        pause
        exit /b 1
    )
)

echo ✅ Required packages available

REM Check if required files exist
if not exist "eJAEGIS-auto-sync.py" (
    echo ❌ eJAEGIS-auto-sync.py not found
    pause
    exit /b 1
)

if not exist "eJAEGIS_auto_sync.py" (
    echo ❌ eJAEGIS_auto_sync.py not found
    pause
    exit /b 1
)

if not exist "eJAEGIS-background-runner.py" (
    echo ❌ eJAEGIS-background-runner.py not found
    pause
    exit /b 1
)

echo ✅ Required files found

echo.
echo 🧪 Testing eJAEGIS functionality...

REM Test authentication and basic functionality
python eJAEGIS-auto-sync.py --test
if %errorlevel% neq 0 (
    echo ❌ eJAEGIS test failed
    echo Please check your GitHub token and configuration
    pause
    exit /b 1
)

echo ✅ eJAEGIS test successful

echo.
echo 🚀 Starting eJAEGIS Background Runner...

REM Start the background runner
python eJAEGIS-background-runner.py start

echo.
echo 📊 Checking status...
python eJAEGIS-background-runner.py status

echo.
echo 🎉 eJAEGIS Simple Setup Complete!
echo.
echo Background Runner Commands:
echo   Start:   python eJAEGIS-background-runner.py start
echo   Stop:    python eJAEGIS-background-runner.py stop
echo   Status:  python eJAEGIS-background-runner.py status
echo   Restart: python eJAEGIS-background-runner.py restart
echo.
echo The eJAEGIS Auto-Sync is now running in the background!
echo It will automatically monitor for file changes and sync to GitHub.
echo.
echo To stop: python eJAEGIS-background-runner.py stop
echo To check status: python eJAEGIS-background-runner.py status
echo.
pause
