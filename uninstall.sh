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
USER_BIN_DIR="$HOME/.local/bin"
SYSTEM_BIN_DIR="/usr/local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Detect installation mode
USER_LAUNCHER="$USER_BIN_DIR/desktop-file-maker"
SYSTEM_LAUNCHER="$SYSTEM_BIN_DIR/desktop-file-maker"
INSTALL_MODE="none"

if [[ -f "$SYSTEM_LAUNCHER" ]]; then
    INSTALL_MODE="system"
    LAUNCHER="$SYSTEM_LAUNCHER"
elif [[ -f "$USER_LAUNCHER" ]]; then
    INSTALL_MODE="user"
    LAUNCHER="$USER_LAUNCHER"
fi

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
    
    if [[ "$INSTALL_MODE" == "none" ]]; then
        print_warning "No Desktop File Maker installation detected"
        echo "Checking for remaining files..."
    else
        echo "Detected $INSTALL_MODE installation of Desktop File Maker."
    fi
    
    echo "This will completely remove Desktop File Maker from your system."
    if [[ "$INSTALL_MODE" == "system" ]]; then
        echo "System-wide installation requires sudo to remove."
    fi
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
    
    # Remove launcher script based on installation mode
    if [[ "$INSTALL_MODE" == "system" ]] && [[ -f "$SYSTEM_LAUNCHER" ]]; then
        sudo rm -f "$SYSTEM_LAUNCHER"
        print_success "Removed system launcher script (with sudo)"
    elif [[ "$INSTALL_MODE" == "user" ]] && [[ -f "$USER_LAUNCHER" ]]; then
        rm -f "$USER_LAUNCHER"
        print_success "Removed user launcher script"
    fi
    
    # Also check for and remove the other location (cleanup)
    if [[ -f "$USER_LAUNCHER" ]] && [[ "$INSTALL_MODE" != "user" ]]; then
        rm -f "$USER_LAUNCHER"
        print_success "Removed user launcher script (cleanup)"
    fi
    if [[ -f "$SYSTEM_LAUNCHER" ]] && [[ "$INSTALL_MODE" != "system" ]]; then
        if sudo -n true 2>/dev/null; then
            sudo rm -f "$SYSTEM_LAUNCHER"
            print_success "Removed system launcher script (cleanup)"
        else
            print_warning "System launcher exists but no sudo access for removal: $SYSTEM_LAUNCHER"
        fi
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
    
    if [[ "$INSTALL_MODE" == "system" ]]; then
        echo ""
        echo "The system-wide command 'desktop-file-maker' has been removed."
    fi
    
    echo ""
    echo "The source code directory can be safely deleted:"
    echo -e "${YELLOW}rm -rf \"$SCRIPT_DIR\"${NC}"
    echo ""
    print_info "No configuration files were modified during installation or removal"
}

# Run uninstallation
main