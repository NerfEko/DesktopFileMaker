"""
Icon search functionality using Iconify API.

Provides internet-based icon search for desktop file creation.
"""

import requests
from typing import List, Optional, Dict, Any
from pathlib import Path


class IconResult:
    """Represents a single icon search result."""

    def __init__(self, name: str, collection: str, description: str = ""):
        """
        Initialize icon result.

        Args:
            name: Icon name (e.g., "firefox")
            collection: Icon collection (e.g., "mdi", "simple-icons")
            description: Optional description of the icon
        """
        self.name = name
        self.collection = collection
        self.description = description
        self.full_name = f"{collection}:{name}"

    def __repr__(self) -> str:
        """String representation."""
        return f"IconResult({self.full_name})"

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, IconResult):
            return False
        return self.full_name == other.full_name


def search_icons_online(query: str, limit: int = 10) -> List[IconResult]:
    """
    Search for icons using Iconify API.

    Args:
        query: Search query (app name, icon name, etc.)
        limit: Maximum number of results to return

    Returns:
        List of IconResult objects

    Raises:
        requests.RequestException: If API call fails
    """
    if not query or not query.strip():
        return []

    try:
        # Use Iconify API for icon search
        url = "https://api.iconify.design/search"
        params = {"query": query.strip(), "limit": limit}

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        # Parse results
        results = []
        icons = data.get("icons", [])

        for icon_data in icons:
            # icon_data format: "collection:name"
            if ":" in icon_data:
                collection, name = icon_data.split(":", 1)
                results.append(IconResult(name, collection))
            else:
                # Fallback if format is unexpected
                results.append(IconResult(icon_data, "custom"))

        return results[:limit]

    except requests.Timeout:
        return []
    except requests.RequestException:
        return []
    except (ValueError, KeyError):
        # JSON parsing error or missing expected keys
        return []


def search_icons_local(query: str, limit: int = 10) -> List[IconResult]:
    """
    Search for icons in local system icon themes.

    Args:
        query: Search query (icon name)
        limit: Maximum number of results to return

    Returns:
        List of IconResult objects
    """
    if not query or not query.strip():
        return []

    results = []
    icon_theme_dirs = [
        Path.home() / ".local" / "share" / "icons",
        Path("/usr/local/share/icons"),
        Path("/usr/share/icons"),
    ]

    icon_extensions = {".png", ".svg", ".xpm", ".jpg", ".jpeg", ".gif"}
    seen = set()

    for theme_dir in icon_theme_dirs:
        if not theme_dir.exists():
            continue

        try:
            for icon_file in theme_dir.rglob(f"*{query}*"):
                if icon_file.suffix in icon_extensions:
                    icon_name = icon_file.stem
                    if icon_name not in seen:
                        seen.add(icon_name)
                        results.append(IconResult(icon_name, "local"))

                    if len(results) >= limit:
                        return results
        except (PermissionError, OSError):
            # Skip directories we can't read
            continue

    return results[:limit]


def extract_search_term(name: str = "", exec_path: str = "") -> str:
    """
    Extract search term from name or exec path.

    Args:
        name: Application name
        exec_path: Executable path

    Returns:
        Search term to use for icon search
    """
    # Prefer name if available
    if name and name.strip():
        return name.strip()

    # Fall back to exec filename
    if exec_path and exec_path.strip():
        exec_file = Path(exec_path).name
        # Remove common extensions
        for ext in [".sh", ".py", ".bin", ".exe", ".AppImage"]:
            if exec_file.endswith(ext):
                exec_file = exec_file[: -len(ext)]
        return exec_file

    return ""


def search_icons(
    query: str = "",
    name: str = "",
    exec_path: str = "",
    limit: int = 10,
    online_first: bool = True,
) -> List[IconResult]:
    """
    Search for icons from multiple sources.

    Searches online first (Iconify API), then falls back to local system icons.

    Args:
        query: Direct search query (overrides name/exec_path)
        name: Application name (used if query not provided)
        exec_path: Executable path (used if query and name not provided)
        limit: Maximum number of results
        online_first: If True, search online first then local; if False, local first

    Returns:
        List of IconResult objects, combined from all sources
    """
    # Determine search term
    search_term = query or extract_search_term(name, exec_path)

    if not search_term:
        return []

    results = []
    seen = set()

    def add_result(result: IconResult):
        """Add result if not already seen."""
        if result.full_name not in seen:
            seen.add(result.full_name)
            results.append(result)

    # Search online first if requested
    if online_first:
        try:
            online_results = search_icons_online(search_term, limit)
            for result in online_results:
                add_result(result)
        except Exception:
            pass

    # Search local icons
    local_results = search_icons_local(search_term, limit - len(results))
    for result in local_results:
        add_result(result)

    # If we don't have enough results and haven't searched online yet, try now
    if not online_first and len(results) < limit:
        try:
            online_results = search_icons_online(search_term, limit - len(results))
            for result in online_results:
                add_result(result)
        except Exception:
            pass

    return results[:limit]
