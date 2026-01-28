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


