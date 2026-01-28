"""
Validation functions for desktop file fields.

Pure functions for validating user input.
"""

import os
import re
from typing import Tuple, List, Optional


def validate_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate application name.

    Args:
        name: Application name

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> validate_name("My App")
        (True, None)
        >>> validate_name("")
        (False, 'Name cannot be empty')
    """
    if not name or not name.strip():
        return False, "Name cannot be empty"

    if len(name) > 100:
        return False, "Name must be 100 characters or less"

    return True, None


def validate_exec_path(path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate executable path.

    Args:
        path: Path to executable or command

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> validate_exec_path("/usr/bin/python3")
        (True, None)
        >>> validate_exec_path("")
        (False, 'Exec path cannot be empty')
    """
    if not path or not path.strip():
        return False, "Exec path cannot be empty"

    # Check if it's a valid path or command
    # Allow paths with spaces and special chars for AppImage support
    if len(path) > 500:
        return False, "Exec path is too long"

    return True, None


def validate_icon_path(path: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate icon path or name.

    Args:
        path: Icon file path or icon name (can be None)

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> validate_icon_path(None)
        (True, None)
        >>> validate_icon_path("application-x-executable")
        (True, None)
    """
    if not path:
        return True, None  # Icon is optional

    if len(path) > 500:
        return False, "Icon path is too long"

    return True, None


def validate_appimage_path(path: str) -> Tuple[bool, Optional[str]]:
    """
    Validate AppImage file path.

    Args:
        path: Path to AppImage file

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> validate_appimage_path("/path/to/app.AppImage")
        (True, None)
        >>> validate_appimage_path("/path/to/app.zip")
        (False, 'File must be an AppImage')
    """
    if not path or not path.strip():
        return False, "AppImage path cannot be empty"

    if not path.lower().endswith(".appimage"):
        return False, "File must be an AppImage (.AppImage extension)"

    return True, None


def validate_categories(categories: Optional[List[str]]) -> Tuple[bool, Optional[str]]:
    """
    Validate desktop categories.

    Args:
        categories: List of category strings

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> validate_categories(["Development", "Utility"])
        (True, None)
        >>> validate_categories([])
        (True, None)
    """
    if not categories:
        return True, None  # Categories are optional

    if not isinstance(categories, list):
        return False, "Categories must be a list"

    # Valid desktop categories (subset of freedesktop spec)
    valid_categories = {
        "AudioVideo",
        "Audio",
        "Video",
        "Development",
        "Education",
        "Game",
        "Graphics",
        "Network",
        "Office",
        "Science",
        "Settings",
        "System",
        "Utility",
        "Accessories",
        "Multimedia",
        "Internet",
        "Presentation",
        "Spreadsheet",
        "WordProcessor",
        "Database",
        "Email",
        "Finance",
        "IDE",
        "Debugger",
        "GUIDesigner",
        "Profiling",
        "RevisionControl",
        "Translation",
        "Calendar",
        "ContactManagement",
        "Dictionary",
        "Photography",
        "Viewer",
        "TextEditor",
        "DesktopSettings",
        "HardwareSettings",
        "PackageManager",
        "Screensaver",
        "TerminalEmulator",
        "FileManager",
        "WebBrowser",
        "News",
        "Chat",
        "Monitor",
        "Emulator",
        "Player",
        "Recorder",
        "DiscBurning",
        "ActionGame",
        "AdventureGame",
        "ArcadeGame",
        "BoardGame",
        "CardGame",
        "KidsGame",
        "LogicGame",
        "RolePlayingGame",
        "Shooter",
        "SimulationGame",
        "SportsGame",
        "StrategyGame",
        "Amusement",
        "Archiving",
        "Compression",
        "FileTools",
        "Maps",
        "News",
        "P2P",
        "RemoteAccess",
        "Telephony",
        "TelephonyTools",
        "VideoConference",
        "WebDevelopment",
        "Building",
        "CAD",
        "Publishing",
        "RasterGraphics",
        "VectorGraphics",
        "3DGraphics",
        "Scanning",
        "OCR",
        "Photography",
        "Printing",
        "TextTools",
        "DesktopSettings",
        "HardwareSettings",
        "Printing",
        "PackageManager",
        "Security",
        "Accessibility",
        "Accessibility",
        "Calculator",
        "Clock",
        "TextEditor",
        "Documentation",
        "Adult",
        "Gis",
    }

    for category in categories:
        if category not in valid_categories:
            return False, f"Invalid category: {category}"

    return True, None


def validate_mime_types(mime_types: Optional[List[str]]) -> Tuple[bool, Optional[str]]:
    """
    Validate MIME types.

    Args:
        mime_types: List of MIME type strings

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> validate_mime_types(["text/plain", "text/html"])
        (True, None)
        >>> validate_mime_types(["invalid"])
        (False, 'Invalid MIME type format: invalid')
    """
    if not mime_types:
        return True, None  # MIME types are optional

    if not isinstance(mime_types, list):
        return False, "MIME types must be a list"

    # Basic MIME type validation (type/subtype format)
    mime_pattern = re.compile(r"^[a-zA-Z0-9]+/[a-zA-Z0-9\.\+\-]+$")

    for mime_type in mime_types:
        if not mime_pattern.match(mime_type):
            return False, f"Invalid MIME type format: {mime_type}"

    return True, None


def validate_all_fields(
    name: str,
    exec_path: str,
    icon: Optional[str] = None,
    categories: Optional[List[str]] = None,
    mime_types: Optional[List[str]] = None,
) -> Tuple[bool, List[str]]:
    """
    Validate all fields together.

    Args:
        name: Application name
        exec_path: Executable path
        icon: Icon path (optional)
        categories: List of categories (optional)
        mime_types: List of MIME types (optional)

    Returns:
        Tuple of (all_valid, list_of_errors)

    Example:
        >>> validate_all_fields("App", "/usr/bin/app")
        (True, [])
    """
    errors = []

    valid, error = validate_name(name)
    if not valid:
        errors.append(error)

    valid, error = validate_exec_path(exec_path)
    if not valid:
        errors.append(error)

    valid, error = validate_icon_path(icon)
    if not valid:
        errors.append(error)

    valid, error = validate_categories(categories)
    if not valid:
        errors.append(error)

    valid, error = validate_mime_types(mime_types)
    if not valid:
        errors.append(error)

    return len(errors) == 0, errors
