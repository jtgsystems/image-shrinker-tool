#!/bin/bash
# Cross-platform build script for Unix systems

echo "🚀 Cross-Platform Image Shrinker Builder"
echo "========================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

echo "📦 Installing build dependencies..."
python3 -m pip install PyInstaller auto-py-to-exe pyqtdarktheme qt-material

echo "🏗️ Building executable..."
python3 build_cross_platform.py

echo ""
echo "✅ Build process complete!"
echo "📁 Check dist/ folder for executable"
