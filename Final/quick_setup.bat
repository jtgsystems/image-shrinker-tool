@echo off
echo 🚀 Quick Image Shrinker - Auto Setup
echo =====================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

echo Installing required packages...
pip install --upgrade pip
pip install PyQt6 Pillow pillow-heif

if errorlevel 1 (
    echo ⚠️ PyQt6 failed, trying PyQt5...
    pip install PyQt5
)

echo.
echo ✅ Dependencies installed!
echo.
echo Starting application...
python shrink_fixed.py

pause
