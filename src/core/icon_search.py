"""
Icon search functionality using DuckDuckGo image search.

Provides internet-based image search for finding icons/images for applications.
"""

import requests
import tempfile
from pathlib import Path
from typing import List, Optional
from ddgs import DDGS


class IconResult:
    """Represents a single image search result that can be used as an icon."""

    def __init__(
        self,
        title: str,
        image_url: str,
        thumbnail_url: str,
        source: str = "duckduckgo",
        width: int = 0,
        height: int = 0,
    ):
        """
        Initialize icon result.

        Args:
            title: Image title/description
            image_url: Full resolution image URL
            thumbnail_url: Thumbnail image URL
            source: Source of the image
            width: Image width in pixels
            height: Image height in pixels
        """
        self.title = title
        self.image_url = image_url
        self.thumbnail_url = thumbnail_url
        self.source = source
        self.width = width
        self.height = height
        self.local_path: Optional[Path] = None

    @property
    def display_name(self) -> str:
        """Get display name for the icon."""
        return self.title[:60] + "..." if len(self.title) > 60 else self.title

    @property
    def full_name(self) -> str:
        """Get full name (for backward compatibility with existing code)."""
        # If downloaded, return the local path
        if self.local_path:
            return str(self.local_path)
        # Otherwise return a descriptive name
        return self.title

    def download_image(self, target_dir: Optional[Path] = None) -> Optional[Path]:
        """
        Download the full resolution image to local system.

        Args:
            target_dir: Directory to save the image (defaults to temp directory)

        Returns:
            Path to downloaded image or None if download failed
        """
        try:
            # Use target directory or temp directory
            if target_dir is None:
                target_dir = Path(tempfile.gettempdir())

            # Determine file extension from URL
            ext = ".png"  # default
            if self.image_url:
                url_ext = self.image_url.split("?")[0].split(".")[-1].lower()
                if url_ext in ["jpg", "jpeg", "png", "gif", "svg", "webp"]:
                    ext = f".{url_ext}"

            # Create safe filename from title
            safe_title = "".join(
                c for c in self.title if c.isalnum() or c in " -_"
            ).strip()[:50]
            filename = f"{safe_title}{ext}"

            # Download image
            response = requests.get(self.image_url, timeout=10, stream=True)
            response.raise_for_status()

            # Save to file
            file_path = target_dir / filename
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.local_path = file_path
            return file_path

        except Exception as e:
            # Download failed, return None
            return None

    def __repr__(self) -> str:
        """String representation."""
        return f"IconResult({self.display_name})"

    def __eq__(self, other) -> bool:
        """Check equality."""
        if not isinstance(other, IconResult):
            return False
        return self.image_url == other.image_url


def search_images_duckduckgo(query: str, limit: int = 15) -> List[IconResult]:
    """
    Search for images using DuckDuckGo image search.

    Args:
        query: Search query (app name, description, etc.)
        limit: Maximum number of results to return

    Returns:
        List of IconResult objects
    """
    if not query or not query.strip():
        return []

    try:
        # Use DuckDuckGo image search
        # Add "icon" or "logo" to query for better results
        search_query = f"{query.strip()} icon logo"

        results = []
        ddgs = DDGS()

        # Search for images
        search_results = ddgs.images(search_query, max_results=limit)

        for result in search_results:
            # Extract image data
            title = result.get("title", "Unknown")
            image_url = result.get("image", "")
            thumbnail_url = result.get("thumbnail", image_url)
            width = result.get("width", 0)
            height = result.get("height", 0)

            if image_url:
                results.append(
                    IconResult(
                        title=title,
                        image_url=image_url,
                        thumbnail_url=thumbnail_url,
                        source="duckduckgo",
                        width=width,
                        height=height,
                    )
                )

        return results[:limit]

    except Exception as e:
        # Search failed, return empty list
        return []


def extract_search_term(name: str = "", exec_path: str = "") -> str:
    """
    Extract search term from name or exec path.

    Args:
        name: Application name
        exec_path: Executable path

    Returns:
        Search term to use for image search
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
    limit: int = 15,
) -> List[IconResult]:
    """
    Search for images that can be used as icons.

    Searches DuckDuckGo for images related to the application.

    Args:
        query: Direct search query (overrides name/exec_path)
        name: Application name (used if query not provided)
        exec_path: Executable path (used if query and name not provided)
        limit: Maximum number of results

    Returns:
        List of IconResult objects with image URLs
    """
    # Determine search term
    search_term = query or extract_search_term(name, exec_path)

    if not search_term:
        return []

    # Search DuckDuckGo for images
    results = search_images_duckduckgo(search_term, limit)

    return results
