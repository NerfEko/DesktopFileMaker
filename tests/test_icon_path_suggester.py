"""Tests for the IconPathSuggester."""

import pytest
import anyio
from pathlib import Path
from src.tui.widgets.icon_path_suggester import IconPathSuggester


class TestIconPathSuggester:
    """Test suite for IconPathSuggester class."""

    def test_suggester_finds_icons_by_name(self):
        """Test that suggester can find icon files by name."""

        async def run_test():
            suggester = IconPathSuggester(case_sensitive=True)
            result = await suggester.get_suggestion("arch")

            # Should find an arch-related icon in /usr/share/pixmaps
            if result:
                assert "arch" in result.lower()
                assert any(
                    result.endswith(ext)
                    for ext in [".png", ".svg", ".jpg", ".ico", ".xpm"]
                )

        anyio.run(run_test)

    def test_suggester_returns_none_for_nonexistent(self):
        """Test that suggester returns None for nonexistent icons."""

        async def run_test():
            suggester = IconPathSuggester(case_sensitive=True)
            result = await suggester.get_suggestion("thisiconfiledoesnotexist123456789")

            assert result is None

        anyio.run(run_test)

    def test_suggester_returns_none_for_empty_string(self):
        """Test that suggester returns None for empty input."""

        async def run_test():
            suggester = IconPathSuggester(case_sensitive=True)
            result = await suggester.get_suggestion("")

            assert result is None

        anyio.run(run_test)

    def test_suggester_with_directory_path(self):
        """Test that suggester searches custom directory when path contains /."""

        async def run_test():
            suggester = IconPathSuggester(case_sensitive=True)

            # Test with /usr/share/pixmaps/ directory
            result = await suggester.get_suggestion("/usr/share/pixmaps/")
            # Should find image files or directories
            if result:
                # Should be a file or directory and have arrow
                assert "/" in result
                assert result.endswith(" 🠊")

        anyio.run(run_test)

    def test_suggester_with_partial_path(self):
        """Test that suggester matches partial filename in custom directory."""

        async def run_test():
            suggester = IconPathSuggester(case_sensitive=True)

            # Test with partial filename in /usr/share/pixmaps
            result = await suggester.get_suggestion("/usr/share/pixmaps/arch")
            if result:
                assert result.startswith("/usr/share/pixmaps/arch")
                # Should be an image file
                assert any(
                    result.endswith(ext)
                    for ext in [".png", ".svg", ".jpg", ".ico", ".xpm", "/"]
                )

        anyio.run(run_test)

    def test_suggester_with_tilde_expansion(self):
        """Test that suggester expands ~ to home directory."""

        async def run_test():
            import os

            suggester = IconPathSuggester(case_sensitive=True)

            # Test with tilde
            result = await suggester.get_suggestion("~/")
            # Result may suggest directory or icon file
            if result is not None:
                # Result should start with ~ (preserved notation)
                assert result.startswith("~/")
                # Expand to check actual path exists
                expanded = Path(os.path.expanduser(result))
                assert expanded.exists()

        anyio.run(run_test)

    def test_suggester_with_nonexistent_directory(self):
        """Test that suggester handles nonexistent directories gracefully."""

        async def run_test():
            suggester = IconPathSuggester(case_sensitive=True)

            # Test with nonexistent directory
            result = await suggester.get_suggestion("/nonexistent/path/")
            assert result is None

        anyio.run(run_test)

    def test_suggester_suggests_directories(self):
        """Test that suggester suggests directories with trailing /."""

        async def run_test():
            suggester = IconPathSuggester(case_sensitive=True)

            # Test in user home directory (likely has subdirectories)
            result = await suggester.get_suggestion("~/")
            # Should suggest a directory or file
            if result is not None:
                assert "/" in result

        anyio.run(run_test)

    def test_suggester_filters_image_extensions(self):
        """Test that suggester only suggests image files, not other files."""

        async def run_test():
            suggester = IconPathSuggester(case_sensitive=True)

            # Test in a system directory
            result = await suggester.get_suggestion("/usr/share/pixmaps/")
            if result and not result.endswith("/"):
                # Should be an image file
                path = Path(result)
                assert path.suffix.lower() in IconPathSuggester.IMAGE_EXTENSIONS

        anyio.run(run_test)

    def test_suggester_preserves_tilde(self):
        """Test that suggester preserves ~ notation when user types with tilde."""

        async def run_test():
            import os

            suggester = IconPathSuggester(case_sensitive=True)

            # Test that tilde input returns tilde output
            result = await suggester.get_suggestion("~/D")
            if result:
                assert result.startswith("~/"), f"Expected ~/... but got {result}"
                # Verify the expanded path exists
                expanded = Path(os.path.expanduser(result))
                assert expanded.exists()

            # Test that full path input returns full path output
            home = str(Path.home())
            result = await suggester.get_suggestion(f"{home}/D")
            if result:
                assert result.startswith(home), f"Expected {home}/... but got {result}"
                assert not result.startswith("~/"), "Should not convert to tilde"

        anyio.run(run_test)

    def test_suggester_skips_hidden_files(self):
        """Test that suggester skips hidden files/directories (starting with .)."""

        async def run_test():
            suggester = IconPathSuggester(case_sensitive=True)

            # Test in home directory which likely has hidden files
            result = await suggester.get_suggestion("~/.")
            # Should return None or non-hidden item
            if result:
                assert not Path(result).name.startswith(".")

        anyio.run(run_test)
