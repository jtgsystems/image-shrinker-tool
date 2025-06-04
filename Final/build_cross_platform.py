#!/usr/bin/env python3
"""
Cross-Platform Build Script for Image Shrinker
==============================================
Builds executable for Windows, macOS, and Linux with smart Python detection
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def find_working_python():
    """Find a working Python installation with pip."""
    # Define potential Python paths
    potential_paths = [
        # User installations
        Path.home() / "AppData/Local/Programs/Python/Python312/python.exe",
        Path.home() / "AppData/Local/Programs/Python/Python311/python.exe", 
        Path.home() / "AppData/Local/Programs/Python/Python310/python.exe",
        # System installations
        Path("C:/Python312/python.exe"),
        Path("C:/Python311/python.exe"),
        Path("C:/Python310/python.exe"),
        # Unix paths
        Path("/usr/bin/python3"),
        Path("/usr/local/bin/python3"),
        Path("/opt/python3/bin/python3"),
    ]
    
    # Test each potential path
    for python_path in potential_paths:
        if python_path.exists():
            try:
                # Test Python and pip
                result = subprocess.run([str(python_path), "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    # Test pip
                    pip_result = subprocess.run([str(python_path), "-m", "pip", "--version"],
                                              capture_output=True, text=True, timeout=10)
                    if pip_result.returncode == 0:
                        print(f"✅ Found working Python with pip: {python_path}")
                        return str(python_path)
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                continue
    
    # Try system PATH Python (avoiding Inkscape)
    try:
        import shutil as sh
        python_path = sh.which("python")
        if python_path and "inkscape" not in python_path.lower():
            try:
                result = subprocess.run([python_path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    pip_result = subprocess.run([python_path, "-m", "pip", "--version"],
                                              capture_output=True, text=True, timeout=10)
                    if pip_result.returncode == 0:
                        print(f"✅ Found working system Python: {python_path}")
                        return python_path
            except:
                pass
        
        # Try python3
        python3_path = sh.which("python3")
        if python3_path:
            try:
                result = subprocess.run([python3_path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    pip_result = subprocess.run([python3_path, "-m", "pip", "--version"],
                                              capture_output=True, text=True, timeout=10)
                    if pip_result.returncode == 0:
                        print(f"✅ Found working Python3: {python3_path}")
                        return python3_path
            except:
                pass
    except:
        pass
    
    print("❌ No working Python installation with pip found!")
    print("📋 Solutions:")
    print("1. Install Python from https://python.org")
    print("2. Ensure 'Add Python to PATH' is checked during installation")
    print("3. Restart command prompt after installation")
    return None

def get_platform_info():
    """Get platform-specific build information."""
    system = platform.system().lower()
    
    if system == 'windows':
        return {
            'name': 'windows',
            'icon': 'assets/icon.ico',
            'exe_name': 'ImageShrinker_windows.exe',
            'installer_cmd': 'iscc setup_windows.iss'
        }
    elif system == 'darwin':
        return {
            'name': 'macos', 
            'icon': 'assets/icon.icns',
            'exe_name': 'ImageShrinker_macos',
            'installer_cmd': 'pkgbuild --root dist --identifier com.imagetools.shrinker ImageShrinker.pkg'
        }
    else:
        return {
            'name': 'linux',
            'icon': 'assets/icon.png', 
            'exe_name': 'ImageShrinker_linux',
            'installer_cmd': 'fpm -s dir -t deb -n imageshrinker dist/=/'
        }

def install_dependencies(python_exe):
    """Install build dependencies using specified Python executable."""
    print("📦 Installing build dependencies...")
    
    deps = [
        'PyInstaller>=5.13.0',
        'auto-py-to-exe>=2.40.0',
        'PyQt6>=6.4.0',
        'Pillow>=10.0.0',
        'pillow-heif>=0.10.0',
        'pyqtdarktheme>=2.1.0',
        'qt-material>=2.14'
    ]
    
    # Upgrade pip first
    try:
        subprocess.run([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True, timeout=60)
        print("✅ pip upgraded")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print("⚠️ pip upgrade failed, continuing...")
    
    # Install each dependency
    failed_deps = []
    for dep in deps:
        try:
            print(f"  Installing {dep}...")
            subprocess.run([python_exe, '-m', 'pip', 'install', dep], 
                          check=True, timeout=120)
            print(f"  ✅ {dep} installed")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            print(f"  ❌ Failed to install {dep}")
            failed_deps.append(dep)
    
    if failed_deps:
        print(f"⚠️ Some dependencies failed: {', '.join(failed_deps)}")
        print("Continuing with available dependencies...")
        return True  # Continue anyway
    
    print("✅ All dependencies installed successfully")
    return True

def create_assets():
    """Create necessary asset files."""
    print("🎨 Creating assets...")
    
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    # Create simple icon placeholder (SVG content for cross-platform)
    icon_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
    <rect width="256" height="256" fill="#1e40af" rx="32"/>
    <rect x="64" y="64" width="128" height="96" fill="#3b82f6" rx="8"/>
    <rect x="80" y="80" width="96" height="64" fill="#60a5fa" rx="4"/>
    <text x="128" y="200" text-anchor="middle" fill="white" font-family="Arial" font-size="24" font-weight="bold">IS</text>
</svg>'''
    
    # Save SVG icon
    with open(assets_dir / 'icon.svg', 'w') as f:
        f.write(icon_svg)
    
    print("✅ Assets created")

def convert_icons():
    """Convert SVG icon to platform-specific formats."""
    print("🔄 Converting icons...")
    
    try:
        # Try to use imageio or PIL to convert
        from PIL import Image
        import cairosvg
        
        svg_path = Path('assets/icon.svg')
        
        # Convert to PNG
        png_data = cairosvg.svg2png(url=str(svg_path), output_width=256, output_height=256)
        with open('assets/icon.png', 'wb') as f:
            f.write(png_data)
        
        # Convert PNG to ICO for Windows
        img = Image.open('assets/icon.png')
        img.save('assets/icon.ico', format='ICO', sizes=[(256, 256)])
        
        print("✅ Icons converted")
        
    except ImportError:
        print("⚠️ Icon conversion skipped (missing cairosvg/PIL)")
        # Create dummy files
        for ext in ['png', 'ico', 'icns']:
            Path(f'assets/icon.{ext}').touch()

def build_executable(python_exe):
    """Build the executable using PyInstaller with specified Python."""
    print("🏗️ Building executable...")
    
    platform_info = get_platform_info()
    
    # PyInstaller command using the correct Python
    cmd = [
        python_exe, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', platform_info['exe_name'].replace('.exe', ''),
        '--icon', platform_info['icon'],
        '--add-data', 'theme_manager.py:.',
        '--hidden-import', 'PyQt6',
        '--hidden-import', 'PIL',
        '--hidden-import', 'qdarktheme', 
        '--hidden-import', 'qt_material',
        '--exclude-module', 'tkinter',
        '--exclude-module', 'matplotlib',
        'shrink.py'
    ]
    
    try:
        subprocess.run(cmd, check=True, timeout=600)  # 10 minute timeout
        print("✅ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Build timed out (took longer than 10 minutes)")
        return False

def create_installer():
    """Create platform-specific installer."""
    print("📦 Creating installer...")
    
    platform_info = get_platform_info()
    system = platform_info['name']
    
    try:
        if system == 'windows':
            create_windows_installer()
        elif system == 'macos':
            create_macos_installer() 
        else:
            create_linux_installer()
        
        print("✅ Installer created")
        return True
        
    except Exception as e:
        print(f"❌ Installer creation failed: {e}")
        return False

def create_windows_installer():
    """Create Windows NSIS installer."""
    nsis_script = '''
!include "MUI2.nsh"

Name "Image Shrinker"
OutFile "ImageShrinker_Setup.exe"
InstallDir $PROGRAMFILES\\ImageShrinker
RequestExecutionLevel admin

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File "dist\\ImageShrinker_windows.exe"
    CreateShortcut "$DESKTOP\\Image Shrinker.lnk" "$INSTDIR\\ImageShrinker_windows.exe"
    CreateShortcut "$SMPROGRAMS\\Image Shrinker.lnk" "$INSTDIR\\ImageShrinker_windows.exe"
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\ImageShrinker_windows.exe"
    Delete "$INSTDIR\\Uninstall.exe"
    Delete "$DESKTOP\\Image Shrinker.lnk"
    Delete "$SMPROGRAMS\\Image Shrinker.lnk"
    RMDir "$INSTDIR"
SectionEnd
'''
    
    with open('setup_windows.nsi', 'w') as f:
        f.write(nsis_script)
    
    # Try to compile with NSIS
    try:
        subprocess.run(['makensis', 'setup_windows.nsi'], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ NSIS not found, creating ZIP instead")
        create_zip_package()

def create_macos_installer():
    """Create macOS app bundle and DMG."""
    # Create app bundle structure
    app_dir = Path('dist/ImageShrinker.app')
    contents_dir = app_dir / 'Contents'
    macos_dir = contents_dir / 'MacOS'
    resources_dir = contents_dir / 'Resources'
    
    for dir_path in [macos_dir, resources_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Copy executable
    shutil.copy('dist/ImageShrinker_macos', macos_dir / 'ImageShrinker')
    
    # Create Info.plist
    info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>ImageShrinker</string>
    <key>CFBundleIdentifier</key>
    <string>com.imagetools.shrinker</string>
    <key>CFBundleName</key>
    <string>Image Shrinker</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
</dict>
</plist>'''
    
    with open(contents_dir / 'Info.plist', 'w') as f:
        f.write(info_plist)

def create_linux_installer():
    """Create Linux AppImage or DEB package."""
    # Create simple tar.gz package
    create_tar_package()

def create_zip_package():
    """Create ZIP package for distribution."""
    platform_info = get_platform_info()
    shutil.make_archive(f'ImageShrinker_{platform_info["name"]}', 'zip', 'dist')

def create_tar_package():
    """Create TAR.GZ package for Linux."""
    platform_info = get_platform_info() 
    shutil.make_archive(f'ImageShrinker_{platform_info["name"]}', 'gztar', 'dist')

def cleanup():
    """Clean up build artifacts."""
    print("🧹 Cleaning up...")
    
    cleanup_dirs = ['build', '__pycache__', '*.spec']
    for pattern in cleanup_dirs:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

def main():
    """Main build process with smart Python detection."""
    print("🚀 Cross-Platform Image Shrinker Build")
    print("=" * 50)
    
    # Find working Python first
    python_exe = find_working_python()
    if not python_exe:
        return 1
    
    platform_info = get_platform_info()
    print(f"🖥️ Building for: {platform_info['name']}")
    print(f"🐍 Using Python: {python_exe}")
    
    steps = [
        ("Installing dependencies", lambda: install_dependencies(python_exe)),
        ("Creating assets", create_assets),
        ("Converting icons", convert_icons),
        ("Building executable", lambda: build_executable(python_exe)),
        ("Creating installer", create_installer),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"❌ {step_name} failed!")
            return 1
    
    print("\n✅ Build completed successfully!")
    print(f"📁 Output: dist/{platform_info['exe_name']}")
    
    # Optional cleanup
    try:
        cleanup_choice = input("\n🧹 Clean up build files? (y/N): ")
        if cleanup_choice.lower() == 'y':
            cleanup()
    except KeyboardInterrupt:
        print("\n👋 Build completed!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
