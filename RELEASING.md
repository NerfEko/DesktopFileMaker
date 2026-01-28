# Release Guide

## Quick Release Process

### 1. Update Version
Edit `pyproject.toml` and `setup.py`:
```python
version = "0.1.0"  # Update to new version
```

### 2. Create Release
```bash
# Commit version bump
git add pyproject.toml setup.py
git commit -m "Release v0.1.0"
git push origin main

# Create and push tag (must start with 'v')
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

### 3. Wait for Build
- GitHub Actions builds AppImage automatically (~10 minutes)
- Check progress: https://github.com/NerfEko/DesktopFileMaker/actions
- Download from: https://github.com/NerfEko/DesktopFileMaker/releases

---

## Manual Build (Optional)

Build AppImage locally:
```bash
./build-appimage.sh 0.1.0
./dist/DesktopFileMaker-0.1.0-x86_64.AppImage  # Test it
```

---

## Versioning

Follow [Semantic Versioning](https://semver.org/):
- **x.0.0** - Breaking changes
- **0.x.0** - New features
- **0.0.x** - Bug fixes

---

## Troubleshooting

**Workflow doesn't trigger:**
- Ensure tag starts with `v` (e.g., `v0.1.0`)

**Build fails:**
- Check GitHub Actions logs
- Test locally: `./build-appimage.sh`

**AppImage doesn't run:**
- Make executable: `chmod +x DesktopFileMaker-*.AppImage`
