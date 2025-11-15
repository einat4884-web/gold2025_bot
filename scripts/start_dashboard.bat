@echo off
cd /d "%~dp0"
cd ..
echo Starting Streamlit dashboard...
start "" streamlit run dashboard2025.py --server.headless=true
pause
