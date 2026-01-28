# Setup Guide for Arch Linux

Since Arch Linux uses PEP 668 to prevent system-wide Python package installation, we use a virtual environment.

## Quick Setup

### 1. Create Virtual Environment (One-time setup)

```bash
cd ~/projects/desktop-file-maker
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### 2. Run Tests

**Option A: Using the test script (recommended)**
```bash
cd ~/projects/desktop-file-maker
./test.sh
```

**Option B: Manual activation**
```bash
cd ~/projects/desktop-file-maker
source venv/bin/activate
pytest tests/ -v
```

### 3. Run the Application

**Option A: Using the run script (recommended)**
```bash
cd ~/projects/desktop-file-maker
./run.sh
```

**Option B: Manual activation**
```bash
cd ~/projects/desktop-file-maker
source venv/bin/activate
python -m src.main
```

## Virtual Environment Explained

The virtual environment (`venv/`) is a self-contained Python installation that doesn't interfere with your system Python. It's created in the project directory.

### Activating the Virtual Environment

```bash
source venv/bin/activate
```

You'll see `(venv)` in your shell prompt when activated.

### Deactivating the Virtual Environment

```bash
deactivate
```

## Convenient Aliases

Add these to your `~/.bashrc` or `~/.zshrc` for quick access:

```bash
# Desktop File Maker
alias dfm='cd ~/projects/desktop-file-maker && ./run.sh'
alias dfm-test='cd ~/projects/desktop-file-maker && ./test.sh'
alias dfm-dev='cd ~/projects/desktop-file-maker && source venv/bin/activate'
```

Then reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

Now you can use:
```bash
dfm              # Run the app
dfm-test         # Run tests
dfm-dev          # Activate dev environment
```

## Using as a Library

If you want to use the core modules in your own Python code:

```bash
cd ~/projects/desktop-file-maker
source venv/bin/activate
python
```

Then in Python:
```python
from src.core import DesktopFileData, generate_desktop_content

data = DesktopFileData(name="MyApp", exec_path="/path/to/app")
content = generate_desktop_content(data)
print(content)
```

## Troubleshooting

### "command not found: pip"
Use `python -m pip` instead:
```bash
python -m pip install package-name
```

### "ModuleNotFoundError: No module named 'src'"
Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

### Virtual environment not working
Recreate it:
```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Permission denied on run.sh or test.sh
Make them executable:
```bash
chmod +x run.sh test.sh
```

## What's in the Virtual Environment

The virtual environment includes:
- **textual** - TUI framework
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- All project dependencies

## Updating Dependencies

If you update `requirements.txt` or `setup.py`:

```bash
source venv/bin/activate
pip install -e ".[dev]"
```

## Removing the Virtual Environment

If you need to clean up:

```bash
rm -rf venv
```

You can always recreate it with the setup steps above.

## More Information

- See `README.md` for user guide
- See `DEVELOPMENT.md` for development guide
- See `QUICKSTART.md` for code examples
