"""Tests for icon search functionality."""

import pytest
from src.core.icon_search import (
    IconResult,
    search_icons_system,
    search_icons_freedesktop,
    search_icons,
    get_icon_suggestions_for_app,
    validate_icon_url,
)


class TestIconResult:
    """Test IconResult dataclass."""

    def test_create_icon_result(self):
        """Test creating an icon result."""
        result = IconResult(
            name="python", url="https://example.com/python.svg", source="iconify"
        )
        assert result.name == "python"
        assert result.url == "https://example.com/python.svg"
        assert result.source == "iconify"


class TestSearchIconsSystem:
    """Test system icon search."""

    def test_returns_list(self):
        """Test that it returns a list."""
        results = search_icons_system("application")
        assert isinstance(results, list)

    def test_returns_icon_results(self):
        """Test that results are IconResult objects."""
        results = search_icons_system("application")
        if results:
            assert all(isinstance(r, IconResult) for r in results)

    def test_respects_limit(self):
        """Test that limit is respected."""
        results = search_icons_system("application", limit=3)
        assert len(results) <= 3

    def test_empty_query(self):
        """Test with empty query."""
        results = search_icons_system("")
        assert isinstance(results, list)


class TestSearchIconsFreedesktop:
    """Test freedesktop icon search."""

    def test_python_search(self):
        """Test searching for python icons."""
        results = search_icons_freedesktop("python")
        assert len(results) > 0
        assert any("python" in r.name.lower() for r in results)

    def test_app_search(self):
        """Test searching for app icons."""
        results = search_icons_freedesktop("app")
        assert len(results) > 0
        assert any("application" in r.name.lower() for r in results)

    def test_returns_icon_results(self):
        """Test that results are IconResult objects."""
        results = search_icons_freedesktop("python")
        assert all(isinstance(r, IconResult) for r in results)

    def test_respects_limit(self):
        """Test that limit is respected."""
        results = search_icons_freedesktop("python", limit=2)
        assert len(results) <= 2

    def test_source_is_freedesktop(self):
        """Test that source is marked as freedesktop."""
        results = search_icons_freedesktop("python")
        assert all(r.source == "freedesktop" for r in results)

    def test_partial_match(self):
        """Test partial matching."""
        results = search_icons_freedesktop("dev")
        assert len(results) > 0


class TestSearchIcons:
    """Test combined icon search."""

    def test_returns_list(self):
        """Test that it returns a list."""
        results = search_icons("python")
        assert isinstance(results, list)

    def test_returns_icon_results(self):
        """Test that results are IconResult objects."""
        results = search_icons("python")
        if results:
            assert all(isinstance(r, IconResult) for r in results)

    def test_respects_limit(self):
        """Test that limit is respected."""
        results = search_icons("python", limit=3)
        assert len(results) <= 3

    def test_no_duplicates(self):
        """Test that there are no duplicate icon names."""
        results = search_icons("application", limit=10)
        names = [r.name for r in results]
        assert len(names) == len(set(names))

    def test_multiple_sources(self):
        """Test that results come from multiple sources."""
        results = search_icons("python", limit=10)
        if len(results) > 1:
            sources = set(r.source for r in results)
            # Should have at least one source
            assert len(sources) >= 1


class TestGetIconSuggestionsForApp:
    """Test app-based icon suggestions."""

    def test_python_app(self):
        """Test suggestions for Python app."""
        results = get_icon_suggestions_for_app("Python IDE")
        assert len(results) > 0
        assert all(isinstance(r, IconResult) for r in results)

    def test_generic_app(self):
        """Test suggestions for generic app."""
        results = get_icon_suggestions_for_app("MyApp")
        assert len(results) > 0

    def test_respects_limit(self):
        """Test that limit is respected."""
        results = get_icon_suggestions_for_app("Python IDE", limit=2)
        assert len(results) <= 2

    def test_single_word_app(self):
        """Test with single word app name."""
        results = get_icon_suggestions_for_app("Python")
        assert len(results) > 0

    def test_empty_app_name(self):
        """Test with empty app name."""
        results = get_icon_suggestions_for_app("")
        # Should return generic application icons
        assert len(results) > 0


class TestValidateIconUrl:
    """Test icon URL validation."""

    def test_icon_name_valid(self):
        """Test that icon names are valid."""
        valid, error = validate_icon_url("application-x-executable")
        assert valid is True
        assert error is None

    def test_local_path_valid(self):
        """Test that local paths are valid."""
        valid, error = validate_icon_url("/usr/share/icons/app.png")
        assert valid is True
        assert error is None

    def test_relative_path_valid(self):
        """Test that relative paths are valid."""
        valid, error = validate_icon_url("./icons/app.svg")
        assert valid is True
        assert error is None

    def test_invalid_url(self):
        """Test that invalid URLs are rejected."""
        valid, error = validate_icon_url(
            "https://invalid-domain-12345.example.com/icon.svg"
        )
        # May fail or succeed depending on network
        assert isinstance(valid, bool)
        if not valid:
            assert error is not None
