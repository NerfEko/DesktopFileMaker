# Desktop File Maker - AUR Development Branch

[![Release](https://img.shields.io/github/v/release/NerfEko/DesktopFileMaker)](https://github.com/NerfEko/DesktopFileMaker/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **⚠️ This is the AUR development branch** - Contains AUR packaging files and developer tools. For end-users, see the [main branch](https://github.com/NerfEko/DesktopFileMaker).

A modern Linux TUI application for creating and managing `.desktop` files. This branch contains AUR (Arch User Repository) packaging infrastructure and development tools.

## AUR Package Status

This branch contains ready-to-use AUR packages:

- **`desktop-file-maker`** - Stable release package
- **`desktop-file-maker-git`** - Development version package

## Quick AUR Testing

```bash
# Test the stable package
makepkg -si

# Test the git package  
makepkg -si -p PKGBUILD-git

# Install from AUR (when published)
yay -S desktop-file-maker
paru -S desktop-file-maker-git
```

## AUR Files

- **`PKGBUILD`** - Standard release package
- **`PKGBUILD-git`** - Git development package
- **`AUR-GUIDE.md`** - Complete AUR submission guide

## Development

### Building AppImage

```bash
./build-appimage.sh       # Full standalone build
./build-appimage-fast.sh  # Fast build using system Python
```

### Local Testing

# Run application
desktop-file-maker
```

## For AUR Maintainers

See [AUR-GUIDE.md](AUR-GUIDE.md) for complete AUR submission instructions.

### Package Testing Checklist

- [ ] `makepkg -si` builds successfully
- [ ] Application runs: `desktop-file-maker`
- [ ] Desktop entry created in applications menu
- [ ] Clean uninstall with `pacman -R desktop-file-maker`
- [ ] No dependency conflicts

## Repository Structure

```
├── PKGBUILD          # AUR stable package
├── PKGBUILD-git      # AUR git package  
├── AUR-GUIDE.md      # AUR submission guide
├── src/              # Application source
├── build-appimage.sh # AppImage builder
└── install.sh        # Local installer
```

## Core Features

- 🎯 **Terminal UI** - Modern TUI built with Textual
- 🔍 **Icon Search** - Multi-source icon discovery
- 🚀 **Smart Completion** - Tab completion for paths and executables
- ✅ **Validation** - Real-time desktop file validation
- 📦 **AppImage Ready** - Perfect for packaging applications

## Main Branch

For end-users and standard installation instructions, see the [main branch](https://github.com/NerfEko/DesktopFileMaker).

---

*This AUR-testing branch is for Arch Linux packaging development and testing.*
