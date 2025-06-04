@echo off
title Install PyQt6 Theme Libraries
echo 🎨 Installing PyQt6 Theme Libraries
echo ==================================
echo.

echo 📦 Installing PyQtDarkTheme...
pip install pyqtdarktheme

echo 📦 Installing Qt-Material...
pip install qt-material

echo 📦 Installing additional styling tools...
pip install darkdetect

echo.
echo ✅ Theme installation complete!
echo.
echo 🎨 Available themes:
echo   • PyQtDarkTheme: Modern flat dark/light themes
echo   • Qt-Material: Material Design inspired themes  
echo   • Custom: Enhanced built-in themes
echo.
pause
