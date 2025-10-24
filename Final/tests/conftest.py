#!/usr/bin/env python3
"""
Pytest configuration and fixtures for test suite
"""
import sys
from unittest.mock import Mock, MagicMock

# Mock PyQt6 modules before any imports
mock_pyqt6_modules = {
    'PyQt6': MagicMock(),
    'PyQt6.QtWidgets': MagicMock(),
    'PyQt6.QtCore': MagicMock(),
    'PyQt6.QtGui': MagicMock(),
    'PyQt5': MagicMock(),
    'PyQt5.QtWidgets': MagicMock(),
    'PyQt5.QtCore': MagicMock(),
    'PyQt5.QtGui': MagicMock(),
    'qdarktheme': MagicMock(),
    'qt_material': MagicMock(),
}

# Install mocks in sys.modules
for module_name, mock_module in mock_pyqt6_modules.items():
    sys.modules[module_name] = mock_module
