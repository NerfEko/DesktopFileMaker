# Desktop File Maker

[![Release](https://img.shields.io/github/v/release/NerfEko/DesktopFileMaker)](https://github.com/NerfEko/DesktopFileMaker/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A modern Linux TUI (Terminal User Interface) application for creating and managing `.desktop` files with ease. Perfect for packaging AppImage applications and other executables.

## Features

- ✨ **Interactive TUI** - User-friendly terminal interface built with Textual
- 🚀 **Smart Autocomplete** - Tab completion for executables and icon paths
- 🔍 **Multi-Source Icon Search** - Search icons from SimpleIcons, Iconify, and DuckDuckGo
- 🎨 **Color-Coded Results** - Easy-to-identify icon sources with visual indicators
- 📦 **AppImage Support** - Special handling for AppImage files with auto-detection
- 🖼️ **Icon Management** - Browse and select icons from system icon themes
- ✅ **Validation** - Real-time validation of all desktop file fields
- 📝 **Live Preview** - See your desktop file content before saving
- 📂 **Smart Placement** - Automatically places files in the correct locations:
  - User scope: `~/.local/share/applications/`
  - System scope: `/usr/share/applications/` (requires sudo)
- 🔧 **Full Field Support** - All standard desktop file fields:
  - Name, Exec, Icon, Comment
  - Categories, MIME types, Keywords
  - Terminal, NoDisplay, Hidden flags
  - And more!
- 🐧 **Universal Linux Support** - Works on Arch, Ubuntu, Fedora, Debian, and more

## Installation

### Option 1: AppImage (Easiest - No Installation Required) 🚀

**Download and run immediately - works on any Linux distro!**

1. **Download the latest AppImage** from the [Releases page](https://github.com/NerfEko/DesktopFileMaker/releases/latest)

2. **Make it executable and run:**
   ```bash
   chmod +x DesktopFileMaker-*.AppImage
   ./DesktopFileMaker-*.AppImage
   ```

**That's it!** No installation, no dependencies, just download and run.

---

Desktop File Maker also supports installation from source on **all Linux distributions** (Arch, Ubuntu, Fedora, Debian, etc.)

### Option 2: Automatic Installation (Recommended for Development)

The easiest way to install on any Linux distribution:

```bash
git clone https://github.com/NerfEko/DesktopFileMaker.git
cd DesktopFileMaker
./install.sh
```

This will:
- ✅ Create an isolated virtual environment (no system pollution)
- ✅ Install all dependencies automatically
- ✅ Create a launcher in `~/.local/bin/desktop-file-maker`
- ✅ Work on Arch, Ubuntu, Fedora, and any modern Linux distro
- ✅ No root/sudo required

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

### Run the Application

After installation, run with:

```bash
# If using AppImage:
./DesktopFileMaker-*.AppImage

# If installed from source and ~/.local/bin is in your PATH:
desktop-file-maker

# Or using make:
make run

# Or from venv directly:
source venv/bin/activate
python -m src.main
```

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
│   ├── core/                    # Core business logic
│   │   ├── desktop_file.py      # Desktop file generation/parsing
│   │   ├── validation.py        # Field validation
│   │   ├── file_system.py       # File operations
│   │   └── icon_handler.py      # Icon management
│   ├── tui/                     # Terminal UI
│   │   ├── app.py               # Main application
│   │   ├── screens/             # Screen components
│   │   └── widgets/             # Custom widgets
│   └── main.py                  # Entry point
├── tests/                       # Test suite
│   ├── test_desktop_file.py
│   ├── test_validation.py
│   └── test_file_system.py
├── README.md
├── requirements.txt
└── setup.py
```

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
| `Tab` | Move to next field / Accept autocomplete |
| `Shift+Tab` | Move to previous field |
| `Right Arrow` | Accept autocomplete suggestion |
| `Ctrl+S` | Save desktop file |
| `Ctrl+C` | Quit application |

## Uninstallation

```bash
# Using make
make uninstall

# Or manually
rm -rf venv
rm ~/.local/bin/desktop-file-maker
```

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
