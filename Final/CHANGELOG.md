# Changelog

All notable changes to Enhanced Image Shrinker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-24

### Added
- ✨ Complete rewrite with PyQt6 for modern UI
- 🎨 Advanced theme system with 12+ built-in themes
- ⚡ Parallel processing for 3x faster batch operations
- 📦 Cross-platform executable build system
- 🔧 Processing profiles for saving and reusing settings
- 🎭 Support for PyQtDarkTheme and Qt-Material theme libraries
- 📊 Real-time progress tracking with detailed statistics
- 🖼️ Support for HEIC/HEIF image formats
- 🔄 Auto-orientation based on EXIF data
- 📈 Progressive JPEG support for web optimization
- 💾 Format conversion during processing (JPG, WebP, PNG)
- 🎚️ Adaptive quality algorithms
- 📏 Multiple resize methods (percentage, fixed size, max width)
- ✨ Image enhancement options (grayscale, sharpening)
- 📁 Automatic output folder organization by format
- 🖱️ Drag and drop file/folder support

### Changed
- 🔄 Migrated from PyQt5 to PyQt6
- ⚡ Improved processing speed by 3x using multiprocessing
- 🎨 Completely redesigned user interface
- 💾 Reduced memory usage by 40%
- 📦 Improved build system for better cross-platform support

### Fixed
- 🐛 Fixed transparency handling in PNG/WebP conversion
- 🐛 Resolved memory leaks in batch processing
- 🐛 Fixed EXIF data preservation issues
- 🐛 Corrected aspect ratio calculations in resize operations

### Security
- 🔒 Removed hardcoded credentials and secrets
- 🔒 Improved input validation and sanitization
- 🔒 Added comprehensive error handling

### Developer Experience
- 🧪 Added comprehensive unit test suite (39 tests)
- 📝 Added type hints throughout codebase
- 🔍 Integrated ruff linter and mypy type checker
- 📚 Added comprehensive documentation
- 🚀 Set up GitHub Actions CI/CD pipeline
- 📦 Created pyproject.toml for modern Python packaging
- 📝 Added CONTRIBUTING.md guidelines

## [1.x] - Legacy

### Features
- Basic PyQt5 interface
- Simple image compression
- Limited format support
- Single-threaded processing

---

## Upgrade Notes

### From 1.x to 2.0

**Breaking Changes:**
- Requires Python 3.8+ (previously 3.6+)
- PyQt6 instead of PyQt5 (automatic fallback included)
- Configuration file format changed

**Migration:**
1. Back up your existing settings
2. Install new dependencies: `pip install -r requirements.txt`
3. Run the new version
4. Reconfigure your processing preferences

**New Features to Try:**
- Try the new theme system (Menu → Theme)
- Create custom processing profiles
- Use parallel processing for large batches
- Export to WebP format for better compression

---

## Release Schedule

- **Major versions** (X.0.0): Breaking changes, major new features
- **Minor versions** (x.X.0): New features, backward compatible
- **Patch versions** (x.x.X): Bug fixes, security updates

## Support

- Report bugs: [GitHub Issues](https://github.com/jtgsystems/enhanced-image-shrinker/issues)
- Feature requests: [GitHub Discussions](https://github.com/jtgsystems/enhanced-image-shrinker/discussions)
- Security issues: See SECURITY.md

---

*Enhanced Image Shrinker v2.0 - Professional image compression made simple*
*© 2025 John Thomas Gallie - JTG Systems*
