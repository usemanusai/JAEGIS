@echo off
REM eJAEGIS Setup with Integrated Failsafe System
cd /d "%~dp0"

echo 🚀 eJAEGIS Setup with Failsafe System
echo ==================================
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

REM Check and install required packages
echo 📦 Checking required packages...

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

python -c "import psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Installing psutil (required for failsafe system)...
    pip install psutil
    if %errorlevel% neq 0 (
        echo ❌ Failed to install psutil
        pause
        exit /b 1
    )
)

echo ✅ Required packages available

REM Check if required files exist
echo 📁 Checking required files...

set "required_files=eJAEGIS-auto-sync.py eJAEGIS_auto_sync.py eJAEGIS-background-runner.py eJAEGIS-failsafe-system.py eJAEGIS-failsafe-cli.py"

for %%f in (%required_files%) do (
    if not exist "%%f" (
        echo ❌ %%f not found
        pause
        exit /b 1
    )
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
echo 🔧 Testing Failsafe System...

REM Test failsafe system
python eJAEGIS-failsafe-cli.py test
if %errorlevel% neq 0 (
    echo ⚠️ Failsafe test had issues, but continuing...
) else (
    echo ✅ Failsafe system test successful
)

echo.
echo 🚀 Starting eJAEGIS with Failsafe System...

REM Start the background runner (now includes failsafe)
python eJAEGIS-background-runner.py start

echo.
echo 📊 Checking status...
python eJAEGIS-background-runner.py status

echo.
echo 🛡️ Failsafe System Status...
python eJAEGIS-failsafe-cli.py status

echo.
echo 🎉 eJAEGIS Setup with Failsafe System Complete!
echo.
echo ============================================
echo 📋 Available Commands:
echo ============================================
echo.
echo eJAEGIS Background Runner:
echo   python eJAEGIS-background-runner.py start     - Start monitoring
echo   python eJAEGIS-background-runner.py stop      - Stop monitoring
echo   python eJAEGIS-background-runner.py status    - Check status
echo   python eJAEGIS-background-runner.py restart   - Restart monitoring
echo.
echo Failsafe System:
echo   python eJAEGIS-failsafe-cli.py status         - Show failsafe status
echo   python eJAEGIS-failsafe-cli.py test           - Run failsafe tests
echo   python eJAEGIS-failsafe-cli.py config         - Show configuration
echo.
echo Failsafe Controls:
echo   python eJAEGIS-failsafe-cli.py /disable-eJAEGIS-init-check
echo   python eJAEGIS-failsafe-cli.py /enable-eJAEGIS-init-check
echo   python eJAEGIS-failsafe-cli.py /disable-completion-check
echo   python eJAEGIS-failsafe-cli.py /enable-completion-check
echo.
echo ============================================
echo 🛡️ Failsafe Features Enabled:
echo ============================================
echo.
echo ✅ Failsafe 1: Uninitialized eJAEGIS Detection
echo    - Detects development without active eJAEGIS
echo    - Prompts for eJAEGIS initialization
echo    - Auto-detects new projects and Git repos
echo.
echo ✅ Failsafe 2: Post-Completion Development Detection
echo    - Detects development after project completion
echo    - Prompts for status clarification
echo    - Suggests feature branches or project reopening
echo.
echo ============================================
echo 📊 System Status:
echo ============================================
echo.
echo The eJAEGIS Auto-Sync system is now running with integrated failsafe protection!
echo.
echo Key Benefits:
echo • Automatic detection of workflow issues
echo • Proactive warnings and guidance
echo • Prevention of development disruptions
echo • Intelligent project status management
echo.
echo The system will:
echo • Monitor file changes continuously
echo • Detect when eJAEGIS isn't running during development
echo • Alert about post-completion development activity
echo • Provide actionable options for resolution
echo.
echo To stop: python eJAEGIS-background-runner.py stop
echo To check status: python eJAEGIS-background-runner.py status
echo To manage failsafes: python eJAEGIS-failsafe-cli.py status
echo.
pause
