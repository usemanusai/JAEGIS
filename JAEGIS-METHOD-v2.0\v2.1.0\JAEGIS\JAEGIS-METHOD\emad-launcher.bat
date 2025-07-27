@echo off
REM eJAEGIS Auto-Sync Launcher - Can be run from anywhere
REM This script automatically finds and runs eJAEGIS scripts from the correct directory

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo 🚀 eJAEGIS Auto-Sync Launcher
echo =========================
echo Script Directory: %SCRIPT_DIR%
echo Current Directory: %CD%
echo.

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Check what the user wants to do
if "%1"=="" goto :show_menu
if "%1"=="install" goto :install_service
if "%1"=="start" goto :start_service
if "%1"=="stop" goto :stop_service
if "%1"=="status" goto :status_service
if "%1"=="remove" goto :remove_service
if "%1"=="debug" goto :debug_service
if "%1"=="test" goto :test_service
if "%1"=="troubleshoot" goto :troubleshoot
if "%1"=="create-repo" goto :create_repo
if "%1"=="simple" goto :simple_setup
if "%1"=="background" goto :background_runner
goto :show_menu

:show_menu
echo Available Commands:
echo.
echo   simple        - Simple setup (Background Runner - Recommended)
echo   background    - Manage background runner (start/stop/status)
echo   install       - Install eJAEGIS Auto-Sync Windows Service
echo   start         - Start the service
echo   stop          - Stop the service
echo   status        - Check service status
echo   remove        - Remove the service
echo   debug         - Run service in debug mode (foreground)
echo   test          - Run a single test cycle
echo   troubleshoot  - Run diagnostic tests
echo   create-repo   - Create eJAEGIS repository on GitHub
echo.
echo Usage: %~nx0 [command]
echo Example: %~nx0 install
echo.
pause
goto :end

:install_service
echo 🔧 Installing eJAEGIS Auto-Sync Service...
call "%SCRIPT_DIR%\install-eJAEGIS-service.bat"
goto :end

:start_service
echo ▶️ Starting eJAEGIS Auto-Sync Service...
python "%SCRIPT_DIR%\eJAEGIS-service-manager.py" start
goto :end

:stop_service
echo ⏹️ Stopping eJAEGIS Auto-Sync Service...
python "%SCRIPT_DIR%\eJAEGIS-service-manager.py" stop
goto :end

:status_service
echo 📊 eJAEGIS Auto-Sync Service Status:
python "%SCRIPT_DIR%\eJAEGIS-service-manager.py" status
goto :end

:remove_service
echo 🗑️ Removing eJAEGIS Auto-Sync Service...
python "%SCRIPT_DIR%\eJAEGIS-service-manager.py" remove
goto :end

:debug_service
echo 🐛 Running eJAEGIS Auto-Sync in Debug Mode...
python "%SCRIPT_DIR%\eJAEGIS-auto-sync-service.py" debug
goto :end

:test_service
echo 🧪 Running eJAEGIS Auto-Sync Test Cycle...
python "%SCRIPT_DIR%\eJAEGIS-auto-sync.py" --test
goto :end

:troubleshoot
echo 🔍 Running eJAEGIS Diagnostics...
python "%SCRIPT_DIR%\troubleshoot-eJAEGIS.py"
goto :end

:create_repo
echo 🏗️ Creating eJAEGIS Repository...
echo.
echo Choose repository creation method:
echo   1. Node.js (Recommended)
echo   2. Python
echo   3. Cancel
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    if exist "%SCRIPT_DIR%\create-eJAEGIS-repository.js" (
        node "%SCRIPT_DIR%\create-eJAEGIS-repository.js"
    ) else (
        echo ❌ create-eJAEGIS-repository.js not found
    )
) else if "%choice%"=="2" (
    if exist "%SCRIPT_DIR%\create-eJAEGIS-repository.py" (
        python "%SCRIPT_DIR%\create-eJAEGIS-repository.py"
    ) else (
        echo ❌ create-eJAEGIS-repository.py not found
    )
) else (
    echo Operation cancelled
)
goto :end

:simple_setup
echo 🚀 Running Simple eJAEGIS Setup...
call "%SCRIPT_DIR%\setup-eJAEGIS-simple.bat"
goto :end

:background_runner
echo 🔧 eJAEGIS Background Runner Management
echo.
echo Available commands:
echo   1. Start background runner
echo   2. Stop background runner
echo   3. Check status
echo   4. Restart background runner
echo   5. Back to main menu
echo.
set /p bg_choice="Enter choice (1-5): "

if "%bg_choice%"=="1" (
    python "%SCRIPT_DIR%\eJAEGIS-background-runner.py" start
) else if "%bg_choice%"=="2" (
    python "%SCRIPT_DIR%\eJAEGIS-background-runner.py" stop
) else if "%bg_choice%"=="3" (
    python "%SCRIPT_DIR%\eJAEGIS-background-runner.py" status
) else if "%bg_choice%"=="4" (
    python "%SCRIPT_DIR%\eJAEGIS-background-runner.py" restart
) else if "%bg_choice%"=="5" (
    goto :show_menu
) else (
    echo Invalid choice
)
goto :end

:end
echo.
echo 🏁 Operation completed
if "%1"=="" pause
endlocal
