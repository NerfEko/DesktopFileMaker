#!/usr/bin/env bash
#
# Test script for AUR package validation
# Run this before submitting to AUR
#

set -e

echo "🔍 Testing Desktop File Maker AUR package..."
echo ""

# Check if we're in the right directory
if [[ ! -f "PKGBUILD" ]]; then
    echo "❌ PKGBUILD not found. Run this from the directory containing PKGBUILD"
    exit 1
fi

# Test build
echo "📦 Building package..."
makepkg -f

# Check with namcap if available
if command -v namcap &> /dev/null; then
    echo "🔍 Checking with namcap..."
    namcap PKGBUILD
    namcap *.pkg.tar.zst
else
    echo "⚠️ namcap not found, skipping package validation"
fi

# Generate .SRCINFO
echo "📝 Generating .SRCINFO..."
makepkg --printsrcinfo > .SRCINFO

echo ""
echo "✅ Package built successfully!"
echo ""
echo "Next steps:"
echo "1. Install and test: sudo pacman -U *.pkg.tar.zst"
echo "2. Test the command: desktop-file-maker"
echo "3. If all works, submit to AUR following AUR-GUIDE.md"

echo ""
echo "📁 Files ready for AUR submission:"
ls -la PKGBUILD .SRCINFO *.desktop 2>/dev/null || echo "   PKGBUILD .SRCINFO"