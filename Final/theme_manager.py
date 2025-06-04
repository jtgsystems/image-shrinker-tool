#!/usr/bin/env python3
"""
Enhanced Image Shrinker - Theme System Integration
=================================================
Integrates best PyQt6 styling libraries and custom themes
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Theme library availability flags
THEMES_AVAILABLE = {
    'qdarktheme': False,
    'qt_material': False,
    'custom': True
}

# Try to import theme libraries
try:
    import qdarktheme
    THEMES_AVAILABLE['qdarktheme'] = True
except ImportError:
    pass

try:
    from qt_material import apply_stylesheet, list_themes
    THEMES_AVAILABLE['qt_material'] = True
except ImportError:
    pass

class ThemeManager:
    """Manages application themes and styling."""
    
    BUILTIN_THEMES = {
        'light': 'System Light',
        'dark': 'System Dark', 
        'fusion_light': 'Fusion Light',
        'fusion_dark': 'Fusion Dark'
    }
    
    QDARKTHEME_THEMES = ['dark', 'light', 'auto'] if THEMES_AVAILABLE['qdarktheme'] else []
    
    QT_MATERIAL_THEMES = [
        'dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml',
        'dark_pink.xml', 'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml',
        'dark_yellow.xml', 'light_amber.xml', 'light_blue.xml', 'light_cyan.xml',
        'light_lightgreen.xml', 'light_pink.xml', 'light_purple.xml', 'light_red.xml',
        'light_teal.xml', 'light_yellow.xml'
    ] if THEMES_AVAILABLE['qt_material'] else []
    
    def __init__(self, app):
        self.app = app
        self.current_theme = 'system'
        self.theme_callbacks = []
    
    def get_available_themes(self) -> Dict[str, list]:
        """Get all available themes organized by library."""
        themes = {
            'builtin': list(self.BUILTIN_THEMES.keys()),
            'custom': ['enhanced_dark', 'enhanced_light', 'professional', 'creative']
        }
        
        if THEMES_AVAILABLE['qdarktheme']:
            themes['qdarktheme'] = self.QDARKTHEME_THEMES
        
        if THEMES_AVAILABLE['qt_material']:
            themes['qt_material'] = self.QT_MATERIAL_THEMES
        
        return themes
    
    def apply_theme(self, theme_name: str, theme_type: str = 'auto') -> bool:
        """Apply specified theme to application."""
        try:
            if theme_type == 'qdarktheme' and THEMES_AVAILABLE['qdarktheme']:
                return self._apply_qdarktheme(theme_name)
            
            elif theme_type == 'qt_material' and THEMES_AVAILABLE['qt_material']:
                return self._apply_qt_material(theme_name)
            
            elif theme_type == 'custom':
                return self._apply_custom_theme(theme_name)
            
            elif theme_type == 'builtin':
                return self._apply_builtin_theme(theme_name)
            
            else:
                # Auto-detect theme type
                if theme_name in self.QDARKTHEME_THEMES and THEMES_AVAILABLE['qdarktheme']:
                    return self._apply_qdarktheme(theme_name)
                elif theme_name in self.QT_MATERIAL_THEMES and THEMES_AVAILABLE['qt_material']:
                    return self._apply_qt_material(theme_name)
                elif theme_name in self.BUILTIN_THEMES:
                    return self._apply_builtin_theme(theme_name)
                else:
                    return self._apply_custom_theme(theme_name)
        
        except Exception as e:
            print(f"❌ Theme application failed: {e}")
            return False
    
    def _apply_qdarktheme(self, theme_name: str) -> bool:
        """Apply PyQtDarkTheme styling."""
        try:
            qdarktheme.setup_theme(
                theme=theme_name,
                corner_shape="rounded",
                custom_colors={
                    "primary": "#1976d2",
                    "primary:hover": "#1565c0",
                    "primary:pressed": "#0d47a1"
                }
            )
            self.current_theme = f"qdarktheme_{theme_name}"
            return True
        except Exception as e:
            print(f"❌ QDarkTheme error: {e}")
            return False
    
    def _apply_qt_material(self, theme_name: str) -> bool:
        """Apply Qt-Material styling."""
        try:
            apply_stylesheet(self.app, theme=theme_name)
            self.current_theme = f"qt_material_{theme_name}"
            return True
        except Exception as e:
            print(f"❌ Qt-Material error: {e}")
            return False
    
    def _apply_builtin_theme(self, theme_name: str) -> bool:
        """Apply built-in Qt themes."""
        try:
            if theme_name == 'light':
                self.app.setStyle('windowsvista')
                self.app.setStyleSheet("")
            elif theme_name == 'dark':
                self.app.setStyle('fusion')
                self.app.setStyleSheet(self._get_fusion_dark_stylesheet())
            elif theme_name == 'fusion_light':
                self.app.setStyle('fusion')
                self.app.setStyleSheet("")
            elif theme_name == 'fusion_dark':
                self.app.setStyle('fusion')
                self.app.setStyleSheet(self._get_fusion_dark_stylesheet())
            
            self.current_theme = f"builtin_{theme_name}"
            return True
        except Exception as e:
            print(f"❌ Built-in theme error: {e}")
            return False
    
    def _apply_custom_theme(self, theme_name: str) -> bool:
        """Apply custom theme stylesheets."""
        try:
            if theme_name == 'enhanced_dark':
                stylesheet = self._get_enhanced_dark_stylesheet()
            elif theme_name == 'enhanced_light':
                stylesheet = self._get_enhanced_light_stylesheet()
            elif theme_name == 'professional':
                stylesheet = self._get_professional_stylesheet()
            elif theme_name == 'creative':
                stylesheet = self._get_creative_stylesheet()
            else:
                return False
            
            self.app.setStyle('fusion')
            self.app.setStyleSheet(stylesheet)
            self.current_theme = f"custom_{theme_name}"
            return True
        except Exception as e:
            print(f"❌ Custom theme error: {e}")
            return False
    
    def _get_fusion_dark_stylesheet(self) -> str:
        """Get Fusion dark theme stylesheet."""
        return """
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
            selection-background-color: #3daee9;
            selection-color: #ffffff;
        }
        
        QMainWindow {
            background-color: #2b2b2b;
        }
        
        QPushButton {
            background-color: #404040;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 8px 16px;
            min-width: 80px;
        }
        
        QPushButton:hover {
            background-color: #4a4a4a;
            border-color: #6a6a6a;
        }
        
        QPushButton:pressed {
            background-color: #353535;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #555555;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        """
    
    def _get_enhanced_dark_stylesheet(self) -> str:
        """Enhanced dark theme with modern styling."""
        return """
        * {
            background-color: #1e1e1e;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
        }
        
        QMainWindow {
            background-color: #1e1e1e;
            border: none;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #404040, stop:1 #2a2a2a);
            border: 1px solid #555555;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 14px;
            min-width: 100px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4a4a4a, stop:1 #3a3a3a);
            border-color: #0078d4;
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2a2a2a, stop:1 #404040);
        }
        
        QGroupBox {
            font-weight: 600;
            font-size: 13px;
            border: 2px solid #404040;
            border-radius: 8px;
            margin: 15px 0px 10px 0px;
            padding-top: 15px;
            background-color: #252525;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 15px;
            padding: 0 8px 0 8px;
            color: #ffffff;
            background-color: transparent;
        }
        
        QLabel {
            background-color: transparent;
            color: #ffffff;
            font-size: 13px;
        }
        
        QProgressBar {
            border: 1px solid #555555;
            border-radius: 4px;
            text-align: center;
            background-color: #2a2a2a;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0078d4, stop:1 #106ebe);
            border-radius: 3px;
        }
        
        QSlider::groove:horizontal {
            height: 6px;
            background: #2a2a2a;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            background: #0078d4;
            border: 1px solid #555555;
            width: 16px;
            height: 16px;
            border-radius: 8px;
            margin: -5px 0;
        }
        
        QSlider::handle:horizontal:hover {
            background: #106ebe;
        }
        
        QCheckBox {
            spacing: 8px;
            font-size: 13px;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 2px solid #555555;
            border-radius: 3px;
            background-color: #2a2a2a;
        }
        
        QCheckBox::indicator:checked {
            background-color: #0078d4;
            border-color: #0078d4;
        }
        
        QSpinBox {
            background-color: #2a2a2a;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 5px;
            font-size: 13px;
        }
        
        QSpinBox:focus {
            border-color: #0078d4;
        }
        """
    
    def _get_enhanced_light_stylesheet(self) -> str:
        """Enhanced light theme with clean styling."""
        return """
        * {
            background-color: #ffffff;
            color: #2d3748;
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
        }
        
        QMainWindow {
            background-color: #f7fafc;
            border: none;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f1f5f9);
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 14px;
            min-width: 100px;
            color: #2d3748;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f8fafc, stop:1 #e2e8f0);
            border-color: #3182ce;
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #e2e8f0, stop:1 #cbd5e0);
        }
        
        QGroupBox {
            font-weight: 600;
            font-size: 13px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            margin: 15px 0px 10px 0px;
            padding-top: 15px;
            background-color: #ffffff;
            color: #2d3748;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 15px;
            padding: 0 8px 0 8px;
            color: #2d3748;
            background-color: transparent;
        }
        
        QProgressBar {
            border: 1px solid #cbd5e0;
            border-radius: 4px;
            text-align: center;
            background-color: #f1f5f9;
            color: #2d3748;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3182ce, stop:1 #2c5aa0);
            border-radius: 3px;
        }
        """
    
    def _get_professional_stylesheet(self) -> str:
        """Professional blue-accented theme."""
        return """
        * {
            background-color: #1a202c;
            color: #e2e8f0;
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4a5568, stop:1 #2d3748);
            border: 1px solid #718096;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 500;
            color: #ffffff;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #4299e1, stop:1 #3182ce);
            border-color: #63b3ed;
        }
        
        QGroupBox {
            font-weight: 600;
            border: 2px solid #4a5568;
            border-radius: 8px;
            margin: 15px 0px 10px 0px;
            padding-top: 15px;
            background-color: #2d3748;
        }
        """
    
    def _get_creative_stylesheet(self) -> str:
        """Creative purple-accented theme."""
        return """
        * {
            background-color: #1a1a2e;
            color: #eee;
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            color: #ffffff;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #764ba2, stop:1 #667eea);
        }
        
        QGroupBox {
            font-weight: 600;
            border: 2px solid #667eea;
            border-radius: 12px;
            margin: 15px 0px 10px 0px;
            padding-top: 15px;
            background-color: #16213e;
        }
        """
    
    def install_missing_themes(self) -> Dict[str, bool]:
        """Install missing theme libraries."""
        results = {}
        
        if not THEMES_AVAILABLE['qdarktheme']:
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyqtdarktheme"])
                results['qdarktheme'] = True
            except:
                results['qdarktheme'] = False
        
        if not THEMES_AVAILABLE['qt_material']:
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", "qt-material"])
                results['qt_material'] = True
            except:
                results['qt_material'] = False
        
        return results
    
    def register_theme_callback(self, callback):
        """Register callback for theme changes."""
        self.theme_callbacks.append(callback)
    
    def _notify_theme_change(self):
        """Notify all callbacks of theme change."""
        for callback in self.theme_callbacks:
            try:
                callback(self.current_theme)
            except Exception as e:
                print(f"❌ Theme callback error: {e}")

def get_theme_installation_script() -> str:
    """Generate installation script for theme libraries."""
    return """
@echo off
echo 🎨 Installing PyQt6 Theme Libraries
echo ==================================

echo Installing PyQtDarkTheme...
pip install pyqtdarktheme

echo Installing Qt-Material...
pip install qt-material

echo Installing additional styling tools...
pip install darkdetect

echo ✅ Theme installation complete!
echo.
echo Available themes:
echo - PyQtDarkTheme: Modern flat dark/light themes
echo - Qt-Material: Material Design inspired themes
echo - Custom: Enhanced built-in themes
echo.
pause
"""

if __name__ == "__main__":
    # Test theme availability
    print("🎨 Theme Library Status:")
    for lib, available in THEMES_AVAILABLE.items():
        status = "✅ Available" if available else "❌ Missing"
        print(f"  {lib}: {status}")
