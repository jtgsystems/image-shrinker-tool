@echo off
echo Installing PyQt6 and dependencies...
pip install --upgrade pip
pip install PyQt6 Pillow pillow-heif
echo.
echo Dependencies installed successfully!
echo Now you can run shrink.py
pause
