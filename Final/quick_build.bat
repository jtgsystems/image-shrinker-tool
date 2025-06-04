@echo off
title Quick Executable Builder (Simple)
echo 🚀 Quick Image Shrinker Executable Builder
echo ==========================================
echo.

REM Find working Python (same logic as smart_launch.bat)
setlocal enabledelayedexpansion

set "WORKING_PYTHON="
set "PATHS="
set "PATHS=!PATHS!;%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
set "PATHS=!PATHS!;%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
set "PATHS=!PATHS!;%LOCALAPPDATA%\Programs\Python\Python310\python.exe"

for %%P in (%PATHS%) do (
    if exist "%%P" (
        "%%P" --version >nul 2>&1
        if not errorlevel 1 (
            "%%P" -m pip --version >nul 2>&1
            if not errorlevel 1 (
                set "WORKING_PYTHON=%%P"
                echo ✅ Found Python: %%P
                goto :build
            )
        )
    )
)

echo ❌ No Python with pip found
pause
exit /b 1

:build
echo 📦 Installing PyInstaller...
"%WORKING_PYTHON%" -m pip install PyInstaller

echo 🏗️ Building executable (this may take a few minutes)...
"%WORKING_PYTHON%" -m PyInstaller --onefile --windowed --name "ImageShrinker" shrink.py

if exist "dist\ImageShrinker.exe" (
    echo ✅ Build successful!
    echo 📁 Executable created: dist\ImageShrinker.exe
) else (
    echo ❌ Build failed - check for errors above
)

pause
