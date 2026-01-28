#!/usr/bin/env bash
#
# Build AppImage for Desktop File Maker
# Creates a portable executable for all Linux distributions
#

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
APP_NAME="DesktopFileMaker"
APP_VERSION="${1:-0.1.0}"
PYTHON_VERSION="3.11"
ARCH="x86_64"

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build/appimage"
APPDIR="$BUILD_DIR/$APP_NAME.AppDir"
OUTPUT_DIR="$SCRIPT_DIR/dist"

# Print functions
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Building AppImage for Desktop File Maker${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Check dependencies
check_dependencies() {
    print_info "Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed"
        exit 1
    fi
    
    print_success "Dependencies OK"
}

# Download appimagetool if needed
get_appimagetool() {
    print_info "Getting appimagetool..."
    
    APPIMAGETOOL="$BUILD_DIR/appimagetool-${ARCH}.AppImage"
    
    if [ -f "$APPIMAGETOOL" ]; then
        print_success "appimagetool already downloaded"
        return
    fi
    
    mkdir -p "$BUILD_DIR"
    
    curl -L -o "$APPIMAGETOOL" \
        "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-${ARCH}.AppImage"
    
    chmod +x "$APPIMAGETOOL"
    print_success "appimagetool downloaded"
}

# Create AppDir structure
create_appdir() {
    print_info "Creating AppDir structure..."
    
    # Clean and create AppDir
    rm -rf "$APPDIR"
    mkdir -p "$APPDIR/usr/bin"
    mkdir -p "$APPDIR/usr/lib"
    mkdir -p "$APPDIR/usr/share/applications"
    mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
    
    print_success "AppDir structure created"
}

# Install Python and dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."
    
    # Create virtual environment in AppDir
    python3 -m venv "$APPDIR/usr/python"
    
    # Activate and install dependencies
    source "$APPDIR/usr/python/bin/activate"
    
    pip install --upgrade pip setuptools wheel
    pip install -e "$SCRIPT_DIR"
    
    deactivate
    
    print_success "Python dependencies installed"
}

# Copy application files
copy_app_files() {
    print_info "Copying application files..."
    
    # Copy source code
    cp -r "$SCRIPT_DIR/src" "$APPDIR/usr/"
    
    # Copy icon if exists
    if [ -f "$SCRIPT_DIR/appimage/desktop-file-maker.png" ]; then
        cp "$SCRIPT_DIR/appimage/desktop-file-maker.png" \
           "$APPDIR/usr/share/icons/hicolor/256x256/apps/desktop-file-maker.png"
        ln -sf "usr/share/icons/hicolor/256x256/apps/desktop-file-maker.png" \
           "$APPDIR/desktop-file-maker.png"
    fi
    
    print_success "Application files copied"
}

# Create AppRun script
create_apprun() {
    print_info "Creating AppRun script..."
    
    cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash

# AppRun script for Desktop File Maker

APPDIR="$(dirname "$(readlink -f "$0")")"

# Set Python path
export PYTHONPATH="$APPDIR/usr:$PYTHONPATH"
export PATH="$APPDIR/usr/python/bin:$PATH"

# Use bundled Python
PYTHON="$APPDIR/usr/python/bin/python3"

# Run the application
exec "$PYTHON" -m src.main "$@"
EOF
    
    chmod +x "$APPDIR/AppRun"
    print_success "AppRun script created"
}

# Create .desktop file (for AppImage metadata only, not installed)
create_desktop_file() {
    print_info "Creating desktop file metadata..."
    
    cat > "$APPDIR/desktop-file-maker.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Desktop File Maker
Comment=Create and manage Linux .desktop files
Exec=desktop-file-maker
Icon=desktop-file-maker
Categories=Utility;Development;
Terminal=false
EOF
    
    print_success "Desktop file metadata created"
}

# Build AppImage
build_appimage() {
    print_info "Building AppImage..."
    
    mkdir -p "$OUTPUT_DIR"
    
    APPIMAGE_OUTPUT="$OUTPUT_DIR/$APP_NAME-$APP_VERSION-${ARCH}.AppImage"
    
    # Remove old AppImage if exists
    rm -f "$APPIMAGE_OUTPUT"
    
    # Build with appimagetool
    ARCH=$ARCH "$BUILD_DIR/appimagetool-${ARCH}.AppImage" \
        --comp gzip \
        "$APPDIR" \
        "$APPIMAGE_OUTPUT"
    
    chmod +x "$APPIMAGE_OUTPUT"
    
    print_success "AppImage built successfully!"
    echo ""
    echo "Output: $APPIMAGE_OUTPUT"
    
    # Get file size
    SIZE=$(du -h "$APPIMAGE_OUTPUT" | cut -f1)
    echo "Size: $SIZE"
}

# Main build process
main() {
    print_header
    
    check_dependencies
    get_appimagetool
    create_appdir
    install_python_deps
    copy_app_files
    create_apprun
    create_desktop_file
    build_appimage
    
    echo ""
    print_success "Build complete!"
    echo ""
    echo "To run the AppImage:"
    echo -e "  ${GREEN}$OUTPUT_DIR/$APP_NAME-$APP_VERSION-${ARCH}.AppImage${NC}"
    echo ""
}

# Run build
main
