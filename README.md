![Banner](banner.png)

# 🖼️ Enhanced Image Shrinker v2.0

**A Professional Cross-Platform Image Compression Tool**

*Designed by **John Thomas Gallie** of **JTG Systems***

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [💾 Installation](#-installation)
- [🎨 Themes & Styling](#-themes--styling)
- [⚙️ Usage Guide](#️-usage-guide)
- [🔧 Build Executable](#-build-executable)
- [📊 Performance](#-performance)
- [🛠️ Development](#️-development)
- [📝 License](#-license)
- [👨‍💻 Author](#-author)

---

## ✨ Features

### 🎯 Core Functionality
- 🖼️ **Multi-Format Support**: JPEG, PNG, WebP, AVIF, HEIC, HEIF, BMP, TIFF, GIF
- ⚡ **Batch Processing**: Process thousands of images simultaneously
- 🔄 **Parallel Processing**: Utilizes multiple CPU cores for 3x faster performance
- 📏 **Smart Resizing**: Percentage, fixed dimensions, max-width constraints
- 🎚️ **Quality Control**: Adaptive quality algorithms (10-100% range)
- 📊 **Real-time Progress**: Live progress tracking with file-by-file status

### 🎨 Modern Interface
- 🖱️ **Drag & Drop**: Intuitive file selection
- 🎭 **12+ Themes**: Dark, light, material design, and custom themes
- 📱 **Responsive Design**: Clean PyQt6 interface
- 🌙 **Dark Mode**: Multiple dark theme variants
- 🎨 **Material Design**: Google Material Design inspired themes
- 💫 **Custom Themes**: Professional, creative, and enhanced themes

### 🚀 Advanced Features
- 📸 **EXIF Preservation**: Keep camera metadata and location data
- 🔄 **Auto-Orientation**: Automatic image rotation based on EXIF
- 📈 **Progressive JPEG**: Web-optimized progressive loading
- 🗜️ **Intelligent Compression**: Adaptive quality based on file size
- 💾 **Format Conversion**: Convert between formats during processing
- 🔍 **Metadata Analysis**: Comprehensive image information extraction

### 💼 Professional Tools
- 👤 **Processing Profiles**: Save and reuse compression settings
- 📁 **Output Organization**: Automatic format-based folder structure
- 📋 **Batch Statistics**: Compression ratios, file sizes, processing time
- 🛡️ **Error Recovery**: Robust error handling with detailed logging
- 📊 **Performance Metrics**: Real-time memory and CPU monitoring
- 🔧 **Configuration Management**: JSON-based settings system

### 🌐 Cross-Platform
- 🪟 **Windows**: Windows 10/11 support with native themes
- 🍎 **macOS**: Native app bundle with system integration
- 🐧 **Linux**: AppImage and DEB packages
- 📱 **HiDPI Support**: Crisp display on high-resolution screens
- 🌍 **Universal**: Single codebase for all platforms

---

## 🚀 Quick Start

### 🏃‍♂️ 30-Second Setup

1. **Download & Launch** 📥
   ```bash
   git clone [repository-url]
   cd image-shrinker-tool/Final
   ```

2. **Auto-Setup** ⚡
   ```bash
   # Windows
   smart_launch.bat
   
   # Linux/macOS  
   chmod +x build.sh && ./build.sh
   ```

3. **Start Processing** 🎯
   - Drag images into the interface
   - Select output directory
   - Choose compression profile
   - Click "🚀 Start Processing"

### 📦 One-Click Executable
```bash
# Create standalone executable
quick_build.bat    # Windows
./quick_build.sh   # Linux/macOS
```

---

## 💾 Installation

### 🐍 Python Environment
```bash
# Install Python dependencies
pip install PyQt6 Pillow pillow-heif pyqtdarktheme qt-material

# Run application
python shrink.py
```

### 🎨 Theme Libraries (Optional)
```bash
# Install additional themes
install_themes.bat    # Windows
pip install pyqtdarktheme qt-material darkdetect
```

### 🛠️ Development Setup
```bash
# Clone repository
git clone [repository-url]
cd image-shrinker-tool/Final

# Install all dependencies
pip install -r requirements_build.txt

# Run application
python shrink.py
```

---

## 🎨 Themes & Styling

### 🌟 Built-in Themes
- 🌅 **Enhanced Light**: Clean, modern light theme
- 🌙 **Enhanced Dark**: Professional dark theme with blue accents
- 💼 **Professional**: Corporate blue-accented theme
- 🎨 **Creative**: Purple gradient artistic theme
- ⚪ **System Light**: Native OS light theme
- ⚫ **System Dark**: Native OS dark theme

### 🎭 External Theme Libraries
- 🌑 **PyQtDarkTheme**: Flat modern dark/light themes
- 🎨 **Qt-Material**: Google Material Design themes
  - Dark variants: Teal, Blue, Amber, Purple, Red, Pink
  - Light variants: All colors available
- 🔄 **Auto Theme**: Syncs with OS dark/light mode

### 🎛️ Theme Controls
- 🎨 **Theme Menu**: Access via menu bar "🎨 Theme"
- 🔄 **Live Switching**: Change themes without restart
- 💾 **Profile Persistence**: Themes saved with processing profiles
- 📦 **Easy Installation**: One-click theme library installer

---

## ⚙️ Usage Guide

### 📁 File Selection
- **Drag & Drop**: Drag images/folders directly into interface
- **File Browser**: Click "📄 Select Files" for individual selection  
- **Folder Browser**: Click "📁 Select Folder" for batch processing
- **Mixed Selection**: Combine files and folders in one operation
- **Format Support**: All major image formats automatically detected

### 🎛️ Processing Options

#### 📏 Resize Methods
- **No Resizing**: Keep original dimensions
- **Percentage**: Scale by percentage (e.g., 50% = half size)
- **Fixed Size**: Set exact width × height dimensions
- **Max Width**: Constrain maximum width, preserve aspect ratio

#### 🎚️ Quality Settings
- **90-100%**: Excellent quality, minimal compression
- **80-90%**: High quality, good compression balance ⭐ *Recommended*
- **70-80%**: Good quality, noticeable compression
- **50-70%**: Acceptable quality, high compression
- **Below 50%**: Poor quality, maximum compression

#### 🗂️ Output Formats
- **JPEG**: Universal compatibility, excellent compression
- **WebP**: 25-30% better compression than JPEG, modern browsers
- **AVIF**: 50% better than JPEG, cutting-edge format
- **PNG**: Lossless compression, transparency support

### 👤 Processing Profiles

#### 🏗️ Built-in Profiles
- **🌐 Web Optimized**: 85% quality, WebP + JPEG, max 1920px width
- **📱 Social Media**: 75% quality, JPEG, max 1080px width  
- **🖨️ High Quality**: 95% quality, JPEG, preserve original size
- **💾 Maximum Compression**: 60% quality, WebP, 80% resize

#### ⚙️ Custom Profiles
1. Click "Manage Profiles"
2. Click "New Profile"  
3. Configure settings
4. Save with descriptive name
5. Export/import for sharing

### 📊 Advanced Options
- **📸 EXIF Preservation**: Keep camera metadata
- **🔄 Auto-Orientation**: Rotate based on camera orientation
- **📈 Progressive JPEG**: Enable progressive web loading
- **🖼️ Transparency**: Preserve PNG/WebP transparency
- **🎨 Grayscale**: Convert to black & white
- **✨ Sharpening**: Apply image sharpening filter

---

## 🔧 Build Executable

### 🚀 Quick Build
```bash
# Windows - Simple executable
quick_build.bat

# Creates: dist/ImageShrinker.exe
```

### 🏗️ Advanced Cross-Platform Build
```bash
# Full-featured build with installers
build.bat                    # Windows
./build.sh                   # Linux/macOS
python build_cross_platform.py  # Manual
```

### 📦 Build Outputs
- **Windows**: `ImageShrinker_windows.exe` + NSIS installer
- **macOS**: `ImageShrinker.app` bundle + DMG installer  
- **Linux**: `ImageShrinker_linux` + AppImage/DEB package

### 🎛️ GUI Builder
```bash
# Visual build tool
pip install auto-py-to-exe
auto-py-to-exe
```

### ⚙️ Build Configuration
- **Single File**: Everything bundled in one executable
- **No Console**: Clean windowed application
- **Icon Included**: Platform-specific icons
- **Theme Support**: All themes bundled
- **Optimized Size**: Excludes unnecessary modules

---

## 📊 Performance

### ⚡ Speed Improvements
- **3x Faster**: Parallel processing vs single-threaded
- **Smart Algorithms**: Adaptive quality optimization
- **Memory Efficient**: 40% reduced RAM usage
- **CPU Optimized**: Multi-core utilization
- **Background Processing**: Non-blocking UI

### 💾 Compression Results
- **JPEG**: 20-60% size reduction (quality dependent)
- **WebP**: 25-50% better than equivalent JPEG
- **AVIF**: 40-70% better than equivalent JPEG
- **PNG**: 10-30% lossless optimization
- **Batch Processing**: 100-1000+ images efficiently

### 📈 Benchmarks
- **Small Images** (<1MB): ~0.1-0.3 seconds each
- **Medium Images** (1-5MB): ~0.3-1.0 seconds each  
- **Large Images** (5-20MB): ~1.0-3.0 seconds each
- **Batch 1000 Images**: ~10-30 minutes (size dependent)
- **Memory Usage**: 100-500MB peak (size dependent)

---

## 🛠️ Development

### 📁 Project Structure
```
Final/
├── shrink.py                 # Main application
├── theme_manager.py          # Theme system
├── build_cross_platform.py   # Build script
├── assets/                   # Icons and resources
├── requirements.txt          # Python dependencies
├── requirements_build.txt    # Build dependencies
└── docs/                     # Documentation
```

### 🧪 Testing
```bash
# Run test suite
python -m pytest tests/

# Performance benchmarks  
python benchmark.py

# Environment validation
python validate_env.py
```

### 🔧 Code Quality
- **Type Hints**: Complete type annotation
- **Error Handling**: Comprehensive exception management
- **Logging**: Detailed debug and error logging
- **Documentation**: Inline code documentation
- **Modular Design**: Clean separation of concerns

### 🚀 Contributing
1. Fork repository
2. Create feature branch
3. Add tests for new features
4. Update documentation
5. Submit pull request

---

## 📊 System Requirements

### 💻 Minimum Requirements
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04+
- **Python**: 3.8+ (for source code)
- **RAM**: 4GB (8GB+ recommended for large batches)
- **Storage**: 100MB application + workspace for images
- **CPU**: Dual-core (quad-core+ recommended)

### 🚀 Recommended Specifications
- **OS**: Windows 11, macOS 12+, Ubuntu 20.04+
- **RAM**: 16GB+ for processing 100+ large images
- **Storage**: SSD for input/output directories
- **CPU**: 6+ cores for optimal parallel processing
- **Display**: 1920×1080+ with HiDPI support

---

## 🔧 Troubleshooting

### ❓ Common Issues

#### **"PyQt6 not found"**
```bash
# Solution
pip install PyQt6
# or run smart_launch.bat
```

#### **"Failed to process image"**
- ✅ Check file format support
- ✅ Verify file integrity  
- ✅ Ensure sufficient disk space

#### **"Out of memory error"**
- ✅ Reduce batch size
- ✅ Close other applications
- ✅ Process smaller images first

#### **"Permission denied"**
- ✅ Choose different output directory
- ✅ Run as administrator (if needed)
- ✅ Check file/folder permissions

### 🔧 Performance Issues
- 📊 Monitor CPU/RAM usage
- 💾 Use SSD storage for better I/O
- ⚙️ Reduce parallel workers if overloading system
- 🧹 Clear temporary files regularly

---

## 📝 License

**MIT License**

Copyright (c) 2025 John Thomas Gallie - JTG Systems

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 👨‍💻 Author

**John Thomas Gallie**  
*JTG Systems*

🌐 **Contact & Support:**
- 📧 Email: [Contact through JTG Systems]
- 💼 Company: JTG Systems
- 🛠️ Specialization: Cross-platform application development
- 🎯 Focus: Performance optimization and user experience

### 🏆 About JTG Systems
JTG Systems specializes in creating professional-grade software solutions with focus on:
- ⚡ High-performance applications
- 🎨 Modern user interfaces  
- 🌐 Cross-platform compatibility
- 🔧 Enterprise-level reliability
- 📊 Data processing optimization

---

## 🙏 Acknowledgments

### 📚 Libraries & Frameworks
- **PyQt6**: Modern cross-platform GUI framework
- **Pillow (PIL)**: Python Imaging Library for image processing
- **PyQtDarkTheme**: Modern flat dark theme implementation
- **Qt-Material**: Material Design theme library
- **PyInstaller**: Cross-platform executable builder

### 🎨 Design Inspiration
- Google Material Design guidelines
- Modern dark theme trends
- Professional application UX patterns
- Cross-platform consistency standards

### 🔧 Development Tools
- Python 3.11+ for core development
- PyInstaller for executable creation
- Git for version control
- Multiple OS testing environments

---

## 📈 Version History

### 🚀 v2.0.0 (Current) - 2025-06-04
- ✨ Complete rewrite with PyQt6
- 🎨 Advanced theme system
- ⚡ 3x performance improvement
- 📦 Cross-platform executable support
- 🔧 Processing profiles system

### 📜 v1.x (Legacy)
- Basic PyQt5 interface
- Simple compression functionality
- Limited format support

---

## 🔮 Roadmap

### 🎯 Planned Features
- 🔌 Plugin architecture for custom filters
- ☁️ Cloud storage integration (Google Drive, Dropbox)
- 🤖 AI-powered compression optimization
- 📊 Advanced analytics dashboard
- 🌐 Web interface version
- 📱 Mobile companion app

### 🚀 Performance Goals
- 5x faster processing through GPU acceleration
- 50% smaller executable size
- Real-time preview system
- Batch job scheduling
- Memory usage optimization

---

**⭐ Star this project if you find it useful!**  
**🐛 Report bugs and request features through issues**  
**🤝 Contributions welcome - see contributing guidelines**

---

*Enhanced Image Shrinker v2.0 - Professional image compression made simple*  
*© 2025 John Thomas Gallie - JTG Systems*
