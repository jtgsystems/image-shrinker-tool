@echo off
title Image Shrinker - Environment Fix
echo 🔧 Fixing Python Environment Issue
echo =====================================
echo.

REM Check if running from Inkscape Python (problematic)
echo %~dp0 | findstr /i "inkscape" >nul
if not errorlevel 1 (
    echo ⚠️ Detected Inkscape Python environment
    echo This may cause issues. Looking for system Python...
)

REM Try to find system Python
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ System Python not found in PATH
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Get Python path
for /f "tokens=*" %%i in ('where python') do (
    set PYTHON_PATH=%%i
    goto :found_python
)

:found_python
echo ✅ Found Python: %PYTHON_PATH%

REM Check if it's the problematic Inkscape Python
echo %PYTHON_PATH% | findstr /i "inkscape" >nul
if not errorlevel 1 (
    echo ⚠️ This is Inkscape Python - searching for alternatives...
    
    REM Try common Python locations
    if exist "C:\Python3*\python.exe" (
        for /d %%d in (C:\Python3*) do (
            set PYTHON_PATH=%%d\python.exe
            goto :use_python
        )
    )
    
    if exist "%LOCALAPPDATA%\Programs\Python\Python*\python.exe" (
        for /d %%d in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
            set PYTHON_PATH=%%d\python.exe
            goto :use_python
        )
    )
    
    echo ❌ Could not find alternative Python installation
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:use_python
echo 🐍 Using Python: %PYTHON_PATH%

REM Check pip
"%PYTHON_PATH%" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip not available. Installing pip...
    "%PYTHON_PATH%" -m ensurepip --upgrade
)

echo 📦 Installing required packages...
"%PYTHON_PATH%" -m pip install --upgrade pip
"%PYTHON_PATH%" -m pip install PyQt6 Pillow pillow-heif

if errorlevel 1 (
    echo ⚠️ PyQt6 failed, trying PyQt5...
    "%PYTHON_PATH%" -m pip install PyQt5
)

echo.
echo ✅ Installation complete!
echo 🚀 Starting Image Shrinker...
echo.

"%PYTHON_PATH%" "%~dp0shrink.py"

echo.
echo 📝 If issues persist:
echo 1. Install Python from python.org
echo 2. Add Python to system PATH
echo 3. Restart command prompt
echo.
pause
