# Maintainer: Your Name <your.email@example.com>
pkgname=desktop-file-maker
pkgver=0.1.1
pkgrel=1
pkgdesc="A modern Linux TUI application for creating and managing .desktop files"
arch=('any')
url="https://github.com/NerfEko/DesktopFileMaker"
license=('MIT')
depends=('python' 'python-textual' 'python-requests')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
optdepends=('python-ddgs: for icon search functionality')
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Will need to be updated with actual checksum

build() {
    cd "DesktopFileMaker-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "DesktopFileMaker-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
    
    # Install license
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    
    # Create desktop entry directly (since the file might not be in the tarball)
    install -Dm644 /dev/stdin "$pkgdir/usr/share/applications/desktop-file-maker.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Desktop File Maker
Comment=Create and manage .desktop files with a modern TUI
Exec=desktop-file-maker
Icon=application-x-desktop
Categories=Development;Utility;
Terminal=true
StartupNotify=false
Keywords=desktop;file;creator;appimage;
EOF
}