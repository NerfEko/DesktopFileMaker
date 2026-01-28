# AUR Submission Guide for Desktop File Maker

This guide explains how to submit Desktop File Maker to the AUR (Arch User Repository).

## Prerequisites

1. **Arch Linux system** (or Arch-based distro)
2. **AUR account**: Register at https://aur.archlinux.org/register/
3. **SSH key**: Upload your SSH public key to your AUR account
4. **Required packages**: Install `base-devel`, `git`, and `namcap`
   ```bash
   sudo pacman -S base-devel git namcap
   ```

## Step 1: Create Release

First, create a proper release on GitHub:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Then go to GitHub → Releases → Create a new release based on this tag.

## Step 2: Test PKGBUILD Locally

1. **Test the stable version**:
   ```bash
   # Copy PKGBUILD to a test directory
   mkdir -p ~/aur-test/desktop-file-maker
   cp PKGBUILD ~/aur-test/desktop-file-maker/
   cd ~/aur-test/desktop-file-maker
   
   # Update checksums
   updpkgsums
   
   # Build and test
   makepkg -si
   
   # Test the installed package
   desktop-file-maker --help
   ```

2. **Test the git version**:
   ```bash
   mkdir -p ~/aur-test/desktop-file-maker-git  
   cp PKGBUILD-git ~/aur-test/desktop-file-maker-git/PKGBUILD
   cd ~/aur-test/desktop-file-maker-git
   
   makepkg -si
   ```

## Step 3: Check with namcap

```bash
# Check PKGBUILD
namcap PKGBUILD

# Check built package
namcap *.pkg.tar.zst
```

## Step 4: Submit to AUR

### For the stable version (desktop-file-maker):

```bash
# Clone AUR repository
git clone ssh://aur@aur.archlinux.org/desktop-file-maker.git
cd desktop-file-maker

# Copy files
cp ../PKGBUILD .
cp ../appimage/desktop-file-maker.desktop .

# Generate .SRCINFO
makepkg --printsrcinfo > .SRCINFO

# Commit and push
git add PKGBUILD .SRCINFO desktop-file-maker.desktop
git commit -m "Initial import: desktop-file-maker 0.1.0"
git push origin master
```

### For the git version (desktop-file-maker-git):

```bash
# Clone AUR repository  
git clone ssh://aur@aur.archlinux.org/desktop-file-maker-git.git
cd desktop-file-maker-git

# Copy files
cp ../PKGBUILD-git PKGBUILD
cp ../appimage/desktop-file-maker.desktop .

# Generate .SRCINFO
makepkg --printsrcinfo > .SRCINFO

# Commit and push
git add PKGBUILD .SRCINFO desktop-file-maker.desktop  
git commit -m "Initial import: desktop-file-maker-git"
git push origin master
```

## Step 5: Update PKGBUILD Information

Before submitting, update the PKGBUILD files with:

1. **Your maintainer information**:
   ```bash
   # Maintainer: Your Name <your.email@example.com>
   ```

2. **Correct checksums**:
   ```bash
   updpkgsums  # This updates sha256sums automatically
   ```

3. **Test on clean system** (optional but recommended):
   ```bash
   # In a chroot or container
   extra-x86_64-build
   ```

## File Structure for AUR

Each AUR package needs:

```
desktop-file-maker/
├── PKGBUILD                    # Build instructions
├── .SRCINFO                    # Generated metadata
└── desktop-file-maker.desktop  # Desktop entry file
```

## Maintenance

After submission:

1. **Monitor comments** on the AUR page
2. **Update when new versions** are released:
   ```bash
   # Update pkgver and pkgrel in PKGBUILD
   updpkgsums
   makepkg --printsrcinfo > .SRCINFO
   git commit -am "Update to version X.X.X"
   git push
   ```

3. **Respond to bug reports** and feature requests

## Installation for Users

Once on AUR, users can install with:

```bash
# Using yay
yay -S desktop-file-maker

# Using paru  
paru -S desktop-file-maker

# Manual
git clone https://aur.archlinux.org/desktop-file-maker.git
cd desktop-file-maker
makepkg -si
```

## Tips

- **Start with `-git` package**: It's easier and helps establish the package
- **Follow naming conventions**: Use lowercase with hyphens
- **Include good description**: Help users find your package
- **Test thoroughly**: Build on clean system if possible
- **Keep it updated**: Maintain the package after submission

## Resources

- [AUR Submission Guidelines](https://wiki.archlinux.org/title/AUR_submission_guidelines)
- [PKGBUILD Manual](https://wiki.archlinux.org/title/PKGBUILD)
- [Arch Package Guidelines](https://wiki.archlinux.org/title/Arch_package_guidelines)