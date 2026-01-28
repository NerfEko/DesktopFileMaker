"""Tests for icon search functionality."""

import pytest
from unittest.mock import patch, MagicMock
from src.core.icon_search import (
    IconResult,
    search_images_duckduckgo,
    extract_search_term,
    search_icons,
)


class TestIconResult:
    """Tests for IconResult class."""

    def test_icon_result_creation(self):
        """Test creating an IconResult."""
        result = IconResult(
            title="Firefox Icon",
            image_url="https://example.com/firefox.png",
            thumbnail_url="https://example.com/firefox_thumb.png",
            source="duckduckgo",
            width=512,
            height=512,
        )
        assert result.title == "Firefox Icon"
        assert result.image_url == "https://example.com/firefox.png"
        assert result.thumbnail_url == "https://example.com/firefox_thumb.png"
        assert result.source == "duckduckgo"
        assert result.width == 512
        assert result.height == 512

    def test_icon_result_display_name(self):
        """Test display name property."""
        result = IconResult(
            title="A very long title that should be truncated to sixty characters max",
            image_url="https://example.com/image.png",
            thumbnail_url="https://example.com/thumb.png",
        )
        assert len(result.display_name) <= 63  # 60 chars + "..."
        assert result.display_name.endswith("...")

    def test_icon_result_display_name_short(self):
        """Test display name with short title."""
        result = IconResult(
            title="Short",
            image_url="https://example.com/image.png",
            thumbnail_url="https://example.com/thumb.png",
        )
        assert result.display_name == "Short"

    def test_icon_result_repr(self):
        """Test IconResult string representation."""
        result = IconResult(
            title="Firefox",
            image_url="https://example.com/firefox.png",
            thumbnail_url="https://example.com/thumb.png",
        )
        assert "Firefox" in repr(result)

    def test_icon_result_equality(self):
        """Test IconResult equality."""
        result1 = IconResult(
            title="Firefox",
            image_url="https://example.com/firefox.png",
            thumbnail_url="https://example.com/thumb.png",
        )
        result2 = IconResult(
            title="Firefox",
            image_url="https://example.com/firefox.png",
            thumbnail_url="https://example.com/thumb.png",
        )
        result3 = IconResult(
            title="Chrome",
            image_url="https://example.com/chrome.png",
            thumbnail_url="https://example.com/thumb.png",
        )

        assert result1 == result2
        assert result1 != result3

    def test_icon_result_equality_with_non_result(self):
        """Test IconResult equality with non-IconResult object."""
        result = IconResult(
            title="Firefox",
            image_url="https://example.com/firefox.png",
            thumbnail_url="https://example.com/thumb.png",
        )
        assert result != "firefox"
        assert result != None


class TestExtractSearchTerm:
    """Tests for extract_search_term function."""

    def test_extract_from_name(self):
        """Test extracting search term from name."""
        term = extract_search_term(name="Firefox")
        assert term == "Firefox"

    def test_extract_from_exec_path(self):
        """Test extracting search term from exec path."""
        term = extract_search_term(exec_path="/usr/bin/firefox")
        assert term == "firefox"

    def test_extract_from_exec_with_extension(self):
        """Test extracting search term from exec with extension."""
        term = extract_search_term(exec_path="/usr/bin/script.sh")
        assert term == "script"

    def test_extract_appimage(self):
        """Test extracting search term from AppImage."""
        term = extract_search_term(exec_path="/home/user/MyApp.AppImage")
        assert term == "MyApp"

    def test_prefer_name_over_exec(self):
        """Test that name is preferred over exec."""
        term = extract_search_term(name="Firefox", exec_path="/usr/bin/firefox")
        assert term == "Firefox"

    def test_empty_inputs(self):
        """Test with empty inputs."""
        term = extract_search_term(name="", exec_path="")
        assert term == ""

    def test_whitespace_only(self):
        """Test with whitespace-only inputs."""
        term = extract_search_term(name="   ", exec_path="   ")
        assert term == ""


class TestSearchImagesDuckDuckGo:
    """Tests for search_images_duckduckgo function."""

    @patch("src.core.icon_search.DDGS")
    def test_search_images_success(self, mock_ddgs_class):
        """Test successful image search."""
        mock_ddgs = MagicMock()
        mock_ddgs.images.return_value = [
            {
                "title": "Firefox Icon",
                "image": "https://example.com/firefox.png",
                "thumbnail": "https://example.com/firefox_thumb.png",
                "width": 512,
                "height": 512,
            },
            {
                "title": "Firefox Logo",
                "image": "https://example.com/firefox2.png",
                "thumbnail": "https://example.com/firefox2_thumb.png",
                "width": 256,
                "height": 256,
            },
        ]
        mock_ddgs_class.return_value = mock_ddgs

        results = search_images_duckduckgo("firefox", limit=5)

        assert len(results) == 2
        assert results[0].title == "Firefox Icon"
        assert results[0].image_url == "https://example.com/firefox.png"
        assert results[1].title == "Firefox Logo"

    @patch("src.core.icon_search.DDGS")
    def test_search_images_respects_limit(self, mock_ddgs_class):
        """Test that limit is respected."""
        mock_ddgs = MagicMock()
        mock_ddgs.images.return_value = [
            {
                "title": f"Icon {i}",
                "image": f"https://example.com/{i}.png",
                "thumbnail": f"https://example.com/{i}_thumb.png",
            }
            for i in range(20)
        ]
        mock_ddgs_class.return_value = mock_ddgs

        results = search_images_duckduckgo("test", limit=5)

        assert len(results) == 5

    def test_search_images_empty_query(self):
        """Test with empty query."""
        results = search_images_duckduckgo("", limit=5)
        assert results == []

    @patch("src.core.icon_search.DDGS")
    def test_search_images_exception(self, mock_ddgs_class):
        """Test exception handling."""
        mock_ddgs_class.side_effect = Exception("Network error")

        results = search_images_duckduckgo("firefox", limit=5)

        assert results == []

    @patch("src.core.icon_search.DDGS")
    def test_search_images_missing_url(self, mock_ddgs_class):
        """Test handling of results without image URL."""
        mock_ddgs = MagicMock()
        mock_ddgs.images.return_value = [
            {"title": "Icon 1", "image": "https://example.com/1.png"},
            {"title": "Icon 2", "image": ""},  # Missing URL
            {"title": "Icon 3", "image": "https://example.com/3.png"},
        ]
        mock_ddgs_class.return_value = mock_ddgs

        results = search_images_duckduckgo("test", limit=5)

        # Should only include results with image URLs
        assert len(results) == 2
        assert results[0].title == "Icon 1"
        assert results[1].title == "Icon 3"


class TestSearchIcons:
    """Tests for combined search_icons function."""

    @patch("src.core.icon_search.search_github_repos")
    @patch("src.core.icon_search.search_simple_icons")
    @patch("src.core.icon_search.search_iconify")
    @patch("src.core.icon_search.search_images_duckduckgo")
    def test_search_icons_with_name(
        self, mock_ddg, mock_iconify, mock_simple, mock_github
    ):
        """Test search with name parameter."""
        mock_github.return_value = []
        mock_simple.return_value = []
        mock_iconify.return_value = []
        mock_ddg.return_value = [
            IconResult(
                "Firefox Icon",
                "https://example.com/firefox.png",
                "https://example.com/thumb.png",
            )
        ]

        results = search_icons(name="Firefox")

        assert len(results) == 1
        # GitHub is disabled by default
        mock_github.assert_not_called()
        mock_simple.assert_called_once_with("Firefox", limit=3)
        mock_iconify.assert_called_once_with("Firefox", limit=5)
        # DDG gets called with calculated remaining limit
        mock_ddg.assert_called_once()

    @patch("src.core.icon_search.search_github_repos")
    @patch("src.core.icon_search.search_simple_icons")
    @patch("src.core.icon_search.search_iconify")
    @patch("src.core.icon_search.search_images_duckduckgo")
    def test_search_icons_with_exec(
        self, mock_ddg, mock_iconify, mock_simple, mock_github
    ):
        """Test search with exec_path parameter."""
        mock_github.return_value = []
        mock_simple.return_value = []
        mock_iconify.return_value = []
        mock_ddg.return_value = [
            IconResult(
                "Firefox Icon",
                "https://example.com/firefox.png",
                "https://example.com/thumb.png",
            )
        ]

        results = search_icons(exec_path="/usr/bin/firefox")

        assert len(results) == 1
        # Should extract "firefox" from path
        mock_github.assert_not_called()
        mock_simple.assert_called_once()
        mock_iconify.assert_called_once()
        mock_ddg.assert_called_once()

    @patch("src.core.icon_search.search_github_repos")
    @patch("src.core.icon_search.search_simple_icons")
    @patch("src.core.icon_search.search_iconify")
    @patch("src.core.icon_search.search_images_duckduckgo")
    def test_search_icons_with_query(
        self, mock_ddg, mock_iconify, mock_simple, mock_github
    ):
        """Test search with direct query parameter."""
        mock_github.return_value = []
        mock_simple.return_value = []
        mock_iconify.return_value = []
        mock_ddg.return_value = []

        search_icons(query="custom search")

        mock_github.assert_not_called()
        mock_simple.assert_called_once_with("custom search", limit=3)
        mock_iconify.assert_called_once_with("custom search", limit=5)
        mock_ddg.assert_called_once()

    @patch("src.core.icon_search.search_github_repos")
    @patch("src.core.icon_search.search_simple_icons")
    @patch("src.core.icon_search.search_iconify")
    @patch("src.core.icon_search.search_images_duckduckgo")
    def test_search_icons_empty_inputs(
        self, mock_ddg, mock_iconify, mock_simple, mock_github
    ):
        """Test with empty inputs."""
        results = search_icons(query="", name="", exec_path="")

        assert results == []
        mock_ddg.assert_not_called()
        mock_iconify.assert_not_called()
        mock_simple.assert_not_called()
        mock_github.assert_not_called()

    @patch("src.core.icon_search.search_github_repos")
    @patch("src.core.icon_search.search_simple_icons")
    @patch("src.core.icon_search.search_iconify")
    @patch("src.core.icon_search.search_images_duckduckgo")
    def test_search_icons_respects_limit(
        self, mock_ddg, mock_iconify, mock_simple, mock_github
    ):
        """Test that limit parameter is passed through."""
        mock_github.return_value = []
        mock_simple.return_value = []
        mock_iconify.return_value = []
        mock_ddg.return_value = []

        search_icons(name="firefox", limit=10)

        mock_github.assert_not_called()
        mock_simple.assert_called_once_with("firefox", limit=3)
        mock_iconify.assert_called_once_with("firefox", limit=5)
        # DDG gets called with remaining limit
        mock_ddg.assert_called_once()


class TestIconDownload:
    """Tests for icon download functionality."""

    @patch("src.core.icon_search.requests.get")
    def test_download_image_success(self, mock_get, tmp_path):
        """Test successful image download."""
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b"image data"]
        mock_get.return_value = mock_response

        result = IconResult(
            "Firefox Icon",
            "https://example.com/firefox.png",
            "https://example.com/thumb.png",
        )

        downloaded = result.download_image(tmp_path)

        assert downloaded is not None
        assert downloaded.exists()
        assert "Firefox Icon" in downloaded.name

    @patch("src.core.icon_search.requests.get")
    def test_download_image_failure(self, mock_get, tmp_path):
        """Test failed image download."""
        mock_get.side_effect = Exception("Network error")

        result = IconResult(
            "Firefox Icon",
            "https://example.com/firefox.png",
            "https://example.com/thumb.png",
        )

        downloaded = result.download_image(tmp_path)

        assert downloaded is None

    @patch("src.core.icon_search.requests.get")
    def test_download_image_sets_local_path(self, mock_get, tmp_path):
        """Test that download sets local_path attribute."""
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b"image data"]
        mock_get.return_value = mock_response

        result = IconResult(
            "Firefox Icon",
            "https://example.com/firefox.png",
            "https://example.com/thumb.png",
        )

        assert result.local_path is None

        downloaded = result.download_image(tmp_path)

        assert result.local_path == downloaded
        assert result.full_name == str(downloaded)
