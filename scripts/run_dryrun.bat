
@echo off
cd /d "%~dp0"
echo DRY_RUN=true (from .env) - starting bot...
python auto_trade_ib.py
