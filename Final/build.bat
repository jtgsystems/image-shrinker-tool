@echo off
setlocal enabledelayedexpansion

title Cross-Platform Executable Builder
echo 🚀 Cross-Platform Image Shrinker Builder
echo ==========================================
echo.

REM Smart Python detection (avoiding Inkscape)
echo 🐍 Finding suitable Python installation...

set "WORKING_PYTHON="

REM Define potential Python paths
set "PATHS="
set "PATHS=!PATHS!;%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
set "PATHS=!PATHS!;%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
set "PATHS=!PATHS!;%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
set "PATHS=!PATHS!;C:\Python312\python.exe"
set "PATHS=!PATHS!;C:\Python311\python.exe"
set "PATHS=!PATHS!;C:\Python310\python.exe"

REM Test each potential path
for %%P in (%PATHS%) do (
    if exist "%%P" (
        echo Testing: %%P
        "%%P" --version >nul 2>&1
        if not errorlevel 1 (
            "%%P" -m pip --version >nul 2>&1
            if not errorlevel 1 (
                set "WORKING_PYTHON=%%P"
                echo ✅ Found working Python with pip: %%P
                goto :found_python
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
                goto :found_python
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

:found_python
echo.
echo 🏗️ Starting build process with: %WORKING_PYTHON%
"%WORKING_PYTHON%" build_cross_platform.py

echo.
echo ✅ Build process complete!
echo 📁 Check dist/ folder for executable
pause
