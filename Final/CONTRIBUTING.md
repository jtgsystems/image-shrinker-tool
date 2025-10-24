# Contributing to Enhanced Image Shrinker

Thank you for considering contributing to Enhanced Image Shrinker! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of PyQt6 and image processing

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jtgsystems/enhanced-image-shrinker.git
   cd enhanced-image-shrinker/Final
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run tests to ensure everything works:**
   ```bash
   python -m pytest tests/ -v
   ```

## Development Workflow

### 1. Create a Branch

Create a descriptive branch name:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Changes

- Write clean, readable code following PEP 8 style guide
- Add type hints where appropriate
- Include docstrings for new functions and classes
- Update tests for modified functionality

### 3. Run Code Quality Checks

Before committing, ensure your code passes all checks:

```bash
# Run linter
ruff check . --fix

# Run type checker
mypy shrink.py theme_manager.py --ignore-missing-imports

# Run tests
python -m pytest tests/ -v --cov

# Check test coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### 4. Commit Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: Add new image format support"
# or
git commit -m "fix: Resolve memory leak in batch processing"
```

**Commit message format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code refactoring
- `style:` Code style changes (formatting, etc.)
- `perf:` Performance improvements
- `chore:` Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots (if UI changes)
- Test results

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guide
- Maximum line length: 100 characters
- Use type hints for function parameters and return values
- Write descriptive variable and function names

### Docstring Format

Use Google-style docstrings:

```python
def process_image(filepath: Path, quality: int) -> bool:
    """Process a single image with specified quality.

    Args:
        filepath: Path to the input image file
        quality: JPEG quality (1-100)

    Returns:
        True if processing succeeded, False otherwise

    Raises:
        FileNotFoundError: If input file doesn't exist
    """
    pass
```

### Testing Guidelines

- Write unit tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names: `test_optimize_image_with_transparency`
- Use fixtures for common test setup
- Mock external dependencies (PyQt, file system operations where appropriate)

### Code Review Checklist

Before submitting a pull request, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated (if applicable)
- [ ] No hardcoded secrets or sensitive information
- [ ] Type hints added where appropriate
- [ ] Docstrings added/updated
- [ ] CHANGELOG.md updated (for significant changes)

## Areas for Contribution

### High Priority

- [ ] Add support for additional image formats (AVIF, HEIF)
- [ ] Implement GPU acceleration for batch processing
- [ ] Add progress cancellation functionality
- [ ] Improve memory efficiency for large images
- [ ] Add image preview before/after comparison

### Medium Priority

- [ ] Add more theme options
- [ ] Implement processing profiles save/load
- [ ] Add undo/redo functionality
- [ ] Create plugin architecture for custom filters
- [ ] Add batch rename functionality

### Documentation

- [ ] Add video tutorials
- [ ] Create user guide with screenshots
- [ ] Write architecture documentation
- [ ] Add API documentation
- [ ] Translate documentation to other languages

### Testing

- [ ] Increase test coverage to 90%+
- [ ] Add integration tests
- [ ] Add performance benchmarks
- [ ] Test on different OS versions

## Reporting Bugs

### Before Submitting a Bug Report

1. Check existing issues to avoid duplicates
2. Update to the latest version
3. Try to reproduce with minimal example

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Windows 11, macOS 13, Ubuntu 22.04]
- Python version: [e.g., 3.11.5]
- Application version: [e.g., 2.0.0]

**Additional context**
Any other relevant information.
```

## Feature Requests

We welcome feature requests! Please:

1. Check existing feature requests first
2. Provide clear use case and benefits
3. Include mockups or examples if applicable
4. Be open to discussion and iteration

## Questions?

- Open an issue with the `question` label
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to Enhanced Image Shrinker! 🎨✨
