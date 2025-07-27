@echo off
REM eJAEGIS Auto-Start Script
REM This script can be placed in Windows Startup folder to automatically start eJAEGIS

REM Change to the eJAEGIS directory
cd /d "C:\Users\Lenovo ThinkPad T480\Desktop\JAEGIS\JAEGIS-METHOD"

REM Wait a bit for system to fully boot
timeout /t 30 /nobreak >nul

REM Start eJAEGIS Background Runner
python eJAEGIS-background-runner.py start

REM Optional: Show a notification that eJAEGIS started
echo eJAEGIS Auto-Sync started successfully > "%TEMP%\eJAEGIS-startup.log"
