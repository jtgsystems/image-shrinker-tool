@echo off
setlocal enabledelayedexpansion

title Image Shrinker - Python Environment Selector
echo 🐍 Python Environment Selector
echo ================================
echo.

REM Define potential Python paths
set "PATHS="
set "PATHS=!PATHS!;%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
set "PATHS=!PATHS!;%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
set "PATHS=!PATHS!;%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
set "PATHS=!PATHS!;C:\Python312\python.exe"
set "PATHS=!PATHS!;C:\Python311\python.exe"
set "PATHS=!PATHS!;C:\Python310\python.exe"

REM Find working Python
set "WORKING_PYTHON="
for %%P in (%PATHS%) do (
    if exist "%%P" (
        echo Testing: %%P
        "%%P" --version >nul 2>&1
        if not errorlevel 1 (
            "%%P" -m pip --version >nul 2>&1
            if not errorlevel 1 (
                set "WORKING_PYTHON=%%P"
                echo ✅ Found working Python with pip: %%P
                goto :install_deps
            )
        )
    )
)

REM Try system PATH Python (avoiding Inkscape)
for /f "tokens=*" %%i in ('where python 2^>nul') do (
    echo %%i | findstr /i "inkscape" >nul
    if errorlevel 1 (
        echo Testing: %%i
        "%%i" --version >nul 2>&1
        if not errorlevel 1 (
            "%%i" -m pip --version >nul 2>&1
            if not errorlevel 1 (
                set "WORKING_PYTHON=%%i"
                echo ✅ Found working Python: %%i
                goto :install_deps
            )
        )
    )
)

echo ❌ No suitable Python found with pip
echo.
echo 📋 Solutions:
echo 1. Install Python from https://python.org
echo 2. Ensure "Add Python to PATH" is checked during installation
echo 3. Restart command prompt after installation
pause
exit /b 1

:install_deps
echo.
echo 📦 Installing dependencies with: %WORKING_PYTHON%
"%WORKING_PYTHON%" -m pip install --upgrade pip
"%WORKING_PYTHON%" -m pip install PyQt6 Pillow pillow-heif

if errorlevel 1 (
    echo ⚠️ PyQt6 failed, trying PyQt5...
    "%WORKING_PYTHON%" -m pip install PyQt5
)

echo.
echo 🚀 Starting Image Shrinker...
"%WORKING_PYTHON%" "%~dp0shrink.py"

pause
