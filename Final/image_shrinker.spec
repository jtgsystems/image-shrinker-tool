# PyInstaller spec file for cross-platform Image Shrinker build
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Determine the platform
if sys.platform.startswith('win'):
    platform_name = 'windows'
    icon_file = 'assets/icon.ico'
    exe_extension = '.exe'
elif sys.platform.startswith('darwin'):
    platform_name = 'macos'
    icon_file = 'assets/icon.icns'
    exe_extension = ''
else:
    platform_name = 'linux'
    icon_file = 'assets/icon.png'
    exe_extension = ''

block_cipher = None

# Data files to include
datas = [
    ('theme_manager.py', '.'),
    ('assets/', 'assets/'),
]

# Hidden imports for PyQt6 and theme libraries
hiddenimports = [
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PIL',
    'PIL.Image',
    'PIL.ImageEnhance',
    'pillow_heif',
    'qdarktheme',
    'qt_material',
    'concurrent.futures',
    'pathlib',
    'logging',
]

# Binaries to exclude (reduce size)
excludes = [
    'tkinter',
    'matplotlib',
    'numpy',
    'scipy',
    'pandas',
    'IPython',
    'jupyter',
    'notebook',
    'sphinx',
    'pytest',
]

a = Analysis(
    ['shrink.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=f'ImageShrinker_{platform_name}{exe_extension}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

# macOS app bundle
if sys.platform.startswith('darwin'):
    app = BUNDLE(
        exe,
        name='ImageShrinker.app',
        icon=icon_file,
        bundle_identifier='com.imagetools.shrinker',
        version='2.0.0',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSAppleScriptEnabled': False,
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeName': 'Image',
                    'CFBundleTypeIconFile': 'icon.icns',
                    'LSItemContentTypes': ['public.image'],
                    'LSHandlerRank': 'Alternate'
                }
            ]
        },
    )
