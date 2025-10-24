# CI/CD Setup Instructions

## GitHub Actions Workflow Setup

Due to GitHub App permission restrictions, the CI/CD workflow file needs to be added manually to the repository.

### Steps to Add CI/CD Workflow

1. **Navigate to your repository on GitHub**

2. **Create the workflow directory:**
   - Go to the "Actions" tab
   - Click "New workflow"
   - Click "set up a workflow yourself"

3. **Create the file:** `.github/workflows/ci.yml`

4. **Copy the workflow content from:** `/home/user/image-shrinker-tool/.github/workflows/ci.yml`

5. **Or use this content:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop, claude/* ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint-and-test:
    name: Lint and Test
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r Final/requirements-dev.txt

    - name: Lint with ruff
      run: |
        cd Final
        ruff check . --output-format=github

    - name: Type check with mypy
      run: |
        cd Final
        mypy shrink.py theme_manager.py build_cross_platform.py --ignore-missing-imports
      continue-on-error: true

    - name: Run tests with pytest
      run: |
        cd Final
        python -m pytest tests/ -v --cov=. --cov-report=xml --cov-report=term

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
      with:
        file: ./Final/coverage.xml
        flags: unittests
        name: codecov-umbrella
      if: matrix.python-version == '3.11' && matrix.os == 'ubuntu-latest'

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install safety bandit

    - name: Run safety check
      run: |
        cd Final
        safety check --file requirements.txt --file requirements-dev.txt || true

    - name: Run bandit security scan
      run: |
        cd Final
        bandit -r . -f json -o bandit-report.json || true
        bandit -r . -f txt || true

  build-executables:
    name: Build Executables
    runs-on: ${{ matrix.os }}
    needs: [lint-and-test]
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r Final/requirements.txt
        pip install PyInstaller>=5.13.0

    - name: Build executable (Linux)
      if: runner.os == 'Linux'
      run: |
        cd Final
        python build_cross_platform.py || echo "Build completed with warnings"
      continue-on-error: true

    - name: Build executable (Windows)
      if: runner.os == 'Windows'
      run: |
        cd Final
        python build_cross_platform.py || echo "Build completed with warnings"
      continue-on-error: true

    - name: Build executable (macOS)
      if: runner.os == 'macOS'
      run: |
        cd Final
        python build_cross_platform.py || echo "Build completed with warnings"
      continue-on-error: true

    - name: Upload artifacts
      uses: actions/upload-artifact@v4
      with:
        name: image-shrinker-${{ matrix.os }}
        path: Final/dist/*
      if: success()

  code-quality:
    name: Code Quality Check
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install radon complexity-report

    - name: Check code complexity
      run: |
        cd Final
        radon cc . -a -nb || true
        radon mi . -nb || true
```

6. **Commit the workflow file directly on GitHub**

7. **Verify the workflow runs** by checking the "Actions" tab

## Why Manual Setup?

The GitHub App used for this commit doesn't have the `workflows` permission, which is required to create or modify workflow files. This is a security feature to prevent automated tools from modifying CI/CD pipelines.

## Alternative: Local Setup

If you have direct push access (not through a GitHub App):

```bash
# Copy the workflow file from the project root
cp ../.github/workflows/ci.yml .github/workflows/ci.yml

# Commit and push
git add .github/workflows/ci.yml
git commit -m "chore: Add GitHub Actions CI/CD workflow"
git push
```

## Verification

Once the workflow is added, you should see:
- ✅ Automated tests running on push/PR
- ✅ Multi-OS and multi-Python version testing
- ✅ Security scans
- ✅ Build artifacts
- ✅ Code coverage reports

The workflow file is located at: `/home/user/image-shrinker-tool/.github/workflows/ci.yml`
