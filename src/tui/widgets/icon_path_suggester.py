"""
Icon path suggester for autocomplete in the Icon field.

Provides autocomplete suggestions based on image files in directories.
"""

import os
from pathlib import Path
from typing import List, Optional, Set
from textual.suggester import Suggester


class IconPathSuggester(Suggester):
    """Suggester that provides autocomplete for icon/image file paths."""

    # Common image file extensions for icons
    IMAGE_EXTENSIONS = {
        ".png",
        ".svg",
        ".jpg",
        ".jpeg",
        ".ico",
        ".xpm",
        ".webp",
        ".gif",
        ".bmp",
    }

    def __init__(self, *, case_sensitive: bool = True):
        """
        Initialize the icon path suggester.

        Args:
            case_sensitive: Whether suggestions are case sensitive.
        """
        super().__init__(use_cache=True, case_sensitive=case_sensitive)
        self._icon_files: Optional[List[str]] = None

    def _get_common_icon_paths(self) -> List[Path]:
        """
        Get list of common icon directories to search.

        Returns:
            List of Path objects for common icon directories.
        """
        paths = [
            Path("/usr/share/icons"),
            Path("/usr/share/pixmaps"),
            Path(os.path.expanduser("~/.local/share/icons")),
            Path(os.path.expanduser("~/.icons")),
            Path("/usr/local/share/icons"),
        ]

        return [p for p in paths if p.exists()]

    def _is_image_file(self, path: Path) -> bool:
        """
        Check if a file is an image file based on extension.

        Args:
            path: Path to check.

        Returns:
            True if file has an image extension.
        """
        return path.suffix.lower() in self.IMAGE_EXTENSIONS

    def _scan_icon_files(self) -> List[str]:
        """
        Scan common icon paths for image files.

        Returns:
            Sorted list of icon file paths.
        """
        icon_files = set()
        paths = self._get_common_icon_paths()

        for path in paths:
            try:
                # Only scan top-level files, not recursive
                # (icon directories can be huge)
                for item in path.iterdir():
                    if item.is_file() and self._is_image_file(item):
                        icon_files.add(str(item))
                    elif item.is_symlink():
                        try:
                            target = item.resolve()
                            if target.is_file() and self._is_image_file(item):
                                icon_files.add(str(item))
                        except (OSError, RuntimeError):
                            pass
            except (PermissionError, OSError):
                continue

        return sorted(icon_files)

    def _get_icon_files(self) -> List[str]:
        """
        Get cached list of icon files or scan if not cached.

        Returns:
            List of icon file paths.
        """
        if self._icon_files is None:
            self._icon_files = self._scan_icon_files()
        return self._icon_files

    def _search_directory_for_images(
        self, directory: Path, prefix: str = ""
    ) -> List[str]:
        """
        Search a specific directory for image files and subdirectories.

        Args:
            directory: Directory to search.
            prefix: Optional prefix to filter items by name.

        Returns:
            List of paths (directories with trailing /, images without) matching the prefix.
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
                # Add image files
                elif item.is_file() and self._is_image_file(item):
                    items.append(str(item))
                elif item.is_symlink():
                    # Follow symlinks to check type
                    try:
                        target = item.resolve()
                        if target.is_dir():
                            items.append(str(item) + "/")
                        elif target.is_file() and self._is_image_file(item):
                            items.append(str(item))
                    except (OSError, RuntimeError):
                        pass
        except (PermissionError, OSError):
            return []

        return sorted(items)

    async def get_suggestion(self, value: str) -> Optional[str]:
        """
        Get autocomplete suggestion for the given input value.

        Supports two modes:
        1. Path-based: If value contains '/', searches that specific directory
           for subdirectories (with trailing /) and image files
        2. Name-based: Searches common icon paths for image files by name

        Args:
            value: Current value in the input field.

        Returns:
            Suggested completion or None if no match found.
            Directories are returned with trailing '/'.
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
                # Suggest first image in that directory
                directory = value_path
                prefix = ""
            else:
                # User is typing a filename in a directory
                # Suggest images matching the partial filename
                directory = value_path.parent
                prefix = value_path.name

            # Expand ~ to home directory for searching
            expanded_directory = Path(os.path.expanduser(str(directory)))

            # Search the specific directory
            items = self._search_directory_for_images(expanded_directory, prefix)

            if items:
                result = items[0]

                # If user typed with ~, convert result back to ~ notation
                if uses_tilde:
                    home = str(Path.home())
                    if result.startswith(home):
                        result = "~" + result[len(home) :]

                return result

            return None

        # Name-based suggestion (original behavior)
        # Get list of icon files from common paths
        icon_files = self._get_icon_files()

        # Find first icon file that starts with the input value
        search_value = value if self.case_sensitive else value.lower()

        for icon_path in icon_files:
            icon_compare = icon_path if self.case_sensitive else icon_path.lower()

            # Check if icon path starts with input
            if icon_compare.startswith(search_value):
                return icon_path

            # Also check if just the icon name matches
            icon_name = Path(icon_path).name
            icon_name_compare = icon_name if self.case_sensitive else icon_name.lower()
            if icon_name_compare.startswith(search_value):
                return icon_path

        return None
