#!/usr/bin/env python3
"""
Unit tests for ImageProcessor class
"""
import tempfile
import pytest
from pathlib import Path
from PIL import Image
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shrink import ImageProcessor


class TestImageProcessor:
    """Test cases for ImageProcessor functionality."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test outputs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def sample_image(self, temp_dir):
        """Create a sample test image."""
        img_path = temp_dir / "test_image.jpg"
        img = Image.new('RGB', (800, 600), color='blue')
        img.save(img_path, 'JPEG')
        return img_path

    @pytest.fixture
    def sample_rgba_image(self, temp_dir):
        """Create a sample RGBA image with transparency."""
        img_path = temp_dir / "test_rgba.png"
        img = Image.new('RGBA', (800, 600), color=(255, 0, 0, 128))
        img.save(img_path, 'PNG')
        return img_path

    def test_convert_to_rgb_rgb_image(self):
        """Test converting an RGB image (should return same)."""
        img = Image.new('RGB', (100, 100), color='red')
        result = ImageProcessor.convert_to_rgb(img)
        assert result.mode == 'RGB'
        assert result.size == (100, 100)

    def test_convert_to_rgb_rgba_image(self):
        """Test converting an RGBA image to RGB."""
        img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 128))
        result = ImageProcessor.convert_to_rgb(img)
        assert result.mode == 'RGB'
        assert result.size == (100, 100)

    def test_convert_to_rgb_palette_with_transparency(self):
        """Test converting a palette image with transparency."""
        img = Image.new('P', (100, 100))
        img.info['transparency'] = 0
        result = ImageProcessor.convert_to_rgb(img)
        assert result.mode == 'RGB'

    def test_optimize_image_basic(self, sample_image, temp_dir):
        """Test basic image optimization."""
        output_dir = temp_dir / "output"
        result = ImageProcessor.optimize_image(
            filepath=sample_image,
            output_dir=output_dir,
            resize_method="none",
            resize_value=None,
            quality=85,
            to_jpg=True,
            to_webp=False,
            preserve_exif=False,
            allow_enlarge=False,
            preserve_transparency=False,
            grayscale=False,
            sharpen=False,
            rename_prefix=""
        )
        assert result is True
        assert (output_dir / 'jpg' / 'test_image.jpg').exists()

    def test_optimize_image_percentage_resize(self, sample_image, temp_dir):
        """Test image resizing by percentage."""
        output_dir = temp_dir / "output"
        result = ImageProcessor.optimize_image(
            filepath=sample_image,
            output_dir=output_dir,
            resize_method="percentage",
            resize_value=50,
            quality=85,
            to_jpg=True,
            to_webp=False,
            preserve_exif=False,
            allow_enlarge=False,
            preserve_transparency=False,
            grayscale=False,
            sharpen=False,
            rename_prefix=""
        )
        assert result is True
        output_file = output_dir / 'jpg' / 'test_image.jpg'
        assert output_file.exists()

        # Check dimensions
        with Image.open(output_file) as img:
            assert img.size == (400, 300)  # 50% of 800x600

    def test_optimize_image_fixed_size_resize(self, sample_image, temp_dir):
        """Test image resizing to fixed dimensions."""
        output_dir = temp_dir / "output"
        result = ImageProcessor.optimize_image(
            filepath=sample_image,
            output_dir=output_dir,
            resize_method="fixed_size",
            resize_value=(640, 480),
            quality=85,
            to_jpg=True,
            to_webp=False,
            preserve_exif=False,
            allow_enlarge=False,
            preserve_transparency=False,
            grayscale=False,
            sharpen=False,
            rename_prefix=""
        )
        assert result is True
        output_file = output_dir / 'jpg' / 'test_image.jpg'
        assert output_file.exists()

        with Image.open(output_file) as img:
            assert img.size == (640, 480)

    def test_optimize_image_max_width_resize(self, sample_image, temp_dir):
        """Test image resizing with max width constraint."""
        output_dir = temp_dir / "output"
        result = ImageProcessor.optimize_image(
            filepath=sample_image,
            output_dir=output_dir,
            resize_method="max_width",
            resize_value=400,
            quality=85,
            to_jpg=True,
            to_webp=False,
            preserve_exif=False,
            allow_enlarge=False,
            preserve_transparency=False,
            grayscale=False,
            sharpen=False,
            rename_prefix=""
        )
        assert result is True
        output_file = output_dir / 'jpg' / 'test_image.jpg'
        assert output_file.exists()

        with Image.open(output_file) as img:
            assert img.size[0] == 400
            assert img.size[1] == 300  # Maintains aspect ratio

    def test_optimize_image_webp_output(self, sample_image, temp_dir):
        """Test WebP format output."""
        output_dir = temp_dir / "output"
        result = ImageProcessor.optimize_image(
            filepath=sample_image,
            output_dir=output_dir,
            resize_method="none",
            resize_value=None,
            quality=85,
            to_jpg=False,
            to_webp=True,
            preserve_exif=False,
            allow_enlarge=False,
            preserve_transparency=False,
            grayscale=False,
            sharpen=False,
            rename_prefix=""
        )
        assert result is True
        assert (output_dir / 'webp' / 'test_image.webp').exists()

    def test_optimize_image_both_formats(self, sample_image, temp_dir):
        """Test output to both JPG and WebP formats."""
        output_dir = temp_dir / "output"
        result = ImageProcessor.optimize_image(
            filepath=sample_image,
            output_dir=output_dir,
            resize_method="none",
            resize_value=None,
            quality=85,
            to_jpg=True,
            to_webp=True,
            preserve_exif=False,
            allow_enlarge=False,
            preserve_transparency=False,
            grayscale=False,
            sharpen=False,
            rename_prefix=""
        )
        assert result is True
        assert (output_dir / 'jpg' / 'test_image.jpg').exists()
        assert (output_dir / 'webp' / 'test_image.webp').exists()

    def test_optimize_image_with_prefix(self, sample_image, temp_dir):
        """Test image optimization with filename prefix."""
        output_dir = temp_dir / "output"
        result = ImageProcessor.optimize_image(
            filepath=sample_image,
            output_dir=output_dir,
            resize_method="none",
            resize_value=None,
            quality=85,
            to_jpg=True,
            to_webp=False,
            preserve_exif=False,
            allow_enlarge=False,
            preserve_transparency=False,
            grayscale=False,
            sharpen=False,
            rename_prefix="optimized"
        )
        assert result is True
        assert (output_dir / 'jpg' / 'optimized_test_image.jpg').exists()

    def test_optimize_image_grayscale(self, sample_image, temp_dir):
        """Test grayscale conversion."""
        output_dir = temp_dir / "output"
        result = ImageProcessor.optimize_image(
            filepath=sample_image,
            output_dir=output_dir,
            resize_method="none",
            resize_value=None,
            quality=85,
            to_jpg=True,
            to_webp=False,
            preserve_exif=False,
            allow_enlarge=False,
            preserve_transparency=False,
            grayscale=True,
            sharpen=False,
            rename_prefix=""
        )
        assert result is True
        output_file = output_dir / 'jpg' / 'test_image.jpg'
        assert output_file.exists()

    def test_optimize_image_invalid_file(self, temp_dir):
        """Test handling of invalid/nonexistent file."""
        output_dir = temp_dir / "output"
        result = ImageProcessor.optimize_image(
            filepath=temp_dir / "nonexistent.jpg",
            output_dir=output_dir,
            resize_method="none",
            resize_value=None,
            quality=85,
            to_jpg=True,
            to_webp=False,
            preserve_exif=False,
            allow_enlarge=False,
            preserve_transparency=False,
            grayscale=False,
            sharpen=False,
            rename_prefix=""
        )
        assert result is False

    def test_get_all_image_files_single_file(self, sample_image):
        """Test getting image files from a single file path."""
        files = ImageProcessor.get_all_image_files([sample_image])
        assert len(files) == 1
        assert files[0] == sample_image

    def test_get_all_image_files_directory(self, temp_dir):
        """Test getting all image files from a directory."""
        # Create multiple test images
        for i in range(3):
            img_path = temp_dir / f"test_{i}.jpg"
            img = Image.new('RGB', (100, 100), color='red')
            img.save(img_path, 'JPEG')

        files = ImageProcessor.get_all_image_files([temp_dir])
        assert len(files) == 3

    def test_get_all_image_files_mixed(self, temp_dir, sample_image):
        """Test getting files from mixed file and directory paths."""
        # Create additional images in subdirectory
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        for i in range(2):
            img_path = subdir / f"sub_{i}.png"
            img = Image.new('RGB', (100, 100), color='green')
            img.save(img_path, 'PNG')

        files = ImageProcessor.get_all_image_files([sample_image, subdir])
        assert len(files) == 3  # 1 from sample_image + 2 from subdir

    def test_extensions_coverage(self):
        """Test that all documented extensions are supported."""
        expected_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
        assert ImageProcessor.extensions == expected_extensions
