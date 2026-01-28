"""
Icon handling for desktop files.

Pure functions for icon validation and management.
"""

import os
from pathlib import Path
from typing import Tuple, Optional, List


# Common icon theme directories
ICON_THEME_DIRS = [
    Path.home() / ".local" / "share" / "icons",
    Path("/usr/local/share/icons"),
    Path("/usr/share/icons"),
]

# Common icon file extensions
ICON_EXTENSIONS = {".png", ".svg", ".xpm", ".jpg", ".jpeg", ".gif"}


def find_icon_in_themes(icon_name: str) -> Optional[Path]:
    """
    Find icon in system icon themes.

    Args:
        icon_name: Icon name (without extension)

    Returns:
        Path to icon file or None if not found

    Example:
        >>> icon = find_icon_in_themes("application-x-executable")
        >>> icon is None or icon.exists()
        True
    """
    for theme_dir in ICON_THEME_DIRS:
        if not theme_dir.exists():
            continue

        # Search in theme directories
        for icon_file in theme_dir.rglob(f"{icon_name}*"):
            if icon_file.suffix in ICON_EXTENSIONS:
                return icon_file

    return None


def validate_icon_file(path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate icon file exists and is valid format.

    Args:
        path: Path to icon file

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> validate_icon_file("/usr/share/icons/hicolor/48x48/apps/app.png")
        (True, None)
    """
    if not path:
        return True, None  # Icon is optional

    icon_path = Path(path)

    # Check if it's a file path or icon name
    if icon_path.exists():
        # It's a file path
        if icon_path.suffix not in ICON_EXTENSIONS:
            return False, f"Unsupported icon format: {icon_path.suffix}"
        return True, None
    else:
        # It might be an icon name from theme
        # Try to find it
        found = find_icon_in_themes(path)
        if found:
            return True, None

        # Icon name not found, but that's okay - it might be available at runtime
        return True, None


def get_icon_suggestions(partial_name: str) -> List[str]:
    """
    Get icon name suggestions based on partial name.

    Args:
        partial_name: Partial icon name

    Returns:
        List of matching icon names

    Example:
        >>> suggestions = get_icon_suggestions("app")
        >>> isinstance(suggestions, list)
        True
    """
    suggestions = set()

    for theme_dir in ICON_THEME_DIRS:
        if not theme_dir.exists():
            continue

        for icon_file in theme_dir.rglob(f"*{partial_name}*"):
            if icon_file.suffix in ICON_EXTENSIONS:
                # Extract icon name (without extension and path)
                icon_name = icon_file.stem
                if partial_name.lower() in icon_name.lower():
                    suggestions.add(icon_name)

    return sorted(list(suggestions))[:10]  # Return top 10


def copy_icon_to_user_share(
    source_path: str, icon_name: str
) -> Tuple[bool, Optional[str], Optional[Path]]:
    """
    Copy icon to user's icon directory.

    Args:
        source_path: Source icon file path
        icon_name: Name for the icon

    Returns:
        Tuple of (success, error_message, destination_path)

    Example:
        >>> success, error, path = copy_icon_to_user_share(
        ...     "/tmp/icon.png",
        ...     "myapp"
        ... )
        >>> success
        True
    """
    source = Path(source_path)

    if not source.exists():
        return False, f"Source icon not found: {source_path}", None

    if source.suffix not in ICON_EXTENSIONS:
        return False, f"Unsupported icon format: {source.suffix}", None

    # Create user icon directory
    user_icon_dir = (
        Path.home() / ".local" / "share" / "icons" / "hicolor" / "48x48" / "apps"
    )

    try:
        user_icon_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return False, f"Failed to create icon directory: {str(e)}", None

    # Destination path
    dest_path = user_icon_dir / f"{icon_name}{source.suffix}"

    try:
        # Copy file
        with open(source, "rb") as src:
            with open(dest_path, "wb") as dst:
                dst.write(src.read())
        return True, None, dest_path
    except PermissionError:
        return False, f"Permission denied: {dest_path}", None
    except Exception as e:
        return False, f"Failed to copy icon: {str(e)}", None


def get_common_icon_names() -> List[str]:
    """
    Get list of common icon names.

    Returns:
        List of common icon names

    Example:
        >>> icons = get_common_icon_names()
        >>> "application-x-executable" in icons
        True
    """
    return [
        "application-x-executable",
        "application-x-python",
        "application-x-shellscript",
        "application-x-java",
        "application-x-ms-dos-executable",
        "application-x-wine-extension-msp",
        "application-x-appimage",
        "application-x-elf-binary",
        "application-x-object",
        "application-x-shared-library",
        "application-x-archive",
        "application-x-compressed-tar",
        "application-x-tar",
        "application-x-zip-compressed",
        "application-x-7z-compressed",
        "application-x-rar-compressed",
        "application-x-gzip",
        "application-x-bzip2",
        "application-x-xz-compressed",
        "application-x-lzip-compressed",
        "application-x-lzma-compressed",
        "application-x-lz4-compressed",
        "application-x-zstd-compressed",
        "application-x-brotli-compressed",
        "application-x-bzip-compressed-tar",
        "application-x-compressed-tar",
        "application-x-xz-compressed-tar",
        "application-x-lzip-compressed-tar",
        "application-x-lzma-compressed-tar",
        "application-x-lz4-compressed-tar",
        "application-x-zstd-compressed-tar",
        "application-x-brotli-compressed-tar",
        "application-x-cpio-compressed-tar",
        "application-x-cpio",
        "application-x-dvi",
        "application-x-font-afm",
        "application-x-font-bdf",
        "application-x-font-dos",
        "application-x-font-framemaker",
        "application-x-font-libgrx",
        "application-x-font-linux-psf",
        "application-x-font-otf",
        "application-x-font-pcf",
        "application-x-font-speedo",
        "application-x-font-sunos-news",
        "application-x-font-tex",
        "application-x-font-tex-tfm",
        "application-x-font-ttf",
        "application-x-font-type1",
        "application-x-font-vfont",
        "application-x-font-winfont",
        "application-x-gzip",
        "application-x-java-applet",
        "application-x-java-jnlp-file",
        "application-x-java-keystore",
        "application-x-java-pack200",
        "application-x-java-serialized-object",
        "application-x-java-source",
        "application-x-javascript",
        "application-x-json",
        "application-x-latex",
        "application-x-lha",
        "application-x-lhz",
        "application-x-lzip",
        "application-x-lzma",
        "application-x-lzop",
        "application-x-ms-dos-executable",
        "application-x-ms-wim",
        "application-x-ms-windows-registry",
        "application-x-ms-windows-shortcut",
        "application-x-ms-windows-theme-pack",
        "application-x-msi",
        "application-x-mswinurl",
        "application-x-object",
        "application-x-ole-storage",
        "application-x-perl",
        "application-x-php",
        "application-x-python",
        "application-x-python-bytecode",
        "application-x-python-source",
        "application-x-rar",
        "application-x-rpm",
        "application-x-rpmdb",
        "application-x-ruby",
        "application-x-shar",
        "application-x-shared-library",
        "application-x-shellscript",
        "application-x-sharedlib",
        "application-x-sqlite3",
        "application-x-stuffit",
        "application-x-subrip",
        "application-x-tar",
        "application-x-tarz",
        "application-x-tex",
        "application-x-tex-gf",
        "application-x-tex-pk",
        "application-x-texinfo",
        "application-x-trash",
        "application-x-troff",
        "application-x-troff-man",
        "application-x-troff-man-compressed",
        "application-x-troff-me",
        "application-x-troff-ms",
        "application-x-ustar",
        "application-x-wais-source",
        "application-x-x509-ca-cert",
        "application-x-xbel",
        "application-x-xfig",
        "application-x-xpinstall",
        "application-x-xz",
        "application-x-xz-compressed-tar",
        "application-x-zip",
        "application-x-zip-compressed",
        "application-x-zoo",
        "application-x-zstd",
        "application-x-zstd-compressed-tar",
    ]
