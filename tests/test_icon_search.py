"""Tests for icon search functionality."""

import pytest
from unittest.mock import patch, MagicMock
from src.core.icon_search import (
    IconResult,
    search_icons_online,
    search_icons_local,
    extract_search_term,
    search_icons,
)


class TestIconResult:
    """Tests for IconResult class."""

    def test_icon_result_creation(self):
        """Test creating an IconResult."""
        result = IconResult("firefox", "mdi", "Firefox browser")
        assert result.name == "firefox"
        assert result.collection == "mdi"
        assert result.description == "Firefox browser"
        assert result.full_name == "mdi:firefox"

    def test_icon_result_repr(self):
        """Test IconResult string representation."""
        result = IconResult("firefox", "mdi")
        assert repr(result) == "IconResult(mdi:firefox)"

    def test_icon_result_equality(self):
        """Test IconResult equality."""
        result1 = IconResult("firefox", "mdi")
        result2 = IconResult("firefox", "mdi")
        result3 = IconResult("chrome", "mdi")

        assert result1 == result2
        assert result1 != result3

    def test_icon_result_equality_with_non_result(self):
        """Test IconResult equality with non-IconResult object."""
        result = IconResult("firefox", "mdi")
        assert result != "mdi:firefox"
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


class TestSearchIconsOnline:
    """Tests for search_icons_online function."""

    @patch("src.core.icon_search.requests.get")
    def test_search_icons_online_success(self, mock_get):
        """Test successful online icon search."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "icons": ["mdi:firefox", "mdi:firefox-box", "simple-icons:firefox"]
        }
        mock_get.return_value = mock_response

        results = search_icons_online("firefox", limit=5)

        assert len(results) == 3
        assert results[0].full_name == "mdi:firefox"
        assert results[1].full_name == "mdi:firefox-box"
        assert results[2].full_name == "simple-icons:firefox"

    @patch("src.core.icon_search.requests.get")
    def test_search_icons_online_respects_limit(self, mock_get):
        """Test that limit is respected."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"icons": [f"mdi:icon{i}" for i in range(20)]}
        mock_get.return_value = mock_response

        results = search_icons_online("test", limit=5)

        assert len(results) == 5

    @patch("src.core.icon_search.requests.get")
    def test_search_icons_online_empty_query(self, mock_get):
        """Test with empty query."""
        results = search_icons_online("", limit=5)

        assert results == []
        mock_get.assert_not_called()

    @patch("src.core.icon_search.requests.get")
    def test_search_icons_online_timeout(self, mock_get):
        """Test timeout handling."""
        import requests

        mock_get.side_effect = requests.Timeout()

        results = search_icons_online("firefox", limit=5)

        assert results == []

    @patch("src.core.icon_search.requests.get")
    def test_search_icons_online_request_error(self, mock_get):
        """Test request error handling."""
        import requests

        mock_get.side_effect = requests.RequestException()

        results = search_icons_online("firefox", limit=5)

        assert results == []

    @patch("src.core.icon_search.requests.get")
    def test_search_icons_online_json_error(self, mock_get):
        """Test JSON parsing error handling."""
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        results = search_icons_online("firefox", limit=5)

        assert results == []

    @patch("src.core.icon_search.requests.get")
    def test_search_icons_online_missing_icons_key(self, mock_get):
        """Test handling of missing 'icons' key."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        results = search_icons_online("firefox", limit=5)

        assert results == []

    @patch("src.core.icon_search.requests.get")
    def test_search_icons_online_malformed_icon_name(self, mock_get):
        """Test handling of malformed icon names."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "icons": [
                "mdi:firefox",
                "invalid_icon_without_colon",
                "simple-icons:chrome",
            ]
        }
        mock_get.return_value = mock_response

        results = search_icons_online("test", limit=5)

        assert len(results) == 3
        # Malformed icon should have "custom" as collection
        assert results[1].collection == "custom"
        assert results[1].name == "invalid_icon_without_colon"


class TestSearchIconsLocal:
    """Tests for search_icons_local function."""

    def test_search_icons_local_empty_query(self):
        """Test with empty query."""
        results = search_icons_local("", limit=5)
        assert results == []

    def test_search_icons_local_whitespace_query(self):
        """Test with whitespace-only query."""
        results = search_icons_local("   ", limit=5)
        assert results == []

    def test_search_icons_local_returns_list(self):
        """Test that function returns a list."""
        results = search_icons_local("application", limit=5)
        assert isinstance(results, list)

    def test_search_icons_local_respects_limit(self):
        """Test that limit is respected."""
        results = search_icons_local("application", limit=3)
        assert len(results) <= 3

    def test_search_icons_local_returns_icon_results(self):
        """Test that results are IconResult objects."""
        results = search_icons_local("application", limit=5)
        for result in results:
            assert isinstance(result, IconResult)
            assert result.collection == "local"


class TestSearchIcons:
    """Tests for combined search_icons function."""

    @patch("src.core.icon_search.search_icons_online")
    @patch("src.core.icon_search.search_icons_local")
    def test_search_icons_online_first(self, mock_local, mock_online):
        """Test that online search is tried first."""
        mock_online.return_value = [
            IconResult("firefox", "mdi"),
            IconResult("firefox-box", "mdi"),
        ]
        mock_local.return_value = []

        results = search_icons(name="Firefox", online_first=True)

        assert len(results) == 2
        mock_online.assert_called_once()

    @patch("src.core.icon_search.search_icons_online")
    @patch("src.core.icon_search.search_icons_local")
    def test_search_icons_local_first(self, mock_local, mock_online):
        """Test that local search is tried first when online_first=False."""
        mock_local.return_value = [IconResult("firefox", "local")]
        mock_online.return_value = []

        results = search_icons(name="Firefox", online_first=False)

        assert len(results) == 1
        mock_local.assert_called_once()

    @patch("src.core.icon_search.search_icons_online")
    @patch("src.core.icon_search.search_icons_local")
    def test_search_icons_combines_results(self, mock_local, mock_online):
        """Test that results from both sources are combined."""
        mock_online.return_value = [IconResult("firefox", "mdi")]
        mock_local.return_value = [IconResult("firefox", "local")]

        results = search_icons(name="Firefox")

        assert len(results) == 2

    @patch("src.core.icon_search.search_icons_online")
    @patch("src.core.icon_search.search_icons_local")
    def test_search_icons_deduplicates(self, mock_local, mock_online):
        """Test that duplicate results are removed."""
        mock_online.return_value = [IconResult("firefox", "mdi")]
        mock_local.return_value = [IconResult("firefox", "mdi")]

        results = search_icons(name="Firefox")

        assert len(results) == 1

    @patch("src.core.icon_search.search_icons_online")
    @patch("src.core.icon_search.search_icons_local")
    def test_search_icons_respects_limit(self, mock_local, mock_online):
        """Test that limit is respected."""
        mock_online.return_value = [IconResult(f"icon{i}", "mdi") for i in range(20)]
        mock_local.return_value = []

        results = search_icons(name="test", limit=5)

        assert len(results) == 5

    @patch("src.core.icon_search.search_icons_online")
    @patch("src.core.icon_search.search_icons_local")
    def test_search_icons_empty_query(self, mock_local, mock_online):
        """Test with empty query."""
        results = search_icons(query="", name="", exec_path="")

        assert results == []
        mock_online.assert_not_called()
        mock_local.assert_not_called()

    @patch("src.core.icon_search.search_icons_online")
    @patch("src.core.icon_search.search_icons_local")
    def test_search_icons_uses_direct_query(self, mock_local, mock_online):
        """Test that direct query parameter is used."""
        mock_online.return_value = []
        mock_local.return_value = []

        search_icons(query="custom-query", name="ignored", exec_path="ignored")

        # Check that the search was called with the direct query
        mock_online.assert_called_once()
        call_args = mock_online.call_args
        assert call_args[0][0] == "custom-query"

    @patch("src.core.icon_search.search_icons_online")
    @patch("src.core.icon_search.search_icons_local")
    def test_search_icons_fallback_to_online(self, mock_local, mock_online):
        """Test fallback to online search when local_first=False and local returns nothing."""
        mock_local.return_value = []
        mock_online.return_value = [IconResult("firefox", "mdi")]

        results = search_icons(name="Firefox", online_first=False)

        assert len(results) == 1
        mock_online.assert_called_once()

    @patch("src.core.icon_search.search_icons_online")
    @patch("src.core.icon_search.search_icons_local")
    def test_search_icons_exception_handling(self, mock_local, mock_online):
        """Test that exceptions are handled gracefully."""
        mock_online.side_effect = Exception("API error")
        mock_local.return_value = [IconResult("firefox", "local")]

        results = search_icons(name="Firefox")

        # Should still return local results
        assert len(results) == 1
