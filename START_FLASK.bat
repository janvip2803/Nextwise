@echo off
echo Starting NextWise Flask Backend...
echo.
cd /d "%~dp0backend"
pip install flask flask-mail flask-cors >nul 2>&1
echo Flask is starting on http://127.0.0.1:5000
echo Keep this window open while using the website.
echo.
python app.py
pause
