"""
Executable path suggester for autocomplete in the Exec field.

Provides autocomplete suggestions based on executable files in common system paths.
"""

import os
from pathlib import Path
from typing import List, Optional
from textual.suggester import Suggester


class ExecutableSuggester(Suggester):
    """Suggester that provides autocomplete for executable file paths."""

    def __init__(self, *, case_sensitive: bool = True):
        """
        Initialize the executable suggester.

        Args:
            case_sensitive: Whether suggestions are case sensitive.
        """
        super().__init__(use_cache=True, case_sensitive=case_sensitive)
        self._executables: Optional[List[str]] = None

    def _get_common_paths(self) -> List[Path]:
        """
        Get list of common executable paths to search.

        Returns:
            List of Path objects for common executable directories.
        """
        paths = [
            Path("/usr/bin"),
            Path("/usr/local/bin"),
            Path("/bin"),
            Path("/usr/games"),
            Path(os.path.expanduser("~/.local/bin")),
            Path("/opt"),
            Path("/snap/bin"),
            Path("/var/lib/flatpak/exports/bin"),
            Path(os.path.expanduser("~/.local/share/flatpak/exports/bin")),
        ]

        # Add /opt/*/bin directories
        opt_path = Path("/opt")
        if opt_path.exists():
            for subdir in opt_path.iterdir():
                if subdir.is_dir():
                    bin_dir = subdir / "bin"
                    if bin_dir.exists():
                        paths.append(bin_dir)

        return [p for p in paths if p.exists()]

    def _scan_executables(self) -> List[str]:
        """
        Scan common paths for executable files and AppImage files.
        AppImage files are included regardless of executable status.

        Returns:
            Sorted list of executable file paths.
        """
        executables = set()
        paths = self._get_common_paths()

        for path in paths:
            try:
                for item in path.iterdir():
                    if item.is_file() and (os.access(item, os.X_OK) or item.name.lower().endswith('.appimage')):
                        executables.add(str(item))
                    elif item.is_symlink():
                        # Follow symlinks to check if target is executable or AppImage
                        try:
                            target = item.resolve()
                            if target.is_file() and (os.access(target, os.X_OK) or target.name.lower().endswith('.appimage')):
                                executables.add(str(item))
                        except (OSError, RuntimeError):
                            # Broken symlink or circular reference
                            pass
            except (PermissionError, OSError):
                # Skip directories we can't read
                continue

        return sorted(executables)

    @staticmethod
    def is_appimage(file_path: str) -> bool:
        """
        Check if a file is an AppImage.

        Args:
            file_path: Path to the file to check.

        Returns:
            True if the file is an AppImage, False otherwise.
        """
        return file_path.lower().endswith('.appimage')

    def _get_executables(self) -> List[str]:
        """
        Get cached list of executables or scan if not cached.

        Returns:
            List of executable paths.
        """
        if self._executables is None:
            self._executables = self._scan_executables()
        return self._executables

    def _search_directory_for_executables(
        self, directory: Path, prefix: str = ""
    ) -> List[str]:
        """
        Search a specific directory for executable files and subdirectories.
        Also includes .appimage files regardless of executable status.

        Args:
            directory: Directory to search.
            prefix: Optional prefix to filter items by name.

        Returns:
            List of paths (directories with trailing /, executables without) matching the prefix.
        """
        if not directory.exists() or not directory.is_dir():
            return []

        items = []
        try:
            for item in directory.iterdir():
                # Skip hidden files/directories (starting with .)
                if item.name.startswith("."):
                    continue

                # Check if name matches prefix
                if prefix and not item.name.startswith(prefix):
                    continue

                # Add directories with trailing /
                if item.is_dir():
                    items.append(str(item) + "/")
                # Add executable files or AppImage files (regardless of executable status)
                elif item.is_file() and (os.access(item, os.X_OK) or item.name.lower().endswith('.appimage')):
                    items.append(str(item))
                elif item.is_symlink():
                    # Follow symlinks to check type
                    try:
                        target = item.resolve()
                        if target.is_dir():
                            items.append(str(item) + "/")
                        elif target.is_file() and (os.access(target, os.X_OK) or target.name.lower().endswith('.appimage')):
                            items.append(str(item))
                    except (OSError, RuntimeError):
                        # Broken symlink or circular reference
                        pass
        except (PermissionError, OSError):
            # Can't read directory
            return []

        return sorted(items)

    async def get_suggestion(self, value: str) -> Optional[str]:
        """
        Get autocomplete suggestion for the given input value.

        Supports two modes:
        1. Path-based: If value contains '/', searches that specific directory
           for subdirectories (with trailing /) and executable files
        2. Name-based: Searches common system paths for executable by name

        Args:
            value: Current value in the input field.

        Returns:
            Suggested completion with arrow indicator for display.
            The actual completion will be clean (without arrow).
        """
        if not value:
            return None

        # Check if user is typing a path (contains '/')
        if "/" in value:
            # Path-based suggestion
            # Preserve user's notation (~ vs full path)
            uses_tilde = value.startswith("~/")
            value_path = Path(value)

            # Determine directory and filename prefix
            if value.endswith("/"):
                # User typed a directory path with trailing slash
                # Suggest first executable in that directory
                directory = value_path
                prefix = ""
            else:
                # User is typing a filename in a directory
                # Suggest executables matching the partial filename
                directory = value_path.parent
                prefix = value_path.name

            # Expand ~ to home directory for searching
            expanded_directory = Path(os.path.expanduser(str(directory)))

            # Search the specific directory
            items = self._search_directory_for_executables(expanded_directory, prefix)

            if items:
                result = items[0]

                # If user typed with ~, convert result back to ~ notation
                if uses_tilde:
                    home = str(Path.home())
                    if result.startswith(home):
                        result = "~" + result[len(home) :]

                return result + " 🠊"

            return None

        # Name-based suggestion (original behavior)
        # Get list of executables from common paths
        executables = self._get_executables()

        # Find first executable that starts with the input value
        search_value = value if self.case_sensitive else value.lower()

        for exe_path in executables:
            exe_compare = exe_path if self.case_sensitive else exe_path.lower()

            # Check if executable path starts with input
            if exe_compare.startswith(search_value):
                return exe_path + " 🠊"

            # Also check if just the executable name matches
            exe_name = Path(exe_path).name
            exe_name_compare = exe_name if self.case_sensitive else exe_name.lower()
            if exe_name_compare.startswith(search_value):
                return exe_path + " 🠊"

        return None
