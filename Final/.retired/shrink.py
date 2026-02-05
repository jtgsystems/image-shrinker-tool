"""
Image processing utility with a PyQt6 GUI for resizing, converting, and optimizing images.
Enhanced with modern themes and styling support.
"""
import sys
from pathlib import Path
from typing import Union, List, Tuple, Sequence, Optional, Dict, Any 

# Theme management import
try:
    from theme_manager import ThemeManager, THEMES_AVAILABLE
    THEME_SUPPORT = True
except ImportError:
    THEME_SUPPORT = False 

# Try PyQt6 first, fall back to PyQt5
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QFileDialog, QProgressBar, QCheckBox,
        QSlider, QSpinBox, QGroupBox, QFormLayout, QComboBox, QStackedWidget,
        QLineEdit
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData
    from PyQt6.QtGui import QDropEvent, QDragEnterEvent, QMouseEvent, QDragLeaveEvent
    PYQT_VERSION = 6
except ImportError:
    try:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QPushButton, QLabel, QFileDialog, QProgressBar, QCheckBox,
            QSlider, QSpinBox, QGroupBox, QFormLayout, QComboBox, QStackedWidget,
            QLineEdit
        )
        from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMimeData
        from PyQt5.QtGui import QDropEvent, QDragEnterEvent, QMouseEvent, QDragLeaveEvent
        PYQT_VERSION = 5
    except ImportError:
        print("❌ Neither PyQt6 nor PyQt5 found.")
        print("🔧 Please run 'fix_environment.bat' to install dependencies.")
        print("Or manually install: pip install PyQt6 Pillow pillow-heif")
        input("Press Enter to exit...")
        sys.exit(1)
from PIL import Image, ImageEnhance
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

# Setup logging
logging.basicConfig(
    filename='image_processor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class ImageProcessor:
    """Handles image processing operations like resizing, conversion, and optimization."""
    extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

    @staticmethod
    def convert_to_rgb(image: Image.Image) -> Image.Image:
        """Converts an image to RGB format, handling transparency."""
        # Accessing image.info can be tricky for type checkers.
        # We'll assume it's a dict-like structure if it exists and has 'transparency'.
        has_transparency_in_info = False
        if hasattr(image, 'info') and isinstance(image.info, dict):
            has_transparency_in_info = 'transparency' in image.info

        if (image.mode in ('RGBA', 'LA') or
                (image.mode == 'P' and has_transparency_in_info)):
            bg = Image.new("RGB", image.size, (255, 255, 255))
            try:
                alpha = image.convert('RGBA').split()[-1]
                bg.paste(image, mask=alpha)
            except IndexError: 
                bg.paste(image)
            return bg
        return image.convert('RGB')

    @staticmethod
    def optimize_image(
        filepath: Union[Path, str],
        output_dir: Union[Path, str],
        resize_method: str,
        resize_value: Optional[Union[int, Tuple[int, int]]],
        quality: int,
        to_jpg: bool,
        to_webp: bool,
        preserve_exif: bool,
        allow_enlarge: bool,
        preserve_transparency: bool,
        grayscale: bool,
        sharpen: bool,
        rename_prefix: str
    ) -> bool:
        """
        Optimizes a single image based on the provided parameters.
        """
        try:
            filepath = Path(filepath)
            with Image.open(filepath) as img:
                original_width, original_height = img.size
                
                # Handle img.info carefully for EXIF data
                exif_data: Optional[bytes] = None
                if preserve_exif and hasattr(img, 'info') and isinstance(img.info, dict):
                    raw_exif = img.info.get('exif')
                    if isinstance(raw_exif, bytes):
                        exif_data = raw_exif

                new_width, new_height = original_width, original_height
                if resize_method == "percentage" and isinstance(resize_value, int):
                    new_width = int(original_width * resize_value / 100)
                    new_height = int(original_height * resize_value / 100)
                elif resize_method == "fixed_size" and isinstance(resize_value, tuple):
                    new_width, new_height = resize_value
                elif resize_method == "max_width" and isinstance(resize_value, int):
                    max_width_val = resize_value
                    if original_width > max_width_val:
                        scale = max_width_val / original_width
                        new_width = max_width_val
                        new_height = int(original_height * scale)

                if (not allow_enlarge and
                        (new_width > original_width or new_height > original_height)):
                    new_width, new_height = original_width, original_height

                if (new_width, new_height) != (original_width, original_height):
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                if grayscale:
                    img = img.convert('L').convert('RGB')
                if sharpen:
                    img = ImageEnhance.Sharpness(img).enhance(2.0)

                if preserve_transparency and to_webp and img.mode in ('RGBA', 'LA'):
                    webp_img = img
                else:
                    webp_img = ImageProcessor.convert_to_rgb(img)

                jpg_img = ImageProcessor.convert_to_rgb(img)

                base_name = f"{rename_prefix}_{filepath.stem}" if rename_prefix else filepath.stem

                output_dir_path = Path(output_dir)
                if to_jpg:
                    jpg_path = output_dir_path / 'jpg' / f"{base_name}.jpg"
                    jpg_path.parent.mkdir(parents=True, exist_ok=True)
                    save_kwargs: Dict[str, Any] = {
                        'quality': quality,
                        'optimize': True,
                        'progressive': True
                    }
                    if exif_data: # exif_data is already Optional[bytes]
                        save_kwargs['exif'] = exif_data
                    jpg_img.save(jpg_path, 'JPEG', **save_kwargs)

                if to_webp:
                    webp_path = output_dir_path / 'webp' / f"{base_name}.webp"
                    webp_path.parent.mkdir(parents=True, exist_ok=True)
                    webp_img.save(webp_path, 'WEBP', quality=quality, method=6)

                logging.info(f"Processed and saved: {filepath}")
                return True
        except Exception as e:
            logging.error(f"Error processing {filepath}: {str(e)}")
            return False

    @staticmethod
    def get_all_image_files(paths: Sequence[Union[str, Path]]) -> List[Path]:
        """Recursively finds all image files in the given list of paths (files or directories)."""
        image_files: List[Path] = []
        for item_path_str_or_path in paths:
            item_path = Path(item_path_str_or_path)
            if item_path.is_file() and item_path.suffix.lower() in ImageProcessor.extensions:
                image_files.append(item_path)
            elif item_path.is_dir():
                for ext in ImageProcessor.extensions:
                    image_files.extend(item_path.rglob(f'*{ext}'))
        return image_files


class ProcessingThread(QThread):
    """Thread for processing images in the background to keep the GUI responsive."""
    progress_update = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(
        self,
        image_files: List[Path],
        output_dir: Path,
        resize_method: str,
        resize_value: Optional[Union[int, Tuple[int, int]]],
        quality: int,
        to_jpg: bool,
        to_webp: bool,
        preserve_exif: bool,
        allow_enlarge: bool,
        preserve_transparency: bool,
        grayscale: bool,
        sharpen: bool,
        rename_prefix: str
    ):
        super().__init__()
        self.image_files = image_files
        self.output_dir = output_dir
        self.resize_method = resize_method
        self.resize_value = resize_value
        self.quality = quality
        self.to_jpg = to_jpg
        self.to_webp = to_webp
        self.preserve_exif = preserve_exif
        self.allow_enlarge = allow_enlarge
        self.preserve_transparency = preserve_transparency
        self.grayscale = grayscale
        self.sharpen = sharpen
        self.rename_prefix = rename_prefix

    def run(self):
        """Executes the image processing tasks."""
        total_files = len(self.image_files)
        processed_count = 0

        with ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(
                    ImageProcessor.optimize_image,
                    file,
                    self.output_dir,
                    self.resize_method,
                    self.resize_value,
                    self.quality,
                    self.to_jpg,
                    self.to_webp,
                    self.preserve_exif,
                    self.allow_enlarge,
                    self.preserve_transparency,
                    self.grayscale,
                    self.sharpen,
                    self.rename_prefix
                )
                for file in self.image_files
            ]
            for future in as_completed(futures):
                try:
                    if future.result():
                        processed_count += 1
                except Exception as e:
                    logging.error(f"A processing task failed: {e}")
                self.progress_update.emit(processed_count, total_files)

        self.finished.emit()


class ImageProcessorGUI(QMainWindow):
    """Main GUI window for the Image Processor application."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Image Processor")
        self.setGeometry(100, 100, 900, 700)
        self.selected_paths: List[str] = []
        self.output_dir = Path.cwd() / "Processed_Images"
        self.processing_thread: Optional[ProcessingThread] = None
        
        # Initialize theme manager if available
        if THEME_SUPPORT:
            self.theme_manager = None  # Will be set after QApplication
        
        self.setup_ui()

    def setup_ui(self):
        """Sets up the user interface elements."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self._setup_drag_drop_area(main_layout)
        self._setup_options_group(main_layout)
        self._setup_conversion_options(main_layout)
        self._setup_additional_options(main_layout)
        self._setup_output_options(main_layout)
        self._setup_controls(main_layout)
        
        # Setup theme menu if available
        if THEME_SUPPORT:
            self._setup_theme_menu()

        self.resize_method_combo.currentIndexChanged.connect(self.resize_stack.setCurrentIndex) # type: ignore
        self.resize_slider.valueChanged.connect(self.resize_spinbox.setValue) # type: ignore
        self.resize_spinbox.valueChanged.connect(self.resize_slider.setValue) # type: ignore

    def _setup_drag_drop_area(self, parent_layout: QVBoxLayout):
        """Sets up the drag and drop area."""
        self.drop_area = QLabel("Drag and drop files or folders here, or click to select")
        self.drop_area.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        self.drop_area.setStyleSheet(
            "border: 2px dashed #aaa; border-radius: 5px; "
            "padding: 20px; background-color: #f0f0f0;"
        )
        self.drop_area.setAcceptDrops(True)
        self.drop_area.mousePressEvent = self._handle_drop_area_click # type: ignore
        parent_layout.addWidget(self.drop_area)

    def _handle_drop_area_click(self, ev: Optional[QMouseEvent]):
        """Handles click on the drop area label to open file dialog."""
        if ev and ev.button() == Qt.MouseButton.LeftButton:
            self.open_file_dialog()

    def _setup_options_group(self, parent_layout: QVBoxLayout):
        """Sets up the main processing options group."""
        options_group = QGroupBox("Processing Options")
        options_layout = QFormLayout()
        options_group.setLayout(options_layout)

        self.resize_method_combo = QComboBox()
        self.resize_method_combo.addItems(["No Resizing", "Percentage", "Fixed Size", "Max Width"]) # type: ignore
        options_layout.addRow("Resize Method:", self.resize_method_combo)

        self.resize_stack = QStackedWidget()
        self._setup_resize_options_stack(self.resize_stack)
        options_layout.addRow(self.resize_stack)

        quality_layout = QHBoxLayout()
        self.quality_slider = QSlider(Qt.Orientation.Horizontal if PYQT_VERSION == 6 else Qt.Horizontal)
        self.quality_slider.setRange(10, 100)
        self.quality_slider.setValue(85)
        self.quality_spinbox = QSpinBox()
        self.quality_spinbox.setRange(10, 100)
        self.quality_spinbox.setValue(85)
        self.quality_spinbox.setSuffix("%")
        self.quality_slider.valueChanged.connect(self.quality_spinbox.setValue) # type: ignore
        self.quality_spinbox.valueChanged.connect(self.quality_slider.setValue) # type: ignore
        quality_layout.addWidget(QLabel("Quality:"))
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_spinbox)
        options_layout.addRow(quality_layout)

        parent_layout.addWidget(options_group)

    def _setup_resize_options_stack(self, stack: QStackedWidget):
        """Populates the QStackedWidget for different resize options."""
        stack.addWidget(QWidget())
        percentage_widget = QWidget()
        percentage_layout = QHBoxLayout(percentage_widget)
        self.resize_slider = QSlider(Qt.Orientation.Horizontal if PYQT_VERSION == 6 else Qt.Horizontal)
        self.resize_slider.setRange(1, 200)
        self.resize_slider.setValue(100)
        self.resize_spinbox = QSpinBox()
        self.resize_spinbox.setRange(1, 200)
        self.resize_spinbox.setValue(100)
        self.resize_spinbox.setSuffix("%")
        percentage_layout.addWidget(self.resize_slider)
        percentage_layout.addWidget(self.resize_spinbox)
        stack.addWidget(percentage_widget)
        fixed_size_widget = QWidget()
        fixed_size_layout = QFormLayout(fixed_size_widget)
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 10000)
        self.width_spinbox.setValue(1920)
        self.width_spinbox.setPrefix("W: ")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 10000)
        self.height_spinbox.setValue(1080)
        self.height_spinbox.setPrefix("H: ")
        fixed_size_layout.addRow(self.width_spinbox, self.height_spinbox)
        stack.addWidget(fixed_size_widget)
        max_width_widget = QWidget()
        max_width_layout = QHBoxLayout(max_width_widget)
        self.max_width_spinbox = QSpinBox()
        self.max_width_spinbox.setRange(1, 10000)
        self.max_width_spinbox.setValue(1920)
        self.max_width_spinbox.setSuffix(" px")
        max_width_layout.addWidget(QLabel("Max Width:"))
        max_width_layout.addWidget(self.max_width_spinbox)
        stack.addWidget(max_width_widget)

    def _setup_conversion_options(self, parent_layout: QVBoxLayout):
        """Sets up conversion format options."""
        conversion_group = QGroupBox("Output Formats")
        conversion_layout = QHBoxLayout(conversion_group)
        self.to_jpg_checkbox = QCheckBox("Convert to JPG")
        self.to_jpg_checkbox.setChecked(True)
        self.to_webp_checkbox = QCheckBox("Convert to WebP")
        self.to_webp_checkbox.setChecked(True)
        conversion_layout.addWidget(self.to_jpg_checkbox)
        conversion_layout.addWidget(self.to_webp_checkbox)
        conversion_layout.addStretch()
        parent_layout.addWidget(conversion_group)

    def _setup_additional_options(self, parent_layout: QVBoxLayout):
        """Sets up additional processing options like EXIF, grayscale, etc."""
        additional_group = QGroupBox("Additional Options")
        additional_layout = QFormLayout(additional_group)
        self.preserve_exif_checkbox = QCheckBox("Preserve EXIF Data")
        self.preserve_exif_checkbox.setChecked(True)
        additional_layout.addRow(self.preserve_exif_checkbox)
        self.allow_enlarge_checkbox = QCheckBox("Allow Enlarging Images")
        self.allow_enlarge_checkbox.setChecked(False)
        additional_layout.addRow(self.allow_enlarge_checkbox)
        self.preserve_transparency_checkbox = QCheckBox("Preserve Transparency (for WebP)")
        self.preserve_transparency_checkbox.setChecked(True)
        additional_layout.addRow(self.preserve_transparency_checkbox)
        self.grayscale_checkbox = QCheckBox("Convert to Grayscale")
        additional_layout.addRow(self.grayscale_checkbox)
        self.sharpen_checkbox = QCheckBox("Apply Sharpening")
        additional_layout.addRow(self.sharpen_checkbox)
        parent_layout.addWidget(additional_group)

    def _setup_output_options(self, parent_layout: QVBoxLayout):
        """Sets up output directory and renaming options."""
        output_group = QGroupBox("Output Settings")
        output_layout = QFormLayout(output_group)
        output_dir_layout = QHBoxLayout()
        self.output_dir_label = QLabel(f"Output: {self.output_dir}")
        self.output_dir_button = QPushButton("Change...")
        self.output_dir_button.clicked.connect(self.select_output_directory) # type: ignore
        output_dir_layout.addWidget(self.output_dir_label)
        output_dir_layout.addWidget(self.output_dir_button)
        output_layout.addRow(output_dir_layout)
        self.rename_prefix_input = QLineEdit()
        self.rename_prefix_input.setPlaceholderText("Optional prefix (e.g., 'processed_')")
        output_layout.addRow("Filename Prefix:", self.rename_prefix_input)
        parent_layout.addWidget(output_group)

    def _setup_controls(self, parent_layout: QVBoxLayout):
        """Sets up the progress bar and start/clear buttons."""
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setValue(0)
        parent_layout.addWidget(self.progress_bar)
        buttons_layout = QHBoxLayout()
        self.select_files_button = QPushButton("Select Files/Folders")
        self.select_files_button.clicked.connect(self.open_file_dialog) # type: ignore
        self.start_button = QPushButton("Start Processing")
        self.start_button.clicked.connect(self.start_processing) # type: ignore
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.clear_button = QPushButton("Clear Selection")
        self.clear_button.clicked.connect(self.clear_selection) # type: ignore
        buttons_layout.addWidget(self.select_files_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.start_button)
        parent_layout.addLayout(buttons_layout)
    
    def _setup_theme_menu(self):
        """Setup theme selection menu if theme support is available."""
        if not THEME_SUPPORT:
            return
        
        # Add theme menu to menu bar
        menu_bar = self.menuBar()
        theme_menu = menu_bar.addMenu("🎨 Theme")
        
        # Built-in themes
        builtin_menu = theme_menu.addMenu("Built-in")
        for theme_name in ['light', 'dark', 'fusion_light', 'fusion_dark']:
            action = builtin_menu.addAction(theme_name.replace('_', ' ').title())
            action.triggered.connect(lambda checked, t=theme_name: self.apply_theme(t, 'builtin'))
        
        # Custom themes
        custom_menu = theme_menu.addMenu("Custom")
        for theme_name in ['enhanced_dark', 'enhanced_light', 'professional', 'creative']:
            action = custom_menu.addAction(theme_name.replace('_', ' ').title())
            action.triggered.connect(lambda checked, t=theme_name: self.apply_theme(t, 'custom'))
        
        # External library themes (if available)
        if THEMES_AVAILABLE.get('qdarktheme', False):
            qdark_menu = theme_menu.addMenu("QDarkTheme")
            for theme_name in ['dark', 'light', 'auto']:
                action = qdark_menu.addAction(theme_name.title())
                action.triggered.connect(lambda checked, t=theme_name: self.apply_theme(t, 'qdarktheme'))
        
        if THEMES_AVAILABLE.get('qt_material', False):
            material_menu = theme_menu.addMenu("Material Design")
            # Add popular material themes
            popular_themes = [
                'dark_teal.xml', 'dark_blue.xml', 'dark_amber.xml',
                'light_blue.xml', 'light_teal.xml', 'light_amber.xml'
            ]
            for theme_name in popular_themes:
                display_name = theme_name.replace('.xml', '').replace('_', ' ').title()
                action = material_menu.addAction(display_name)
                action.triggered.connect(lambda checked, t=theme_name: self.apply_theme(t, 'qt_material'))
        
        # Theme installation option
        theme_menu.addSeparator()
        install_action = theme_menu.addAction("📦 Install More Themes")
        install_action.triggered.connect(self.install_themes)
    
    def apply_theme(self, theme_name: str, theme_type: str):
        """Apply selected theme."""
        if hasattr(self, 'theme_manager') and self.theme_manager:
            success = self.theme_manager.apply_theme(theme_name, theme_type)
            if success:
                self.statusBar().showMessage(f"Applied theme: {theme_name}", 3000)
            else:
                self.statusBar().showMessage(f"Failed to apply theme: {theme_name}", 3000)
    
    def install_themes(self):
        """Install additional theme libraries."""
        if THEME_SUPPORT:
            # Show message about theme installation
            from PyQt6.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self, 'Install Themes',
                'This will install additional theme libraries (PyQtDarkTheme, Qt-Material).\n'
                'Do you want to continue?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    import subprocess
                    subprocess.run(['install_themes.bat'], shell=True)
                    QMessageBox.information(
                        self, 'Installation', 
                        'Theme libraries installation started.\n'
                        'Please restart the application after installation completes.'
                    )
                except Exception as e:
                    QMessageBox.warning(
                        self, 'Error', 
                        f'Failed to start installation: {e}\n'
                        'Please run install_themes.bat manually.'
                    )

    def dragEnterEvent(self, a0: Optional[QDragEnterEvent]):
        """Handles drag enter events."""
        if a0:
            mime_data: Optional[QMimeData] = a0.mimeData()
            if mime_data and mime_data.hasUrls():
                a0.acceptProposedAction()
                self.drop_area.setStyleSheet(
                    "border: 2px dashed #0078d7; border-radius: 5px; "
                    "padding: 20px; background-color: #e0e0ff;"
                )
            else:
                a0.ignore()

    def dragLeaveEvent(self, a0: Optional[QDragLeaveEvent]):
        """Handles drag leave events."""
        self.drop_area.setStyleSheet(
            "border: 2px dashed #aaa; border-radius: 5px; "
            "padding: 20px; background-color: #f0f0f0;"
        )
        if a0:
            a0.accept()

    def dropEvent(self, a0: Optional[QDropEvent]):
        """Handles drop events to add files/folders to the processing list."""
        if not a0:
            return
        
        mime_data: Optional[QMimeData] = a0.mimeData()
        if mime_data and mime_data.hasUrls():
            urls = mime_data.urls()
            if urls:
                for url in urls:
                    path_str = url.toLocalFile()
                    if Path(path_str).exists():
                        if path_str not in self.selected_paths:
                            self.selected_paths.append(path_str)
                self.update_drop_area_text()
                a0.acceptProposedAction()
            else:
                 a0.ignore()
        else:
            a0.ignore()
        
        self.drop_area.setStyleSheet(
            "border: 2px dashed #aaa; border-radius: 5px; "
            "padding: 20px; background-color: #f0f0f0;"
        )

    def open_file_dialog(self):
        """Opens a file dialog to select multiple files and folders."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Image Files",
            "",
            f"Image Files ({' '.join(['*' + ext for ext in ImageProcessor.extensions])});;All Files (*)"
        )
        if files:
            for file_path in files:
                if file_path not in self.selected_paths:
                    self.selected_paths.append(file_path)
        self.update_drop_area_text()

    def update_drop_area_text(self):
        """Updates the text of the drop area based on selected files."""
        if not self.selected_paths:
            self.drop_area.setText("Drag and drop files or folders here, or click to select")
        else:
            count = len(self.selected_paths)
            if count > 3:
                display_paths = "\\n".join([Path(p).name for p in self.selected_paths[:3]])
                self.drop_area.setText(f"Selected {count} items:\\n{display_paths}\\n...and {count-3} more.")
            else:
                display_paths = "\\n".join([Path(p).name for p in self.selected_paths])
                self.drop_area.setText(f"Selected {count} items:\\n{display_paths}")

    def select_output_directory(self):
        """Opens a dialog to select the output directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory", str(self.output_dir))
        if directory:
            self.output_dir = Path(directory)
            self.output_dir_label.setText(f"Output: {self.output_dir}")

    def clear_selection(self):
        """Clears the current selection of files and resets the UI."""
        self.selected_paths = []
        self.update_drop_area_text()
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("0/0 (0%)")
        logging.info("Selection cleared.")

    def start_processing(self):
        """Starts the image processing thread with the current settings."""
        if not self.selected_paths:
            logging.warning("No files selected for processing.")
            self.drop_area.setText("No files selected! Please add files or folders.")
            return

        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                logging.error(f"Could not create output directory {self.output_dir}: {e}")
                return

        image_files: List[Path] = ImageProcessor.get_all_image_files(self.selected_paths)

        if not image_files:
            logging.warning("No valid image files found in the selection.")
            self.drop_area.setText("No processable image files found in selection.")
            return

        total_files = len(image_files)
        self.progress_bar.setMaximum(total_files)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat(f"0/{total_files} (0%)")

        resize_method = self.resize_method_combo.currentText()
        resize_value: Optional[Union[int, Tuple[int, int]]] = None
        if resize_method == "Percentage":
            resize_value = self.resize_spinbox.value()
        elif resize_method == "Fixed Size":
            resize_value = (self.width_spinbox.value(), self.height_spinbox.value())
        elif resize_method == "Max Width":
            resize_value = self.max_width_spinbox.value()

        self._set_ui_enabled(False)

        self.processing_thread = ProcessingThread(
            image_files=image_files,
            output_dir=self.output_dir,
            resize_method=resize_method,
            resize_value=resize_value,
            quality=self.quality_spinbox.value(),
            to_jpg=self.to_jpg_checkbox.isChecked(),
            to_webp=self.to_webp_checkbox.isChecked(),
            preserve_exif=self.preserve_exif_checkbox.isChecked(),
            allow_enlarge=self.allow_enlarge_checkbox.isChecked(),
            preserve_transparency=self.preserve_transparency_checkbox.isChecked(),
            grayscale=self.grayscale_checkbox.isChecked(),
            sharpen=self.sharpen_checkbox.isChecked(),
            rename_prefix=self.rename_prefix_input.text().strip()
        )
        self.processing_thread.progress_update.connect(self.update_progress) # type: ignore
        self.processing_thread.finished.connect(self.on_processing_finished) # type: ignore
        self.processing_thread.start()
        logging.info(f"Started processing {total_files} image files.")

    def _set_ui_enabled(self, enabled: bool):
        """Enables or disables UI elements during processing."""
        self.start_button.setEnabled(enabled)
        self.select_files_button.setEnabled(enabled)
        self.clear_button.setEnabled(enabled)
        self.drop_area.setEnabled(enabled)
        for group_box in self.findChildren(QGroupBox):
            group_box.setEnabled(enabled)
        self.output_dir_button.setEnabled(enabled)

    def update_progress(self, processed_count: int, total_files: int):
        """Updates the progress bar."""
        self.progress_bar.setValue(processed_count)
        percentage = (processed_count / total_files * 100) if total_files > 0 else 0
        self.progress_bar.setFormat(f"{processed_count}/{total_files} ({percentage:.0f}%)")

    def on_processing_finished(self):
        """Handles the completion of the processing thread."""
        logging.info("Image processing finished.")
        self.progress_bar.setFormat("Processing Complete!")
        self._set_ui_enabled(True)
        self.processing_thread = None


def main():
    """Main function to run the application."""
    try:
        from PIL import Image
    except ImportError:
        print("❌ PIL/Pillow not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "pillow-heif"])
        print("✅ PIL installed. Please restart the application.")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    app.setApplicationName(f"Image Processor (PyQt{PYQT_VERSION})")
    
    # Initialize theme manager after QApplication creation
    window = ImageProcessorGUI()
    
    if THEME_SUPPORT:
        try:
            window.theme_manager = ThemeManager(app)
            # Apply default enhanced dark theme
            window.theme_manager.apply_theme('enhanced_dark', 'custom')
        except Exception as e:
            print(f"⚠️ Theme initialization failed: {e}")
    
    window.show()
    return app.exec() if PYQT_VERSION == 6 else app.exec_()


if __name__ == '__main__':
    sys.exit(main())