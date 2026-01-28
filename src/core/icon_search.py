"""
Icon search functionality using multiple sources.

Multi-source approach:
1. SimpleIcons (curated brand icons)
2. Iconify API (large curated icon collection)
3. DuckDuckGo (web search with intelligent queries)

All results are scored and ranked by relevance and quality.
"""

import requests
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    from ddgs import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS = None
    DDGS_AVAILABLE = False


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
    def is_square(self) -> bool:
        """Check if the image is square or nearly square (good for icons)."""
        if self.width <= 0 or self.height <= 0:
            # Unknown dimensions, assume it might be square
            return True

        aspect_ratio = self.width / self.height
        # Allow 10% variance (0.9 to 1.1 ratio)
        return 0.9 <= aspect_ratio <= 1.1

    def calculate_current_score(self) -> int:
        """
        Calculate score indicating this is likely the current/official icon.

        Returns:
            Score (higher = more likely current/official)
        """
        score = 0
        title_lower = self.title.lower()
        url_lower = self.image_url.lower()

        # Source-based scoring (curated sources get highest priority)
        if self.source == "github":
            # Base GitHub score
            score += 600  # Official repo icons are most authoritative
            
            # Extra points for file-specific GitHub results
            if "official repo" in title_lower or "primary" in title_lower:
                score += 150  # Boost for file-specific search results
                
        elif self.source == "simpleicons":
            score += 550  # SimpleIcons is well-maintained and current
        elif self.source == "iconify":
            score += 500  # Iconify is curated but may have older variants

        # Positive signals (current/official)
        if "official" in title_lower:
            score += 100
        if "primary" in title_lower:
            score += 80
        if any(year in title_lower for year in ["2024", "2025", "2026"]):
            score += 100
        if "current" in title_lower:
            score += 50
        if "brand" in title_lower:
            score += 50
        if self.width >= 1024 and self.height >= 1024:
            score += 30  # High-res suggests newer
        elif self.width >= 512 and self.height >= 512:
            score += 20

        # Negative signals (old/legacy)
        if "old" in title_lower:
            score -= 100
        if "legacy" in title_lower:
            score -= 100
        if "vintage" in title_lower:
            score -= 50
        if "history" in title_lower or "historical" in title_lower:
            score -= 50
        if "retro" in title_lower:
            score -= 50
        if self.width > 0 and self.width < 256:
            score -= 20  # Low-res suggests older

        return score

    @property
    def file_type(self) -> str:
        """
        Get file type/extension from URL.

        Returns:
            File extension in uppercase (e.g., "PNG", "SVG", "JPG")
        """
        url_lower = self.image_url.lower()

        # Check for common image extensions
        if ".svg" in url_lower or url_lower.endswith("svg"):
            return "SVG"
        elif ".png" in url_lower or url_lower.endswith("png"):
            return "PNG"
        elif ".jpg" in url_lower or ".jpeg" in url_lower:
            return "JPG"
        elif ".webp" in url_lower:
            return "WEBP"
        elif ".gif" in url_lower:
            return "GIF"
        else:
            return "IMG"  # Unknown/generic image

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

            # Download image with proper headers
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            }
            response = requests.get(
                self.image_url, timeout=10, stream=True, headers=headers
            )
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


def search_iconify(app_name: str, limit: int = 5) -> List[IconResult]:
    """
    Search Iconify API for official icons.

    Iconify has curated, current icons for 200k+ apps/brands.

    Args:
        app_name: Application name (e.g., "firefox", "chrome")
        limit: Maximum number of results

    Returns:
        List of IconResult objects from Iconify
    """
    if not app_name or not app_name.strip():
        return []

    try:
        # Normalize app name for search
        search_term = app_name.strip().lower().replace(" ", "-")

        # Search Iconify collections
        # Try multiple common icon sets
        icon_sets = [
            "logos",  # Brand logos (most likely)
            "simple-icons",  # Simple brand icons
            "mdi",  # Material Design Icons
            "fa",  # Font Awesome
        ]

        results = []

        for icon_set in icon_sets:
            try:
                # Search API endpoint
                api_url = f"https://api.iconify.design/search?query={search_term}&prefix={icon_set}&limit=5"
                response = requests.get(api_url, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    icons = data.get("icons", [])

                    for icon_name in icons[:limit]:
                        # Get SVG URL - Iconify uses format: prefix:icon-name
                        # Example: logos:firefox
                        svg_url = f"https://api.iconify.design/{icon_name}.svg"

                        # Create IconResult
                        results.append(
                            IconResult(
                                title=f"{icon_name.replace('-', ' ').replace(':', ': ').title()} (Official)",
                                image_url=svg_url,
                                thumbnail_url=svg_url,
                                source="iconify",
                                width=512,  # SVG, scalable
                                height=512,
                            )
                        )

                        if len(results) >= limit:
                            break

            except Exception:
                # Continue to next icon set if this one fails
                continue

            if len(results) >= limit:
                break

        return results

    except Exception:
        # Iconify search failed, return empty
        return []


def search_simple_icons(app_name: str, limit: int = 3) -> List[IconResult]:
    """
    Search SimpleIcons.org for brand icons.

    SimpleIcons has 3000+ brand SVG icons, always up-to-date.

    Args:
        app_name: Application name (e.g., "firefox", "chrome")
        limit: Maximum number of results

    Returns:
        List of IconResult objects from SimpleIcons
    """
    if not app_name or not app_name.strip():
        return []

    try:
        # SimpleIcons uses slug format (lowercase, no spaces)
        search_slug = app_name.strip().lower().replace(" ", "").replace("-", "")

        # SimpleIcons CDN endpoint
        # They use jsDelivr CDN for hosting
        results = []

        # Try common variations of the app name
        variations = [
            search_slug,
            search_slug.replace("vs", "visualstudio") if "vs" in search_slug else None,
            search_slug.replace("code", "") if "code" in search_slug else None,
        ]

        for slug in variations:
            if not slug or len(results) >= limit:
                break

            try:
                # SimpleIcons CDN URL pattern
                svg_url = f"https://cdn.simpleicons.org/{slug}"

                # Test if icon exists (HEAD request)
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.head(svg_url, timeout=3, headers=headers)

                if response.status_code == 200:
                    results.append(
                        IconResult(
                            title=f"{slug.title()} (SimpleIcons)",
                            image_url=svg_url,
                            thumbnail_url=svg_url,
                            source="simpleicons",
                            width=512,
                            height=512,
                        )
                    )
            except Exception:
                continue

        return results

    except Exception:
        return []











def search_images_duckduckgo(query: str, limit: int = 15) -> List[IconResult]:
    """
    Search for images using DuckDuckGo with improved queries.

    Tries multiple queries to find current, official icons.

    Args:
        query: Search query (app name, description, etc.)
        limit: Maximum number of results to return

    Returns:
        List of IconResult objects, scored and sorted by relevance
    """
    if not query or not query.strip():
        return []

    if not DDGS_AVAILABLE:
        print("Warning: ddgs module not available, icon search disabled")
        return []

    try:
        # Try multiple search strategies
        queries = [
            f"{query.strip()} official logo",  # Emphasize official
            f"{query.strip()} logo 2024",  # Emphasize recency
            f"{query.strip()} brand icon",  # Brand = current
            f"{query.strip()} icon",  # Fallback generic
        ]

        all_results = []
        seen_urls = set()
        ddgs = DDGS()

        # Search with each query
        for search_query in queries:
            try:
                search_results = ddgs.images(search_query, max_results=limit * 2)

                for result in search_results:
                    image_url = result.get("image", "")

                    # Skip duplicates
                    if image_url in seen_urls:
                        continue
                    seen_urls.add(image_url)

                    # Extract image data
                    title = result.get("title", "Unknown")
                    thumbnail_url = result.get("thumbnail", image_url)
                    width = result.get("width", 0)
                    height = result.get("height", 0)

                    if image_url:
                        all_results.append(
                            IconResult(
                                title=title,
                                image_url=image_url,
                                thumbnail_url=thumbnail_url,
                                source="duckduckgo",
                                width=width,
                                height=height,
                            )
                        )
            except Exception:
                # Continue to next query if this one fails
                continue

        # Filter for square images only
        square_results = [r for r in all_results if r.is_square]

        # Sort by "current" score (higher = more likely to be current/official)
        square_results.sort(key=lambda r: r.calculate_current_score(), reverse=True)

        # Return top results
        return square_results[:limit]

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
    include_github: bool = False,  # Disabled GitHub functionality
) -> List[IconResult]:
    """
    Search for icons using multi-source hybrid approach.

    Strategy:
    1. SimpleIcons (curated brand icons)
    2. Iconify API (large curated collection)
    3. DuckDuckGo (fallback with improved queries)
    4. Deduplicate and sort by authority/recency

    Args:
        query: Direct search query (overrides name/exec_path)
        name: Application name (used if query not provided)
        exec_path: Executable path (used if query and name not provided)
        limit: Maximum number of results
        include_github: Include GitHub search (disabled)

    Returns:
        List of IconResult objects, prioritized by source quality and recency
    """
    # Determine search term
    search_term = query or extract_search_term(name, exec_path)

    if not search_term:
        return []

    all_results = []
    seen_urls = set()

    # Phase 1: SimpleIcons (well-maintained brand icons)
    simpleicons_results = search_simple_icons(search_term, limit=5)
    for result in simpleicons_results:
        if result.image_url not in seen_urls:
            all_results.append(result)
            seen_urls.add(result.image_url)

    # Phase 2: Iconify (large curated collection)
    iconify_results = search_iconify(search_term, limit=8)
    for result in iconify_results:
        if result.image_url not in seen_urls:
            all_results.append(result)
            seen_urls.add(result.image_url)

    # Phase 3: DuckDuckGo (fallback with improved queries)
    # Request more results to fill up to limit
    remaining = limit - len(all_results)
    if remaining > 0:
        ddg_limit = max(remaining * 2, 10)  # Get extra to account for filtering
        ddg_results = search_images_duckduckgo(search_term, limit=ddg_limit)

        for result in ddg_results:
            if result.image_url not in seen_urls:
                all_results.append(result)
                seen_urls.add(result.image_url)

    # Phase 4: Sort by source authority and current score
    all_results.sort(key=lambda r: r.calculate_current_score(), reverse=True)

    # Return top results
    return all_results[:limit]
