#!/usr/bin/env bash
#
# Build AppImage for Desktop File Maker (Fast version using system Python)
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
APP_VERSION="${1:-0.1.1}"
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
    echo -e "${BLUE}  Building AppImage for Desktop File Maker (Fast)${NC}"
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
    
    if ! python3 -m pip --version &> /dev/null; then
        print_error "pip is not available"
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
    mkdir -p "$APPDIR/usr/lib/python3/site-packages"
    mkdir -p "$APPDIR/usr/share/applications"
    mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
    
    print_success "AppDir structure created"
}

# Install dependencies using virtual environment
install_python_deps() {
    print_info "Installing Python dependencies..."
    
    # Create a temporary virtual environment
    TEMP_VENV="$BUILD_DIR/temp_venv"
    rm -rf "$TEMP_VENV"
    python3 -m venv "$TEMP_VENV"
    
    # Install dependencies in the venv
    print_info "Installing Python packages..."
    "$TEMP_VENV/bin/pip" install --no-warn-script-location \
        textual>=0.47.0 \
        requests>=2.31.0 \
        ddgs>=9.0.0
    
    # Copy site-packages to AppDir
    print_info "Copying Python packages..."
    cp -r "$TEMP_VENV/lib/python"*/site-packages/* "$APPDIR/usr/lib/python3/site-packages/"
    
    # Clean up temp venv
    rm -rf "$TEMP_VENV"
    
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
    
    # Create the main AppRun script
    cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash

# AppRun script for Desktop File Maker

APPDIR="$(dirname "$(readlink -f "$0")")"

# Set Python environment to use system Python with bundled packages
export PYTHONPATH="$APPDIR/usr/lib/python3/site-packages:$APPDIR/usr:$PYTHONPATH"

# Use system Python
PYTHON="python3"

# Run the application
cd "$APPDIR/usr" || exit 1
"$PYTHON" -m src.main "$@"
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