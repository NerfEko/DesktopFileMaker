# Desktop File Maker

[![Release](https://img.shields.io/github/v/release/NerfEko/DesktopFileMaker)](https://github.com/NerfEko/DesktopFileMaker/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A modern, optimized Linux TUI (Terminal User Interface) application for creating and managing `.desktop` files with ease. **Runs entirely in your terminal** - perfect for packaging AppImage applications and other executables.

> **⚠️ Important**: This is a **terminal application** that must be run from a command line. It provides a beautiful text-based interface within your terminal window.

## Features

- 🖥️ **Terminal-Based Interface** - Beautiful TUI that runs in your terminal
- 🔍 **Icon Search** - Search and download icons from the internet (optional)
- 🎨 **Visual Feedback** - Color-coded interface with real-time validation
- 📦 **AppImage Support** - Special handling for AppImage files with auto-detection
- ✅ **Field Validation** - Real-time validation of all desktop file fields
- 📝 **Live Preview** - See your desktop file content before saving
- 📂 **Smart Placement** - Automatically places files in the correct locations:
  - User scope: `~/.local/share/applications/`
  - System scope: `/usr/share/applications/` (requires sudo)
- 🔧 **Full Field Support** - All standard desktop file fields:
  - Name, Exec, Icon, Comment
  - Categories, Terminal flag
  - And more!
- 🐧 **Universal Linux Support** - Works on Arch, Ubuntu, Fedora, Debian, and more
- ⚡ **Modern Packaging** - Uses pyproject.toml, no legacy setup.py
- 🛡️ **Graceful Dependencies** - Optional features degrade gracefully when dependencies are missing
- 🏠 **Non-Intrusive Install** - Never modifies .bashrc, .zshrc, or system PATH
- 📱 **Application Menu Integration** - Shows up in your desktop application menu

## Installation

### Option 1: AppImage (Easiest - No Installation Required) 🚀

**Download and run immediately - works on any Linux distro!**

1. **Download the latest AppImage** from the [Releases page](https://github.com/NerfEko/DesktopFileMaker/releases/latest)

2. **Make it executable and run from terminal:**
   ```bash
   # Download (example filename)
   wget https://github.com/NerfEko/DesktopFileMaker/releases/download/v0.1.0/DesktopFileMaker-0.1.0-x86_64.AppImage
   
   # Make executable
   chmod +x DesktopFileMaker-0.1.0-x86_64.AppImage
   
   # Run from terminal (required - this is a TUI app)
   ./DesktopFileMaker-0.1.0-x86_64.AppImage
   ```

**⚠️ Must run from terminal**: Double-clicking the AppImage file won't work because this is a terminal user interface application. You need to open a terminal and run it from the command line.

**That's it!** No installation, no dependencies, just download and run from your terminal.

---

Desktop File Maker also supports installation from source on **all Linux distributions** (Arch, Ubuntu, Fedora, Debian, etc.)

### Option 2: Automatic Installation (Zero System Impact) 🎯

**Installs completely isolated - no system modifications needed!**

```bash
git clone https://github.com/NerfEko/DesktopFileMaker.git
cd DesktopFileMaker
./install.sh
```

This will:
- ✅ Create an isolated virtual environment (no system pollution)
- ✅ Install all dependencies automatically
- ✅ Create a launcher in `~/.local/bin/desktop-file-maker`
- ✅ **Add to application menu** (no PATH modification required!)
- ✅ Work on Arch, Ubuntu, Fedora, and any modern Linux distro
- ✅ **Zero system configuration changes** - completely self-contained
- ✅ Easy to uninstall with `./uninstall.sh`

**Why this approach rocks:**
- 🚫 **No .bashrc/.zshrc modifications** - your shell config stays clean
- 🚫 **No PATH changes required** - works without environment setup
- 🎯 **Application menu integration** - launch like any other app
- 🧹 **Clean uninstall** - removes everything without traces

### Option 3: Using Make

```bash
git clone https://github.com/NerfEko/DesktopFileMaker.git
cd DesktopFileMaker
make install
```

### Option 4: Manual Installation

```bash
git clone https://github.com/NerfEko/DesktopFileMaker.git
cd DesktopFileMaker

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install
pip install -e .
```

### Option 5: Using pipx (Isolated Installation)

```bash
pipx install git+https://github.com/NerfEko/DesktopFileMaker.git
```

### Why This Installation Method?

Modern Linux distributions (Arch, Fedora 38+, Ubuntu 23.04+) follow [PEP 668](https://peps.python.org/pep-0668/) which prevents `pip install` from modifying system Python packages. Our installer:

- 🔒 **Safe**: Uses isolated virtual environment (no `--break-system-packages` needed)
- 🎯 **Universal**: Works on ALL Linux distros (Arch, Ubuntu, Fedora, Debian, etc.)
- 🚫 **No Root**: Installs to `~/.local` (no sudo required)
- 🧹 **Clean**: Easy to uninstall completely
- ⚡ **Modern**: Follows Python packaging best practices

**For Arch users:** This avoids the `error: externally-managed-environment` without breaking your system!

**Prefer no installation at all?** Use the **AppImage** (Option 1) - just download and run!

---

## Building AppImage Locally

Want to build the AppImage yourself?

```bash
# Clone the repository
git clone https://github.com/NerfEko/DesktopFileMaker.git
cd DesktopFileMaker

# Build AppImage
./build-appimage.sh

# Find the AppImage in dist/
./dist/DesktopFileMaker-*.AppImage
```

The build script will:
- Download appimagetool automatically
- Create a bundled Python environment
- Package everything into a single executable
- Output to `dist/` directory

## Quick Start

### How to Run the Application

**⚠️ Important**: This application runs in your terminal and provides a text-based user interface. You cannot double-click to run it.

```bash
# Method 1: Using AppImage (recommended)
# Download from releases, then:
chmod +x DesktopFileMaker-0.1.0-x86_64.AppImage
./DesktopFileMaker-0.1.0-x86_64.AppImage

# Method 2: From application menu (if installed with ./install.sh)
# Search for "Desktop File Maker" in your application menu

# Method 3: Using the launcher directly:
~/.local/bin/desktop-file-maker

# Method 4: Using make (if you have the source code):
make run

# Method 5: From virtual environment (development):
source venv/bin/activate
python -m src.main
```

### Terminal Requirements

- Any modern terminal emulator (GNOME Terminal, Konsole, xterm, etc.)
- Terminal with color support (most modern terminals)
- Minimum 80x24 character terminal size (larger recommended)

### Basic Usage

1. **Open a terminal** (Ctrl+Alt+T on most Linux distributions)
2. **Navigate** to where you downloaded/installed the application
3. **Run the command** (see methods above)
4. **Use the TUI interface**:
   - Use `Tab` and `Shift+Tab` to navigate between fields
   - Use arrow keys within multi-option fields
   - Press `Ctrl+S` to save
   - Press `Ctrl+C` to quit

### Create a Desktop File

1. Launch the application
2. Fill in the required fields:
   - **Name**: Application name (e.g., "My App")
   - **Exec**: Path to executable (e.g., `/home/user/app.AppImage`)
   - **Icon**: Icon name or path (optional)
   - **Comment**: Brief description (optional)
3. Click "Generate Preview" to see the result
4. Click "Save" to create the `.desktop` file

### For AppImage Files

1. Select your AppImage file in the Exec field
2. The app will auto-detect the name from the filename
3. Choose an icon (optional)
4. Save!

## Usage Examples

### Creating a Desktop File for an AppImage

```
Name: My Cool App
Exec: /home/user/Downloads/MyCoolApp-1.0.AppImage
Icon: application-x-appimage
Comment: An awesome application
Categories: Development;Utility
Terminal: No
```

### Creating a Desktop File for a Python Script

```
Name: Python Tool
Exec: /usr/bin/python3 /home/user/scripts/tool.py
Icon: application-x-python
Comment: A useful Python tool
Categories: Development;Utility
Terminal: Yes
```

## Desktop File Format

The application generates standard `.desktop` files following the [freedesktop.org Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/).

Example generated file:

```ini
[Desktop Entry]
Type=Application
Name=My App
Comment=A cool application
Exec=/home/user/app.AppImage
Icon=app-icon
Categories=Development;Utility
Terminal=false
StartupNotify=true
```

## Project Structure

```
desktop-file-maker/
├── src/
│   ├── core/                    # Core business logic (optimized)
│   │   ├── desktop_file.py      # Desktop file generation/parsing
│   │   ├── validation.py        # Field validation
│   │   ├── file_system.py       # File operations
│   │   ├── icon_handler.py      # Icon management (cleaned up)
│   │   └── icon_search.py       # Icon search (with graceful degradation)
│   ├── tui/                     # Terminal UI
│   │   ├── app.py               # Main application (optimized imports)
│   │   └── widgets/             # Custom widgets (cleaned up)
│   │       ├── exec_suggester.py
│   │       ├── icon_path_suggester.py
│   │       └── icon_selector.py
│   └── main.py                  # Entry point
├── tests/                       # Test suite
│   ├── test_desktop_file.py
│   ├── test_validation.py
│   ├── test_file_system.py
│   └── test_icon_search.py
├── appimage/                    # AppImage build resources
│   ├── generate_icon.py
│   └── desktop-file-maker.desktop
├── build-appimage.sh            # AppImage build script
├── pyproject.toml              # Modern Python packaging
├── requirements.txt
└── README.md
```

### Recent Optimizations (v0.1.0)

- 🗑️ **Removed 130+ lines** of unused `get_common_icon_names()` function
- 🧹 **Cleaned up imports** - removed unused `Static` widgets
- 📦 **Modernized packaging** - removed legacy `setup.py`, using `pyproject.toml`
- 🔧 **Optional dependencies** - icon search gracefully degrades if `ddgs` not available
- 📁 **Removed empty directories** - cleaned up unused `screens/` folder

## What's New in v0.1.0

This release focuses on **code quality and optimization**:

### ✨ Major Cleanup
- **163 net lines removed** from codebase while maintaining full functionality
- Eliminated redundant code and unused functions
- Streamlined imports and dependencies

### 📦 Better Packaging
- Modern `pyproject.toml` configuration
- Simplified dependency management
- Consistent requirements across all config files

### 🛡️ Improved Reliability  
- Made optional dependencies truly optional
- Better error handling for missing components
- Graceful degradation of features

### 🚀 AppImage Ready
- Fresh AppImage build (50MB, x86_64)
- Fully self-contained with embedded Python
- Works on any Linux distribution without installation

## Architecture

### Core Modules (Pure Functions)

The core logic is built with pure functions following functional programming principles:

- **desktop_file.py**: Generate and parse `.desktop` file content
- **validation.py**: Validate all input fields
- **file_system.py**: Handle file operations and placement
- **icon_handler.py**: Manage icon selection and copying

### TUI Layer

Built with [Textual](https://textual.textualize.io/), a modern Python TUI framework:

- Responsive, keyboard-driven interface
- Real-time validation feedback
- Live preview of generated files
- Intuitive form layout

## Testing

Run the test suite:

```bash
# Using make
make test

# With coverage
make test-cov

# Or manually
source venv/bin/activate
pytest

# With coverage
pytest --cov=src tests/
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Move to next field |
| `Shift+Tab` | Move to previous field |
| `Enter` | Activate button/field (context-dependent) |
| `Space` | Toggle selection in select fields |
| `Arrow Keys` | Navigate within multi-option fields |
| `Ctrl+S` | Save desktop file |
| `Ctrl+C` | Quit application |
| `Escape` | Cancel current operation/close modal |

### Field-Specific Controls

- **Text Input Fields**: Type normally, use Ctrl+A to select all
- **Select Fields**: Use arrow keys or mouse to choose options
- **Autocomplete**: Start typing, suggestions appear automatically
- **Icon Search**: Click "Search" button or press Enter in icon field

## Uninstallation

**Complete removal with zero traces:**

```bash
# Using the uninstall script (recommended)
./uninstall.sh

# Or manually remove files:
rm -rf venv
rm ~/.local/bin/desktop-file-maker
rm ~/.local/share/applications/desktop-file-maker.desktop

# Then delete the source directory
rm -rf ~/path/to/desktop-file-maker
```

**No configuration files to clean up** - the installer never modifies your shell configuration!

## Common Use Cases

### 1. Create Desktop Entry for AppImage

```bash
# Launch the app
desktop-file-maker

# Fill in:
# Name: MyApp
# Exec: /home/user/Downloads/MyApp.AppImage
# Icon: myapp
# Categories: Development
# Save!
```

### 2. Create Desktop Entry for Shell Script

```bash
# Name: My Script
# Exec: /usr/local/bin/myscript.sh
# Terminal: Yes
# Categories: Utility
```

### 3. Create Desktop Entry for Python Application

```bash
# Name: Python App
# Exec: /usr/bin/python3 /opt/myapp/main.py
# Icon: application-x-python
# Categories: Development;Utility
```

## Troubleshooting

### AppImage Issues

**"Permission denied" when running AppImage:**
```bash
chmod +x DesktopFileMaker-*.AppImage
./DesktopFileMaker-*.AppImage
```

**"Nothing happens" when double-clicking AppImage:**
This is normal! The application is a terminal interface. You must run it from a terminal:
```bash
# Open terminal first (Ctrl+Alt+T), then:
./DesktopFileMaker-*.AppImage
```

**AppImage won't execute:**
- Ensure you're on a 64-bit Linux system
- Check that FUSE is installed: `sudo apt install fuse` (Ubuntu/Debian)
- Try running from terminal to see error messages

### Terminal Interface Issues

**"Interface looks broken or garbled":**
- Ensure your terminal supports color (most modern terminals do)
- Try a different terminal emulator (GNOME Terminal, Konsole, xterm)
- Make sure terminal is at least 80x24 characters

**"Can't navigate the interface":**
- Use `Tab` and `Shift+Tab` to move between fields
- Use arrow keys within selection fields
- Press `Ctrl+C` to quit
- Press `Ctrl+S` to save

**"Icon search not working":**
Icon search is optional and requires internet connection. The app works fine without it for basic desktop file creation.

### Desktop File Issues

### Desktop file not appearing in application menu

1. Ensure the file is saved to `~/.local/share/applications/`
2. Run `update-desktop-database ~/.local/share/applications/`
3. Restart your desktop environment or application menu

### Icon not showing

1. Verify the icon name exists in your system icon theme
2. Use `find /usr/share/icons -name "icon-name*"` to search
3. Or provide the full path to an icon file

### Permission denied when saving

1. Check that `~/.local/share/applications/` exists and is writable
2. Create it if needed: `mkdir -p ~/.local/share/applications/`
3. For system-wide installation, use `sudo` (not recommended)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Submit a pull request

## Code Standards

This project follows functional programming principles:

- ✅ Pure functions (no side effects)
- ✅ Immutable data structures
- ✅ Composition over inheritance
- ✅ Explicit dependencies
- ✅ Comprehensive tests

See [code-quality.md](docs/code-quality.md) for details.

## License

MIT License - see LICENSE file for details

## Resources

- [freedesktop.org Desktop Entry Spec](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
- [Textual Documentation](https://textual.textualize.io/)
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for Linux users
