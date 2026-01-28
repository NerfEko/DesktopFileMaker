"""Tests for validation functions."""

import pytest
from src.core.validation import (
    validate_name,
    validate_exec_path,
    validate_icon_path,
    validate_appimage_path,
    validate_categories,
    validate_mime_types,
    validate_all_fields,
)


class TestValidateName:
    """Test name validation."""

    def test_valid_name(self):
        """Test valid application name."""
        valid, error = validate_name("My App")
        assert valid is True
        assert error is None

    def test_empty_name(self):
        """Test empty name."""
        valid, error = validate_name("")
        assert valid is False
        assert "empty" in error.lower()

    def test_whitespace_only_name(self):
        """Test whitespace-only name."""
        valid, error = validate_name("   ")
        assert valid is False
        assert "empty" in error.lower()

    def test_long_name(self):
        """Test name exceeding length limit."""
        long_name = "A" * 101
        valid, error = validate_name(long_name)
        assert valid is False
        assert "100" in error


class TestValidateExecPath:
    """Test exec path validation."""

    def test_valid_path(self):
        """Test valid executable path."""
        valid, error = validate_exec_path("/usr/bin/python3")
        assert valid is True
        assert error is None

    def test_valid_appimage_path(self):
        """Test valid AppImage path."""
        valid, error = validate_exec_path("/home/user/app.AppImage")
        assert valid is True
        assert error is None

    def test_empty_path(self):
        """Test empty path."""
        valid, error = validate_exec_path("")
        assert valid is False
        assert "empty" in error.lower()

    def test_whitespace_only_path(self):
        """Test whitespace-only path."""
        valid, error = validate_exec_path("   ")
        assert valid is False
        assert "empty" in error.lower()

    def test_very_long_path(self):
        """Test path exceeding length limit."""
        long_path = "/path/" + "a" * 500
        valid, error = validate_exec_path(long_path)
        assert valid is False


class TestValidateIconPath:
    """Test icon path validation."""

    def test_valid_icon_path(self):
        """Test valid icon path."""
        valid, error = validate_icon_path("/usr/share/icons/app.png")
        assert valid is True
        assert error is None

    def test_valid_icon_name(self):
        """Test valid icon name."""
        valid, error = validate_icon_path("application-x-executable")
        assert valid is True
        assert error is None

    def test_none_icon(self):
        """Test None icon (optional)."""
        valid, error = validate_icon_path(None)
        assert valid is True
        assert error is None

    def test_empty_icon(self):
        """Test empty icon (optional)."""
        valid, error = validate_icon_path("")
        assert valid is True
        assert error is None

    def test_very_long_icon_path(self):
        """Test icon path exceeding length limit."""
        long_path = "/path/" + "a" * 500
        valid, error = validate_icon_path(long_path)
        assert valid is False


class TestValidateAppImagePath:
    """Test AppImage path validation."""

    def test_valid_appimage(self):
        """Test valid AppImage path."""
        valid, error = validate_appimage_path("/home/user/app.AppImage")
        assert valid is True
        assert error is None

    def test_valid_appimage_lowercase(self):
        """Test valid AppImage with lowercase extension."""
        valid, error = validate_appimage_path("/home/user/app.appimage")
        assert valid is True
        assert error is None

    def test_invalid_extension(self):
        """Test invalid file extension."""
        valid, error = validate_appimage_path("/home/user/app.zip")
        assert valid is False
        assert "AppImage" in error

    def test_empty_path(self):
        """Test empty path."""
        valid, error = validate_appimage_path("")
        assert valid is False
        assert "empty" in error.lower()

    def test_no_extension(self):
        """Test file without extension."""
        valid, error = validate_appimage_path("/home/user/app")
        assert valid is False


class TestValidateCategories:
    """Test category validation."""

    def test_valid_categories(self):
        """Test valid categories."""
        valid, error = validate_categories(["Development", "Utility"])
        assert valid is True
        assert error is None

    def test_single_category(self):
        """Test single category."""
        valid, error = validate_categories(["Development"])
        assert valid is True
        assert error is None

    def test_none_categories(self):
        """Test None categories (optional)."""
        valid, error = validate_categories(None)
        assert valid is True
        assert error is None

    def test_empty_categories(self):
        """Test empty categories list (optional)."""
        valid, error = validate_categories([])
        assert valid is True
        assert error is None

    def test_invalid_category(self):
        """Test invalid category."""
        valid, error = validate_categories(["InvalidCategory"])
        assert valid is False
        assert "Invalid category" in error

    def test_mixed_valid_invalid(self):
        """Test mix of valid and invalid categories."""
        valid, error = validate_categories(["Development", "InvalidCategory"])
        assert valid is False

    def test_not_a_list(self):
        """Test non-list input."""
        valid, error = validate_categories("Development")
        assert valid is False
        assert "list" in error.lower()


class TestValidateMimeTypes:
    """Test MIME type validation."""

    def test_valid_mime_types(self):
        """Test valid MIME types."""
        valid, error = validate_mime_types(["text/plain", "text/html"])
        assert valid is True
        assert error is None

    def test_single_mime_type(self):
        """Test single MIME type."""
        valid, error = validate_mime_types(["application/json"])
        assert valid is True
        assert error is None

    def test_none_mime_types(self):
        """Test None MIME types (optional)."""
        valid, error = validate_mime_types(None)
        assert valid is True
        assert error is None

    def test_empty_mime_types(self):
        """Test empty MIME types list (optional)."""
        valid, error = validate_mime_types([])
        assert valid is True
        assert error is None

    def test_invalid_mime_type_format(self):
        """Test invalid MIME type format."""
        valid, error = validate_mime_types(["invalid"])
        assert valid is False
        assert "Invalid MIME type" in error

    def test_mime_type_with_plus(self):
        """Test MIME type with plus sign."""
        valid, error = validate_mime_types(["application/vnd.api+json"])
        assert valid is True
        assert error is None

    def test_mime_type_with_dash(self):
        """Test MIME type with dash."""
        valid, error = validate_mime_types(["application/x-python"])
        assert valid is True
        assert error is None

    def test_not_a_list(self):
        """Test non-list input."""
        valid, error = validate_mime_types("text/plain")
        assert valid is False
        assert "list" in error.lower()


class TestValidateAllFields:
    """Test validating all fields together."""

    def test_all_valid(self):
        """Test all fields valid."""
        valid, errors = validate_all_fields(
            name="My App",
            exec_path="/usr/bin/app",
            icon="app-icon",
            categories=["Development"],
            mime_types=["text/plain"],
        )
        assert valid is True
        assert len(errors) == 0

    def test_minimal_valid(self):
        """Test minimal valid fields."""
        valid, errors = validate_all_fields(
            name="My App",
            exec_path="/usr/bin/app",
        )
        assert valid is True
        assert len(errors) == 0

    def test_multiple_errors(self):
        """Test multiple validation errors."""
        valid, errors = validate_all_fields(
            name="",
            exec_path="",
            categories=["InvalidCategory"],
        )
        assert valid is False
        assert len(errors) >= 2

    def test_invalid_name_only(self):
        """Test only name is invalid."""
        valid, errors = validate_all_fields(
            name="",
            exec_path="/usr/bin/app",
        )
        assert valid is False
        assert len(errors) == 1

    def test_invalid_exec_only(self):
        """Test only exec is invalid."""
        valid, errors = validate_all_fields(
            name="My App",
            exec_path="",
        )
        assert valid is False
        assert len(errors) == 1
