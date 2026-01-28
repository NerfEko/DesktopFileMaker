#!/usr/bin/env bash
#
# Uninstaller for Desktop File Maker
# Removes all files without affecting system configuration
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Print functions
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Desktop File Maker - Uninstaller${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Main uninstallation
main() {
    print_header
    
    echo "This will completely remove Desktop File Maker from your system."
    echo "No system configuration files will be modified."
    echo ""
    echo -n "Are you sure you want to continue? (y/N) "
    read -r response
    
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        print_info "Uninstallation cancelled"
        exit 0
    fi
    
    echo ""
    print_info "Removing Desktop File Maker..."
    
    # Remove virtual environment
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
        print_success "Removed virtual environment"
    fi
    
    # Remove launcher script
    LAUNCHER="$BIN_DIR/desktop-file-maker"
    if [ -f "$LAUNCHER" ]; then
        rm -f "$LAUNCHER"
        print_success "Removed launcher script"
    fi
    
    # Remove desktop entry
    DESKTOP_FILE="$DESKTOP_DIR/desktop-file-maker.desktop"
    if [ -f "$DESKTOP_FILE" ]; then
        rm -f "$DESKTOP_FILE"
        print_success "Removed desktop entry"
    fi
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
        print_success "Updated desktop database"
    fi
    
    echo ""
    print_success "Desktop File Maker has been completely removed"
    echo ""
    echo "The source code directory can be safely deleted:"
    echo -e "${YELLOW}rm -rf \"$SCRIPT_DIR\"${NC}"
    echo ""
    print_info "No system configuration files were modified during installation or removal"
}

# Run uninstallation
main