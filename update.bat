@echo off
title Gold2025 Auto Update
cd /d "C:\Users\haya1843\Downloads\Gold2025_Clean_IBKR"
echo.
echo =====================================
echo   Uploading latest changes to GitHub
echo =====================================
echo.
git add .
git commit -m "auto update"
git push
echo.
echo =====================================
echo   ? Update complete!
echo =====================================
pause
