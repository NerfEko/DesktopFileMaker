# Desktop File Maker

A modern Linux TUI (Terminal User Interface) application for creating and managing `.desktop` files with ease. Perfect for packaging AppImage applications and other executables.

## Features

- ✨ **Interactive TUI** - User-friendly terminal interface built with Textual
- 📦 **AppImage Support** - Special handling for AppImage files with auto-detection
- 🎨 **Icon Management** - Browse and select icons from system icon themes
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

## Installation

### From Source

```bash
git clone https://github.com/yourusername/desktop-file-maker.git
cd desktop-file-maker
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Quick Start

### Run the Application

```bash
python -m src.main
# or if installed
desktop-file-maker
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
pytest
```

With coverage:

```bash
pytest --cov=src tests/
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Move to next field |
| `Shift+Tab` | Move to previous field |
| `Ctrl+S` | Save desktop file |
| `Ctrl+C` | Quit application |

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
