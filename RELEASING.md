# Creating a Release with AppImage

This guide explains how to create a new release of Desktop File Maker with an automatically built AppImage.

## Release Process

### 1. Update Version Number

Update the version in these files:
- `pyproject.toml` - Update `version = "x.y.z"`
- `setup.py` - Update `version="x.y.z"`

### 2. Commit Changes

```bash
git add pyproject.toml setup.py
git commit -m "Bump version to x.y.z"
git push origin main
```

### 3. Create and Push Tag

```bash
# Create a tag (must start with 'v')
git tag -a v0.1.0 -m "Release v0.1.0"

# Push the tag
git push origin v0.1.0
```

### 4. Automatic Build

Once the tag is pushed, GitHub Actions will:
1. ✅ Build the AppImage automatically
2. ✅ Test that it runs
3. ✅ Create a GitHub Release
4. ✅ Upload the AppImage as a downloadable asset

The process takes about 5-10 minutes.

### 5. Check the Release

1. Go to https://github.com/NerfEko/DesktopFileMaker/releases
2. Verify the new release appears
3. Download and test the AppImage

## Manual Release (if needed)

If you need to build and release manually:

### Build AppImage Locally

```bash
# Build
./build-appimage.sh 0.1.0

# Test
./dist/DesktopFileMaker-0.1.0-x86_64.AppImage
```

### Create Release on GitHub

1. Go to https://github.com/NerfEko/DesktopFileMaker/releases/new
2. Create tag: `v0.1.0`
3. Set release title: `Desktop File Maker v0.1.0`
4. Add release notes
5. Upload the AppImage from `dist/`
6. Publish release

## Release Checklist

Before creating a release:

- [ ] All tests pass (`make test`)
- [ ] Version updated in `pyproject.toml` and `setup.py`
- [ ] CHANGELOG updated (if you have one)
- [ ] README accurate
- [ ] All changes committed and pushed
- [ ] Tag created and pushed
- [ ] GitHub Actions workflow succeeds
- [ ] AppImage downloads and runs correctly

## Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (x.0.0): Breaking changes
- **MINOR** (0.x.0): New features, backward compatible
- **PATCH** (0.0.x): Bug fixes, backward compatible

Examples:
- `v0.1.0` - Initial release
- `v0.1.1` - Bug fix
- `v0.2.0` - New feature (autocomplete added)
- `v1.0.0` - First stable release

## Troubleshooting

### Workflow doesn't trigger
- Make sure tag starts with `v` (e.g., `v0.1.0`, not `0.1.0`)
- Check GitHub Actions tab for errors

### Build fails
- Check the GitHub Actions logs
- Test build locally first: `./build-appimage.sh`
- Ensure all dependencies are in `requirements.txt`

### AppImage doesn't run
- Check it's executable: `chmod +x DesktopFileMaker-*.AppImage`
- Test on multiple distros (Ubuntu, Fedora, Arch)
- Check for missing system libraries

## First Release

To create your first release:

```bash
# Make sure everything is ready
make test
git status

# Update version to 0.1.0
# Edit pyproject.toml and setup.py

# Commit
git add pyproject.toml setup.py
git commit -m "Release v0.1.0"
git push origin main

# Create and push tag
git tag -a v0.1.0 -m "Initial release - v0.1.0

Features:
- Interactive TUI for creating .desktop files
- Smart autocomplete for executables and icons
- Multi-source icon search (SimpleIcons, Iconify, DuckDuckGo)
- Color-coded icon results
- Universal Linux installation
- AppImage for portable use"

git push origin v0.1.0
```

Then wait for GitHub Actions to build and release!
