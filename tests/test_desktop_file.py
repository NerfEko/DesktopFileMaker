"""Tests for desktop file generation and parsing."""

import pytest
from src.core.desktop_file import (
    DesktopFileData,
    generate_desktop_content,
    parse_desktop_content,
    generate_filename,
)


class TestDesktopFileData:
    """Test DesktopFileData dataclass."""

    def test_create_minimal_data(self):
        """Test creating minimal desktop file data."""
        data = DesktopFileData(name="Test App", exec_path="/usr/bin/test")
        assert data.name == "Test App"
        assert data.exec_path == "/usr/bin/test"
        assert data.type_ == "Application"
        assert data.terminal is False

    def test_create_full_data(self):
        """Test creating desktop file data with all fields."""
        data = DesktopFileData(
            name="Test App",
            exec_path="/usr/bin/test",
            icon="test-icon",
            comment="A test application",
            categories=["Development", "Utility"],
            type_="Application",
            terminal=True,
            mime_types=["text/plain"],
            keywords=["test", "app"],
        )
        assert data.name == "Test App"
        assert data.icon == "test-icon"
        assert data.terminal is True
        assert len(data.categories) == 2

    def test_to_dict(self):
        """Test converting to dictionary."""
        data = DesktopFileData(
            name="Test App",
            exec_path="/usr/bin/test",
            icon="test-icon",
            categories=["Development"],
        )
        result = data.to_dict()
        assert result["Name"] == "Test App"
        assert result["Exec"] == "/usr/bin/test"
        assert result["Icon"] == "test-icon"
        assert result["Categories"] == "Development"


class TestGenerateDesktopContent:
    """Test desktop file content generation."""

    def test_generate_minimal_content(self):
        """Test generating minimal desktop file content."""
        data = DesktopFileData(name="Test App", exec_path="/usr/bin/test")
        content = generate_desktop_content(data)

        assert "[Desktop Entry]" in content
        assert "Name=Test App" in content
        assert "Exec=/usr/bin/test" in content
        assert "Type=Application" in content

    def test_generate_full_content(self):
        """Test generating full desktop file content."""
        data = DesktopFileData(
            name="Test App",
            exec_path="/usr/bin/test",
            icon="test-icon",
            comment="A test application",
            categories=["Development", "Utility"],
            terminal=True,
            mime_types=["text/plain", "text/html"],
        )
        content = generate_desktop_content(data)

        assert "[Desktop Entry]" in content
        assert "Name=Test App" in content
        assert "Icon=test-icon" in content
        assert "Comment=A test application" in content
        assert "Categories=Development;Utility" in content
        assert "Terminal=true" in content
        assert "MimeType=text/plain;text/html" in content

    def test_content_format(self):
        """Test that content is properly formatted."""
        data = DesktopFileData(name="Test", exec_path="/usr/bin/test")
        content = generate_desktop_content(data)

        lines = content.strip().split("\n")
        assert lines[0] == "[Desktop Entry]"
        assert all("=" in line for line in lines[1:] if line)
        assert content.endswith("\n")

    def test_boolean_fields_formatting(self):
        """Test boolean fields are formatted correctly."""
        data = DesktopFileData(
            name="Test",
            exec_path="/usr/bin/test",
            terminal=True,
            no_display=False,
            hidden=True,
        )
        content = generate_desktop_content(data)

        assert "Terminal=true" in content
        assert "NoDisplay=false" in content
        assert "Hidden=true" in content


class TestParseDesktopContent:
    """Test desktop file content parsing."""

    def test_parse_minimal_content(self):
        """Test parsing minimal desktop file content."""
        content = "[Desktop Entry]\nName=Test App\nExec=/usr/bin/test\n"
        data = parse_desktop_content(content)

        assert data is not None
        assert data.name == "Test App"
        assert data.exec_path == "/usr/bin/test"

    def test_parse_full_content(self):
        """Test parsing full desktop file content."""
        content = """[Desktop Entry]
Name=Test App
Exec=/usr/bin/test
Icon=test-icon
Comment=A test application
Categories=Development;Utility
Terminal=true
MimeType=text/plain;text/html
"""
        data = parse_desktop_content(content)

        assert data is not None
        assert data.name == "Test App"
        assert data.icon == "test-icon"
        assert data.comment == "A test application"
        assert data.categories == ["Development", "Utility"]
        assert data.terminal is True
        assert data.mime_types == ["text/plain", "text/html"]

    def test_parse_invalid_header(self):
        """Test parsing content with invalid header."""
        content = "[Invalid Header]\nName=Test\nExec=/usr/bin/test\n"
        data = parse_desktop_content(content)
        assert data is None

    def test_parse_missing_required_fields(self):
        """Test parsing content missing required fields."""
        content = "[Desktop Entry]\nName=Test App\n"
        data = parse_desktop_content(content)
        assert data is None

    def test_parse_with_comments(self):
        """Test parsing content with comments."""
        content = """[Desktop Entry]
# This is a comment
Name=Test App
Exec=/usr/bin/test
"""
        data = parse_desktop_content(content)
        assert data is not None
        assert data.name == "Test App"

    def test_parse_boolean_fields(self):
        """Test parsing boolean fields."""
        content = """[Desktop Entry]
Name=Test
Exec=/usr/bin/test
Terminal=true
NoDisplay=false
Hidden=true
"""
        data = parse_desktop_content(content)
        assert data.terminal is True
        assert data.no_display is False
        assert data.hidden is True

    def test_roundtrip_parsing(self):
        """Test that parsing generated content works."""
        original = DesktopFileData(
            name="Test App",
            exec_path="/usr/bin/test",
            icon="test-icon",
            comment="A test application",
            categories=["Development"],
        )

        content = generate_desktop_content(original)
        parsed = parse_desktop_content(content)

        assert parsed is not None
        assert parsed.name == original.name
        assert parsed.exec_path == original.exec_path
        assert parsed.icon == original.icon


class TestGenerateFilename:
    """Test filename generation."""

    def test_simple_name(self):
        """Test generating filename from simple name."""
        filename = generate_filename("MyApp")
        assert filename == "myapp.desktop"

    def test_name_with_spaces(self):
        """Test generating filename from name with spaces."""
        filename = generate_filename("My Cool App")
        assert filename == "my-cool-app.desktop"

    def test_name_with_special_chars(self):
        """Test generating filename from name with special characters."""
        filename = generate_filename("My@App#123")
        assert filename == "myapp123.desktop"

    def test_name_with_dashes(self):
        """Test generating filename from name with dashes."""
        filename = generate_filename("My-Cool-App")
        assert filename == "my-cool-app.desktop"

    def test_name_with_underscores(self):
        """Test generating filename from name with underscores."""
        filename = generate_filename("My_Cool_App")
        assert filename == "my_cool_app.desktop"

    def test_empty_name(self):
        """Test generating filename from empty name."""
        filename = generate_filename("")
        assert filename == ".desktop"

    def test_name_with_leading_trailing_spaces(self):
        """Test generating filename from name with leading/trailing spaces."""
        filename = generate_filename("  MyApp  ")
        assert filename == "myapp.desktop"

    def test_long_name(self):
        """Test generating filename from long name."""
        long_name = "A" * 100
        filename = generate_filename(long_name)
        assert filename.endswith(".desktop")
        assert len(filename) <= 110  # 100 chars + ".desktop"
