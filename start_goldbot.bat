@echo off
echo Starting Gold2025 System...

:: Move to main project folder
cd /d "%~dp0"

:: Start dashboard
start "" scripts\start_dashboard.bat

:: Start trading bot
start "" scripts\run_bot.bat

echo All systems started successfully.
pause
