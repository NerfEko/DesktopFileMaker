"""
File system operations for desktop files.

Pure functions for determining correct paths and file operations.
"""

import os
from pathlib import Path
from typing import Tuple, Optional, List


def get_user_applications_dir() -> Path:
    """
    Get user's applications directory.

    Returns:
        Path to ~/.local/share/applications/

    Example:
        >>> path = get_user_applications_dir()
        >>> "applications" in str(path)
        True
    """
    return Path.home() / ".local" / "share" / "applications"


def get_system_applications_dirs() -> List[Path]:
    """
    Get system-wide applications directories.

    Returns:
        List of system application directories

    Example:
        >>> dirs = get_system_applications_dirs()
        >>> any("applications" in str(d) for d in dirs)
        True
    """
    dirs = []

    # Standard XDG locations
    xdg_data_dirs = os.environ.get("XDG_DATA_DIRS", "/usr/local/share:/usr/share")
    for data_dir in xdg_data_dirs.split(":"):
        if data_dir:
            app_dir = Path(data_dir) / "applications"
            dirs.append(app_dir)

    return dirs


def ensure_directory_exists(path: Path) -> Tuple[bool, Optional[str]]:
    """
    Ensure directory exists, creating if necessary.

    Args:
        path: Directory path

    Returns:
        Tuple of (success, error_message)

    Example:
        >>> success, error = ensure_directory_exists(Path("/tmp/test"))
        >>> success
        True
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True, None
    except PermissionError:
        return False, f"Permission denied: {path}"
    except Exception as e:
        return False, f"Failed to create directory: {str(e)}"


def get_desktop_file_path(filename: str, user_scope: bool = True) -> Path:
    """
    Get full path for desktop file.

    Args:
        filename: Desktop file name (e.g., "myapp.desktop")
        user_scope: If True, use user directory; if False, use system

    Returns:
        Full path to desktop file

    Example:
        >>> path = get_desktop_file_path("myapp.desktop")
        >>> "myapp.desktop" in str(path)
        True
    """
    if user_scope:
        return get_user_applications_dir() / filename
    else:
        # Use first system directory
        system_dirs = get_system_applications_dirs()
        if system_dirs:
            return system_dirs[0] / filename
        else:
            # Fallback to /usr/share/applications
            return Path("/usr/share/applications") / filename


def check_file_exists(path: Path) -> bool:
    """
    Check if file exists.

    Args:
        path: File path

    Returns:
        True if file exists

    Example:
        >>> check_file_exists(Path("/etc/passwd"))
        True
    """
    return path.exists()


def check_write_permission(path: Path) -> bool:
    """
    Check if we have write permission to directory.

    Args:
        path: Directory path

    Returns:
        True if writable

    Example:
        >>> check_write_permission(Path.home())
        True
    """
    try:
        return os.access(path, os.W_OK)
    except Exception:
        return False


def save_desktop_file(
    content: str, filename: str, user_scope: bool = True
) -> Tuple[bool, Optional[str], Optional[Path]]:
    """
    Save desktop file to appropriate location.

    Args:
        content: Desktop file content
        filename: Desktop file name
        user_scope: If True, save to user directory; if False, system

    Returns:
        Tuple of (success, error_message, file_path)

    Example:
        >>> success, error, path = save_desktop_file(
        ...     "[Desktop Entry]\\nName=Test",
        ...     "test.desktop"
        ... )
        >>> success
        True
    """
    target_path = get_desktop_file_path(filename, user_scope)
    target_dir = target_path.parent

    # Ensure directory exists
    success, error = ensure_directory_exists(target_dir)
    if not success:
        return False, error, None

    # Check write permission
    if not check_write_permission(target_dir):
        return False, f"No write permission to {target_dir}", None

    try:
        with open(target_path, "w") as f:
            f.write(content)
        return True, None, target_path
    except PermissionError:
        return False, f"Permission denied writing to {target_path}", None
    except Exception as e:
        return False, f"Failed to write file: {str(e)}", None


def get_appimage_exec_command(appimage_path: str) -> str:
    """
    Generate Exec command for AppImage.

    Args:
        appimage_path: Path to AppImage file

    Returns:
        Exec command string

    Example:
        >>> cmd = get_appimage_exec_command("/home/user/app.AppImage")
        >>> "/home/user/app.AppImage" in cmd
        True
    """
    # Make sure path is absolute
    path = Path(appimage_path).resolve()

    # AppImage files should be executable
    # Exec format: /path/to/app.AppImage %F (for file handling)
    return str(path)


def extract_appimage_name(appimage_path: str) -> str:
    """
    Extract application name from AppImage filename.

    Args:
        appimage_path: Path to AppImage file

    Returns:
        Application name

    Example:
        >>> extract_appimage_name("/path/to/MyApp-1.0.AppImage")
        'MyApp'
    """
    filename = Path(appimage_path).stem  # Remove .AppImage extension

    # Remove version numbers and common suffixes
    # e.g., "MyApp-1.0" -> "MyApp"
    name = filename.split("-")[0]

    return name


def list_existing_desktop_files(user_scope: bool = True) -> List[str]:
    """
    List existing desktop files.

    Args:
        user_scope: If True, list user files; if False, system files

    Returns:
        List of desktop file names

    Example:
        >>> files = list_existing_desktop_files()
        >>> isinstance(files, list)
        True
    """
    if user_scope:
        app_dir = get_user_applications_dir()
    else:
        system_dirs = get_system_applications_dirs()
        if not system_dirs:
            return []
        app_dir = system_dirs[0]

    if not app_dir.exists():
        return []

    return [f.name for f in app_dir.glob("*.desktop")]


def delete_desktop_file(
    filename: str, user_scope: bool = True
) -> Tuple[bool, Optional[str]]:
    """
    Delete a desktop file.

    Args:
        filename: Desktop file name
        user_scope: If True, delete from user directory

    Returns:
        Tuple of (success, error_message)

    Example:
        >>> success, error = delete_desktop_file("test.desktop")
        >>> success
        True
    """
    target_path = get_desktop_file_path(filename, user_scope)

    if not target_path.exists():
        return False, f"File not found: {target_path}"

    try:
        target_path.unlink()
        return True, None
    except PermissionError:
        return False, f"Permission denied: {target_path}"
    except Exception as e:
        return False, f"Failed to delete file: {str(e)}"
