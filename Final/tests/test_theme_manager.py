#!/usr/bin/env python3
"""
Unit tests for ThemeManager class
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from theme_manager import ThemeManager, THEMES_AVAILABLE


class TestThemeManager:
    """Test cases for ThemeManager functionality."""

    @pytest.fixture
    def mock_app(self):
        """Create a mock QApplication."""
        app = Mock()
        app.setStyle = Mock()
        app.setStyleSheet = Mock()
        return app

    @pytest.fixture
    def theme_manager(self, mock_app):
        """Create a ThemeManager instance with mock app."""
        return ThemeManager(mock_app)

    def test_initialization(self, theme_manager, mock_app):
        """Test ThemeManager initialization."""
        assert theme_manager.app == mock_app
        assert theme_manager.current_theme == 'system'
        assert isinstance(theme_manager.theme_callbacks, list)

    def test_get_available_themes(self, theme_manager):
        """Test getting available themes."""
        themes = theme_manager.get_available_themes()

        assert 'builtin' in themes
        assert 'custom' in themes
        assert 'enhanced_dark' in themes['custom']
        assert 'enhanced_light' in themes['custom']
        assert 'professional' in themes['custom']
        assert 'creative' in themes['custom']

    def test_builtin_themes_defined(self, theme_manager):
        """Test that builtin themes are properly defined."""
        assert 'light' in theme_manager.BUILTIN_THEMES
        assert 'dark' in theme_manager.BUILTIN_THEMES
        assert 'fusion_light' in theme_manager.BUILTIN_THEMES
        assert 'fusion_dark' in theme_manager.BUILTIN_THEMES

    def test_apply_builtin_light_theme(self, theme_manager, mock_app):
        """Test applying builtin light theme."""
        result = theme_manager.apply_theme('light', 'builtin')
        assert result is True
        assert theme_manager.current_theme == 'builtin_light'
        mock_app.setStyle.assert_called_once()
        mock_app.setStyleSheet.assert_called_once()

    def test_apply_builtin_dark_theme(self, theme_manager, mock_app):
        """Test applying builtin dark theme."""
        result = theme_manager.apply_theme('dark', 'builtin')
        assert result is True
        assert theme_manager.current_theme == 'builtin_dark'
        mock_app.setStyle.assert_called_once_with('fusion')
        mock_app.setStyleSheet.assert_called_once()

    def test_apply_custom_enhanced_dark_theme(self, theme_manager, mock_app):
        """Test applying custom enhanced dark theme."""
        result = theme_manager.apply_theme('enhanced_dark', 'custom')
        assert result is True
        assert theme_manager.current_theme == 'custom_enhanced_dark'
        mock_app.setStyle.assert_called_once_with('fusion')
        mock_app.setStyleSheet.assert_called_once()

    def test_apply_custom_enhanced_light_theme(self, theme_manager, mock_app):
        """Test applying custom enhanced light theme."""
        result = theme_manager.apply_theme('enhanced_light', 'custom')
        assert result is True
        assert theme_manager.current_theme == 'custom_enhanced_light'

    def test_apply_custom_professional_theme(self, theme_manager, mock_app):
        """Test applying custom professional theme."""
        result = theme_manager.apply_theme('professional', 'custom')
        assert result is True
        assert theme_manager.current_theme == 'custom_professional'

    def test_apply_custom_creative_theme(self, theme_manager, mock_app):
        """Test applying custom creative theme."""
        result = theme_manager.apply_theme('creative', 'custom')
        assert result is True
        assert theme_manager.current_theme == 'custom_creative'

    def test_apply_invalid_theme(self, theme_manager):
        """Test applying invalid theme returns False."""
        result = theme_manager.apply_theme('nonexistent', 'custom')
        assert result is False

    def test_get_fusion_dark_stylesheet(self, theme_manager):
        """Test getting fusion dark stylesheet."""
        stylesheet = theme_manager._get_fusion_dark_stylesheet()
        assert isinstance(stylesheet, str)
        assert 'QWidget' in stylesheet
        assert 'background-color' in stylesheet

    def test_get_enhanced_dark_stylesheet(self, theme_manager):
        """Test getting enhanced dark stylesheet."""
        stylesheet = theme_manager._get_enhanced_dark_stylesheet()
        assert isinstance(stylesheet, str)
        assert 'background-color: #1e1e1e' in stylesheet
        assert 'QPushButton' in stylesheet
        assert 'QProgressBar' in stylesheet

    def test_get_enhanced_light_stylesheet(self, theme_manager):
        """Test getting enhanced light stylesheet."""
        stylesheet = theme_manager._get_enhanced_light_stylesheet()
        assert isinstance(stylesheet, str)
        assert 'background-color: #ffffff' in stylesheet
        assert 'QPushButton' in stylesheet

    def test_get_professional_stylesheet(self, theme_manager):
        """Test getting professional stylesheet."""
        stylesheet = theme_manager._get_professional_stylesheet()
        assert isinstance(stylesheet, str)
        assert 'background-color: #1a202c' in stylesheet

    def test_get_creative_stylesheet(self, theme_manager):
        """Test getting creative stylesheet."""
        stylesheet = theme_manager._get_creative_stylesheet()
        assert isinstance(stylesheet, str)
        assert 'background-color: #1a1a2e' in stylesheet
        assert '#667eea' in stylesheet  # Purple accent color

    def test_register_theme_callback(self, theme_manager):
        """Test registering theme change callbacks."""
        callback = Mock()
        theme_manager.register_theme_callback(callback)
        assert callback in theme_manager.theme_callbacks

    def test_notify_theme_change(self, theme_manager):
        """Test notifying callbacks of theme changes."""
        callback1 = Mock()
        callback2 = Mock()
        theme_manager.register_theme_callback(callback1)
        theme_manager.register_theme_callback(callback2)

        theme_manager._notify_theme_change()

        callback1.assert_called_once_with('system')
        callback2.assert_called_once_with('system')

    def test_notify_theme_change_with_exception(self, theme_manager):
        """Test theme change notification handles callback exceptions."""
        def failing_callback(theme):
            raise Exception("Test exception")

        callback_ok = Mock()
        theme_manager.register_theme_callback(failing_callback)
        theme_manager.register_theme_callback(callback_ok)

        # Should not raise exception
        theme_manager._notify_theme_change()
        callback_ok.assert_called_once()

    def test_themes_available_structure(self):
        """Test THEMES_AVAILABLE dictionary structure."""
        assert isinstance(THEMES_AVAILABLE, dict)
        assert 'qdarktheme' in THEMES_AVAILABLE
        assert 'qt_material' in THEMES_AVAILABLE
        assert 'custom' in THEMES_AVAILABLE
        assert THEMES_AVAILABLE['custom'] is True

    @patch('theme_manager.THEMES_AVAILABLE', {'qdarktheme': True, 'qt_material': False, 'custom': True})
    def test_get_available_themes_with_qdarktheme(self, theme_manager):
        """Test getting themes when qdarktheme is available."""
        themes = theme_manager.get_available_themes()
        assert 'qdarktheme' in themes

    @patch('theme_manager.THEMES_AVAILABLE', {'qdarktheme': False, 'qt_material': True, 'custom': True})
    def test_get_available_themes_with_qt_material(self, theme_manager):
        """Test getting themes when qt-material is available."""
        themes = theme_manager.get_available_themes()
        assert 'qt_material' in themes

    def test_stylesheets_have_required_widgets(self, theme_manager):
        """Test that all stylesheets define styles for common widgets."""
        stylesheets = [
            theme_manager._get_enhanced_dark_stylesheet(),
            theme_manager._get_enhanced_light_stylesheet(),
            theme_manager._get_professional_stylesheet(),
            theme_manager._get_creative_stylesheet(),
        ]

        for stylesheet in stylesheets:
            assert 'QPushButton' in stylesheet
            assert 'QGroupBox' in stylesheet
            assert 'background' in stylesheet.lower()

    def test_install_missing_themes(self, theme_manager):
        """Test install_missing_themes method."""
        with patch('subprocess.check_call') as mock_check_call:
            mock_check_call.return_value = None
            results = theme_manager.install_missing_themes()
            assert isinstance(results, dict)
