@echo off
cd /d "%~dp0"
cd ..
python scripts\auto_trade_ib.py
pause
