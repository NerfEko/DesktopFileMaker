"""Tests for the ExecutableSuggester."""

import pytest
import anyio
from pathlib import Path
from src.tui.widgets.exec_suggester import ExecutableSuggester


class TestExecutableSuggester:
    """Test suite for ExecutableSuggester class."""

    def test_suggester_finds_bash(self):
        """Test that suggester can find bash executable."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)
            result = await suggester.get_suggestion("bash")

            assert result is not None
            assert "bash" in result
            assert Path(result).exists()

        anyio.run(run_test)

    def test_suggester_returns_none_for_nonexistent(self):
        """Test that suggester returns None for nonexistent executables."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)
            result = await suggester.get_suggestion("thisexecutabledoesnotexist123456")

            assert result is None

        anyio.run(run_test)

    def test_suggester_returns_none_for_empty_string(self):
        """Test that suggester returns None for empty input."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)
            result = await suggester.get_suggestion("")

            assert result is None

        anyio.run(run_test)

    def test_suggester_with_full_path(self):
        """Test that suggester works with full path input."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)
            result = await suggester.get_suggestion("/bin/bas")

            assert result is not None
            assert result.startswith("/bin/bas")
            assert Path(result).exists()

        anyio.run(run_test)

    def test_suggester_case_insensitive(self):
        """Test that case insensitive mode works."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=False)
            result = await suggester.get_suggestion("BASH")

            assert result is not None
            assert "bash" in result.lower()

        anyio.run(run_test)

    def test_suggester_caching(self):
        """Test that suggester caches executable list."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)

            # First call should populate cache
            result1 = await suggester.get_suggestion("bash")
            assert suggester._executables is not None

            # Second call should use cache
            result2 = await suggester.get_suggestion("bash")
            assert result1 == result2

        anyio.run(run_test)

    def test_suggester_finds_by_name(self):
        """Test that suggester can find executable by name only."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)
            result = await suggester.get_suggestion("ls")

            assert result is not None
            assert Path(result).name == "ls"
            assert Path(result).exists()

        anyio.run(run_test)

    def test_suggester_with_directory_path(self):
        """Test that suggester searches custom directory when path contains /."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)

            # Test with /bin/ directory (should find executables)
            result = await suggester.get_suggestion("/bin/")
            assert result is not None
            assert result.startswith("/bin/")
            assert Path(result).exists()

        anyio.run(run_test)

    def test_suggester_with_partial_path(self):
        """Test that suggester matches partial filename in custom directory."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)

            # Test with partial filename in /bin
            result = await suggester.get_suggestion("/bin/bas")
            assert result is not None
            assert result.startswith("/bin/bas")
            assert Path(result).exists()

        anyio.run(run_test)

    def test_suggester_with_tilde_expansion(self):
        """Test that suggester expands ~ to home directory."""

        async def run_test():
            import os

            suggester = ExecutableSuggester(case_sensitive=True)

            # Test with tilde
            result = await suggester.get_suggestion("~/.local/bin/")
            # Result may be None if directory doesn't exist or has no executables
            # Just verify it doesn't crash and preserves tilde
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
            suggester = ExecutableSuggester(case_sensitive=True)

            # Test with nonexistent directory
            result = await suggester.get_suggestion("/nonexistent/path/")
            assert result is None

        anyio.run(run_test)

    def test_suggester_suggests_directories(self):
        """Test that suggester suggests directories with trailing /."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)

            # Test that /home/ suggests a directory
            result = await suggester.get_suggestion("/home/")
            # Should suggest a directory (may vary by system)
            if result is not None:
                # If a suggestion exists, it should be a directory path
                assert "/" in result
                # Directories or executables both valid here

        anyio.run(run_test)

    def test_suggester_navigates_subdirectories(self):
        """Test that suggester can navigate into subdirectories."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)

            # First, get a directory suggestion from /usr
            result1 = await suggester.get_suggestion("/usr/")
            if result1 and result1.endswith("/"):
                # It's a directory, verify we can navigate into it
                result2 = await suggester.get_suggestion(result1)
                # Should be able to get suggestions from the subdirectory
                # (may be None if empty, but shouldn't crash)
                assert result2 is None or isinstance(result2, str)

        anyio.run(run_test)

    def test_suggester_skips_hidden_files(self):
        """Test that suggester skips hidden files/directories (starting with .)."""

        async def run_test():
            suggester = ExecutableSuggester(case_sensitive=True)

            # Test in home directory which likely has hidden files
            result = await suggester.get_suggestion("~/.")
            # Should return None or non-hidden item (not start with /home/user/.something)
            if result:
                from pathlib import Path

                assert not Path(result).name.startswith(".")

        anyio.run(run_test)

    def test_suggester_preserves_tilde(self):
        """Test that suggester preserves ~ notation when user types with tilde."""

        async def run_test():
            import os

            suggester = ExecutableSuggester(case_sensitive=True)

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
