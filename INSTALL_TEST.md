# Installation Testing Guide

## Test the New Installation System

### 1. Clean Installation Test

```bash
cd ~/projects/desktop-file-maker

# Clean any existing installation
rm -rf venv
rm ~/.local/bin/desktop-file-maker

# Test automatic installer
./install.sh
```

Expected output:
- ✓ Found Python version
- ✓ Virtual environment created
- ✓ Dependencies installed
- ✓ Launcher created

### 2. Test Running the Application

```bash
# Method 1: Using the launcher (if ~/.local/bin is in PATH)
desktop-file-maker

# Method 2: Using make
make run

# Method 3: Direct from venv
source venv/bin/activate
python -m src.main
```

### 3. Test Make Commands

```bash
# Show available commands
make help

# Run tests
make test

# Run tests with coverage
make test-cov

# Clean temporary files
make clean

# Reinstall
make reinstall
```

### 4. Test Uninstallation

```bash
make uninstall
```

Expected:
- venv directory removed
- ~/.local/bin/desktop-file-maker removed

---

## Installation Methods Comparison

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| `./install.sh` | **Recommended** | Automatic, guided, adds to PATH | Requires git clone |
| `make install` | Quick install | Simple command | Requires make |
| Manual venv | Full control | Customizable | Manual steps |
| `pipx install` | System-wide | Isolated, in PATH | Requires pipx |

---

## Troubleshooting

### "Command not found: desktop-file-maker"

**Cause:** `~/.local/bin` is not in your PATH

**Solution 1:** Run the installer again and accept the PATH prompt
**Solution 2:** Add manually to your shell config:

```bash
# For bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Solution 3:** Use `make run` instead

### "error: externally-managed-environment" (Arch Linux)

**Cause:** Modern distros prevent system pip usage (PEP 668)

**Solution:** Our installer creates an isolated venv automatically - this error won't occur!

### "Python version too old"

**Cause:** Python < 3.8

**Solution:** Update Python:

```bash
# Arch
sudo pacman -S python

# Ubuntu/Debian
sudo apt update && sudo apt install python3.10

# Fedora
sudo dnf install python3.11
```

---

## What Was Improved?

### Before (Old Installation)
```bash
pip install -e .  # ❌ Fails on Arch/modern distros
                  # ❌ Pollutes system Python
                  # ❌ Requires --break-system-packages
```

### After (New Installation)
```bash
./install.sh      # ✅ Works on ALL Linux distros
                  # ✅ Isolated venv (clean)
                  # ✅ No system pollution
                  # ✅ No root required
                  # ✅ Easy uninstall
```

---

## Files Created by Installer

```
~/projects/desktop-file-maker/
├── venv/                          # Virtual environment (isolated)
│   ├── bin/
│   │   ├── python3                # Isolated Python
│   │   ├── pip                    # Isolated pip
│   │   └── desktop-file-maker     # Entry point script
│   └── lib/                       # Isolated packages
└── ...

~/.local/bin/
└── desktop-file-maker             # System launcher (calls venv)
```

---

## Next Steps After Installation

1. ✅ Run the app: `desktop-file-maker`
2. ✅ Test autocomplete in Exec field (type `bash`, press Tab)
3. ✅ Test autocomplete in Icon field (type `arch`, press Tab)
4. ✅ Test icon search (click "Search" button)
5. ✅ Create a test .desktop file
6. ✅ Check tests: `make test`

---

## Sharing with Others

Send them this simple command:

```bash
git clone https://github.com/NerfEko/DesktopFileMaker.git
cd DesktopFileMaker
./install.sh
```

Works on **any** Linux distribution! 🎉
