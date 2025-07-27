@echo off
echo 🚀 JAEGIS BULK UPLOAD STARTER
echo ==================================================

REM Set GitHub token (replace YOUR_TOKEN_HERE with actual token)
set GITHUB_TOKEN=YOUR_TOKEN_HERE

REM Set workspace path
set WORKSPACE_PATH=C:\Users\Lenovo ThinkPad T480\Desktop\JAEGIS

REM Set upload configuration
set BATCH_SIZE=50
set MAX_CONCURRENT=5
set RATE_LIMIT_DELAY=1.0
set ENABLE_DOCQA=true
set DRY_RUN=false
set PYTHONIOENCODING=utf-8

echo ✅ Environment configured
echo    Workspace: %WORKSPACE_PATH%
echo    Target: usemanusai/JAEGIS
echo    Batch Size: %BATCH_SIZE%
echo    DocQA Agent: %ENABLE_DOCQA%

echo.
echo ⚠️  IMPORTANT: Update GITHUB_TOKEN in this file before running!
echo.

REM Check if token is set
if "%GITHUB_TOKEN%"=="YOUR_TOKEN_HERE" (
    echo ❌ Please set your GitHub token in start_upload.bat
    pause
    exit /b 1
)

echo 🚀 Starting bulk upload automation...
python bulk_upload_automation.py

pause
