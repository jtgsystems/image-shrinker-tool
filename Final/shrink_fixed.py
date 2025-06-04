#!/usr/bin/env python3
"""
Enhanced Image Shrinker Tool - Quick Fix Version
================================================
Backward-compatible version that works with both PyQt5 and PyQt6
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple, Optional, Union

# Try PyQt6 first, fall back to PyQt5
try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    PYQT_VERSION = 6
except ImportError:
    try:
        from PyQt5.QtWidgets import *
        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        PYQT_VERSION = 5
    except ImportError:
        print("❌ Neither PyQt6 nor PyQt5 found. Installing PyQt6...")
        os.system("pip install PyQt6 Pillow pillow-heif")
        sys.exit(1)

try:
    from PIL import Image, ImageEnhance
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    print("❌ PIL/Pillow not found. Installing...")
    os.system("pip install Pillow pillow-heif")
    sys.exit(1)

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

# Setup logging
logging.basicConfig(
    filename='image_processor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class QuickImageProcessor:
    """Quick and efficient image processor with auto-dependency management."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.heif'}
    
    @staticmethod
    def process_image(input_path: Path, output_dir: Path, quality: int = 85, 
                     max_width: Optional[int] = None, to_webp: bool = False) -> bool:
        """Process single image with error handling."""
        try:
            with Image.open(input_path) as img:
                # Handle orientation
                if hasattr(img, '_getexif') and img._getexif():
                    for tag, value in img._getexif().items():
                        if tag == 274:  # Orientation tag
                            if value == 3:
                                img = img.rotate(180, expand=True)
                            elif value == 6:
                                img = img.rotate(270, expand=True)
                            elif value == 8:
                                img = img.rotate(90, expand=True)
                
                # Resize if needed
                if max_width and img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert for JPEG if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    if img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1])
                    img = background
                
                # Save JPEG
                output_dir.mkdir(parents=True, exist_ok=True)
                jpg_path = output_dir / f"{input_path.stem}.jpg"
                img.save(jpg_path, 'JPEG', quality=quality, optimize=True)
                
                # Save WebP if requested
                if to_webp:
                    webp_path = output_dir / f"{input_path.stem}.webp"
                    img.save(webp_path, 'WebP', quality=quality, method=6)
                
                print(f"✅ Processed: {input_path.name}")
                return True
                
        except Exception as e:
            print(f"❌ Failed: {input_path.name} - {e}")
            logging.error(f"Failed to process {input_path}: {e}")
            return False

class SimpleImageGUI(QMainWindow):
    """Simplified GUI that works with both PyQt5 and PyQt6."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Quick Image Shrinker (PyQt{PYQT_VERSION})")
        self.setGeometry(100, 100, 600, 400)
        self.selected_files = []
        self.output_dir = Path.cwd() / "Shrunk"
        self.setup_ui()
    
    def setup_ui(self):
        """Setup simplified UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🖼️ Quick Image Shrinker")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter if PYQT_VERSION == 6 else Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # File selection
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout(file_group)
        
        self.file_label = QLabel("No files selected")
        file_layout.addWidget(self.file_label)
        
        file_buttons = QHBoxLayout()
        self.select_btn = QPushButton("📁 Select Images")
        self.clear_btn = QPushButton("🗑️ Clear")
        file_buttons.addWidget(self.select_btn)
        file_buttons.addWidget(self.clear_btn)
        file_layout.addLayout(file_buttons)
        
        layout.addWidget(file_group)
        
        # Settings
        settings_group = QGroupBox("Settings")
        settings_layout = QFormLayout(settings_group)
        
        # Quality
        self.quality_slider = QSlider(Qt.Orientation.Horizontal if PYQT_VERSION == 6 else Qt.Horizontal)
        self.quality_slider.setRange(10, 100)
        self.quality_slider.setValue(85)
        self.quality_label = QLabel("85%")
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_label)
        settings_layout.addRow("Quality:", quality_layout)
        
        # Max width
        self.width_spin = QSpinBox()
        self.width_spin.setRange(100, 5000)
        self.width_spin.setValue(1920)
        self.width_spin.setSuffix(" px")
        settings_layout.addRow("Max Width:", self.width_spin)
        
        # WebP option
        self.webp_check = QCheckBox("Also save as WebP")
        settings_layout.addRow(self.webp_check)
        
        # Output directory
        output_layout = QHBoxLayout()
        self.output_label = QLabel(str(self.output_dir))
        self.output_btn = QPushButton("📁 Change")
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_btn)
        settings_layout.addRow("Output:", output_layout)
        
        layout.addWidget(settings_group)
        
        # Progress
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # Process button
        self.process_btn = QPushButton("🚀 Process Images")
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.process_btn)
        
        # Connect signals
        self.select_btn.clicked.connect(self.select_files)
        self.clear_btn.clicked.connect(self.clear_files)
        self.output_btn.clicked.connect(self.select_output)
        self.process_btn.clicked.connect(self.process_images)
        self.quality_slider.valueChanged.connect(self.update_quality_label)
    
    def update_quality_label(self, value):
        """Update quality label."""
        self.quality_label.setText(f"{value}%")
    
    def select_files(self):
        """Select image files."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Image Files", "",
            "Image Files (*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp *.heic *.heif);;All Files (*)"
        )
        if files:
            self.selected_files = [Path(f) for f in files]
            self.file_label.setText(f"{len(self.selected_files)} files selected")
    
    def clear_files(self):
        """Clear selected files."""
        self.selected_files = []
        self.file_label.setText("No files selected")
        self.progress.setValue(0)
    
    def select_output(self):
        """Select output directory."""
        directory = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", str(self.output_dir)
        )
        if directory:
            self.output_dir = Path(directory)
            self.output_label.setText(str(self.output_dir))
    
    def process_images(self):
        """Process selected images."""
        if not self.selected_files:
            QMessageBox.warning(self, "No Files", "Please select images to process.")
            return
        
        # Setup progress
        total_files = len(self.selected_files)
        self.progress.setMaximum(total_files)
        self.progress.setValue(0)
        
        # Get settings
        quality = self.quality_slider.value()
        max_width = self.width_spin.value()
        to_webp = self.webp_check.isChecked()
        
        # Process images
        processed = 0
        failed = 0
        
        for i, file_path in enumerate(self.selected_files):
            if QuickImageProcessor.process_image(
                file_path, self.output_dir, quality, max_width, to_webp
            ):
                processed += 1
            else:
                failed += 1
            
            self.progress.setValue(i + 1)
            QApplication.processEvents()
        
        # Show results
        message = f"Processing complete!\n\n"
        message += f"✅ Processed: {processed} images\n"
        if failed > 0:
            message += f"❌ Failed: {failed} images\n"
        message += f"📁 Output: {self.output_dir}"
        
        QMessageBox.information(self, "Complete", message)

def install_dependencies():
    """Auto-install missing dependencies."""
    print("🔧 Checking dependencies...")
    
    missing = []
    
    # Check PyQt
    try:
        import PyQt6
    except ImportError:
        try:
            import PyQt5
        except ImportError:
            missing.append("PyQt6")
    
    # Check PIL
    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")
    
    if missing:
        print(f"📦 Installing: {', '.join(missing)}")
        os.system(f"pip install {' '.join(missing)} pillow-heif")
        print("✅ Dependencies installed. Please restart the application.")
        return False
    
    return True

def main():
    """Main application entry point."""
    print("🚀 Quick Image Shrinker")
    print("=" * 30)
    
    if not install_dependencies():
        input("Press Enter to exit...")
        return
    
    app = QApplication(sys.argv)
    app.setApplicationName("Quick Image Shrinker")
    
    window = SimpleImageGUI()
    window.show()
    
    return app.exec() if PYQT_VERSION == 6 else app.exec_()

if __name__ == '__main__':
    sys.exit(main())
