"""
Icon search functionality for finding icons online.

Pure functions for searching and retrieving icon suggestions from the web.
"""

import requests
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class IconResult:
    """Icon search result."""

    name: str
    url: str
    source: str  # e.g., "iconify", "flaticon", "system"


def search_icons_iconify(query: str, limit: int = 5) -> List[IconResult]:
    """
    Search for icons using Iconify API.

    Iconify provides free, open-source icons from multiple icon sets.

    Args:
        query: Search query (e.g., "python", "app", "settings")
        limit: Maximum number of results to return

    Returns:
        List of IconResult objects

    Example:
        >>> results = search_icons_iconify("python")
        >>> len(results) > 0
        True
        >>> results[0].name
        'python'
    """
    try:
        # Iconify search API
        url = "https://api.iconify.design/search"
        params = {
            "query": query,
            "limit": limit,
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()
        results = []

        # Parse Iconify results
        if "icons" in data:
            for icon in data["icons"][:limit]:
                icon_name = icon.get("name", query)
                # Iconify CDN URL format
                icon_url = f"https://api.iconify.design/{icon.get('collection', 'mdi')}/{icon_name}.svg"
                results.append(
                    IconResult(name=icon_name, url=icon_url, source="iconify")
                )

        return results
    except Exception as e:
        # Silently fail if API is unavailable
        return []


def search_icons_system(query: str, limit: int = 5) -> List[IconResult]:
    """
    Search for icons in system icon themes.

    Args:
        query: Search query (e.g., "python", "app")
        limit: Maximum number of results to return

    Returns:
        List of IconResult objects from system themes

    Example:
        >>> results = search_icons_system("application")
        >>> isinstance(results, list)
        True
    """
    from pathlib import Path

    results = []
    icon_dirs = [
        Path.home() / ".local" / "share" / "icons",
        Path("/usr/local/share/icons"),
        Path("/usr/share/icons"),
    ]

    found_icons = set()

    for icon_dir in icon_dirs:
        if not icon_dir.exists():
            continue

        # Search for icons matching the query
        for icon_file in icon_dir.rglob(f"*{query}*"):
            if icon_file.suffix in {".png", ".svg", ".xpm"}:
                icon_name = icon_file.stem

                # Avoid duplicates
                if icon_name not in found_icons:
                    found_icons.add(icon_name)
                    results.append(
                        IconResult(name=icon_name, url=str(icon_file), source="system")
                    )

                if len(results) >= limit:
                    return results

    return results


def search_icons_freedesktop(query: str, limit: int = 5) -> List[IconResult]:
    """
    Search for icons using freedesktop.org icon naming spec.

    Returns common icon names that match the query.

    Args:
        query: Search query
        limit: Maximum number of results

    Returns:
        List of IconResult objects with common icon names

    Example:
        >>> results = search_icons_freedesktop("app")
        >>> len(results) > 0
        True
    """
    # Common freedesktop icon names
    common_icons = {
        "python": ["application-x-python", "python", "application-x-executable"],
        "app": ["application-x-executable", "application-x-appimage", "application"],
        "appimage": ["application-x-appimage", "application-x-executable"],
        "executable": ["application-x-executable", "application-x-elf-binary"],
        "script": ["application-x-shellscript", "application-x-python"],
        "java": ["application-x-java", "application-x-jar"],
        "game": ["application-x-executable", "application-x-appimage"],
        "utility": ["application-x-executable", "utilities-terminal"],
        "development": ["application-x-executable", "application-x-python"],
        "settings": ["preferences-system", "preferences-desktop"],
        "terminal": ["utilities-terminal", "application-x-shellscript"],
        "editor": ["text-editor", "accessories-text-editor"],
        "browser": ["web-browser", "firefox", "chromium"],
        "media": ["multimedia-player", "media-player"],
        "image": ["image-viewer", "image-x-generic"],
        "document": ["document", "text-x-generic"],
        "archive": ["application-x-archive", "application-x-compressed-tar"],
    }

    results = []
    query_lower = query.lower()

    # Direct match
    if query_lower in common_icons:
        for icon_name in common_icons[query_lower][:limit]:
            results.append(
                IconResult(
                    name=icon_name,
                    url=icon_name,  # Just the name, will be resolved by system
                    source="freedesktop",
                )
            )
    else:
        # Partial match
        for key, icons in common_icons.items():
            if query_lower in key or key in query_lower:
                for icon_name in icons[:limit]:
                    if len(results) < limit:
                        results.append(
                            IconResult(
                                name=icon_name, url=icon_name, source="freedesktop"
                            )
                        )

    return results[:limit]


def search_icons(query: str, limit: int = 5) -> List[IconResult]:
    """
    Search for icons from multiple sources.

    Searches in order: system icons, freedesktop common icons, then Iconify API.

    Args:
        query: Search query (e.g., "python", "app", "settings")
        limit: Maximum number of results to return

    Returns:
        List of IconResult objects from all sources

    Example:
        >>> results = search_icons("python")
        >>> len(results) > 0
        True
        >>> results[0].source in ["system", "freedesktop", "iconify"]
        True
    """
    all_results = []
    seen_names = set()

    # Search system icons first (fastest)
    system_results = search_icons_system(query, limit)
    for result in system_results:
        if result.name not in seen_names:
            all_results.append(result)
            seen_names.add(result.name)

    # Add freedesktop common icons
    if len(all_results) < limit:
        fd_results = search_icons_freedesktop(query, limit - len(all_results))
        for result in fd_results:
            if result.name not in seen_names:
                all_results.append(result)
                seen_names.add(result.name)

    # Try Iconify API if we still need more results
    if len(all_results) < limit:
        try:
            iconify_results = search_icons_iconify(query, limit - len(all_results))
            for result in iconify_results:
                if result.name not in seen_names:
                    all_results.append(result)
                    seen_names.add(result.name)
        except Exception:
            # Silently fail if API is unavailable
            pass

    return all_results[:limit]


def get_icon_suggestions_for_app(app_name: str, limit: int = 5) -> List[IconResult]:
    """
    Get icon suggestions for an application name.

    Intelligently searches for icons based on the application name.

    Args:
        app_name: Application name (e.g., "MyApp", "Python IDE")
        limit: Maximum number of results

    Returns:
        List of IconResult objects

    Example:
        >>> results = get_icon_suggestions_for_app("Python IDE")
        >>> len(results) > 0
        True
    """
    # Extract keywords from app name
    keywords = app_name.lower().split()

    # Try each keyword
    for keyword in keywords:
        if len(keyword) > 2:  # Skip very short words
            results = search_icons(keyword, limit)
            if results:
                return results

    # Fallback to generic application icon
    return search_icons("application", limit)


def validate_icon_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that an icon URL is accessible.

    Args:
        url: Icon URL or local path

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> valid, error = validate_icon_url("application-x-executable")
        >>> valid
        True
    """
    from pathlib import Path

    # Local paths are always valid (will be resolved by system)
    if not url.startswith("http"):
        return True, None

    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return True, None
        else:
            return False, f"Icon URL returned status {response.status_code}"
    except requests.RequestException as e:
        return False, f"Failed to access icon URL: {str(e)}"
    except Exception as e:
        return False, f"Error validating icon: {str(e)}"
