"""Tests for file system operations."""

import pytest
import tempfile
from pathlib import Path
from src.core.file_system import (
    get_user_applications_dir,
    get_system_applications_dirs,
    ensure_directory_exists,
    get_desktop_file_path,
    check_file_exists,
    check_write_permission,
    save_desktop_file,
    get_appimage_exec_command,
    extract_appimage_name,
    list_existing_desktop_files,
)


class TestGetUserApplicationsDir:
    """Test getting user applications directory."""

    def test_returns_path(self):
        """Test that it returns a Path object."""
        result = get_user_applications_dir()
        assert isinstance(result, Path)

    def test_contains_applications(self):
        """Test that path contains 'applications'."""
        result = get_user_applications_dir()
        assert "applications" in str(result)

    def test_contains_local_share(self):
        """Test that path contains '.local/share'."""
        result = get_user_applications_dir()
        assert ".local" in str(result)
        assert "share" in str(result)


class TestGetSystemApplicationsDirs:
    """Test getting system applications directories."""

    def test_returns_list(self):
        """Test that it returns a list."""
        result = get_system_applications_dirs()
        assert isinstance(result, list)

    def test_contains_paths(self):
        """Test that list contains Path objects."""
        result = get_system_applications_dirs()
        if result:  # May be empty in some environments
            assert all(isinstance(p, Path) for p in result)

    def test_contains_applications(self):
        """Test that paths contain 'applications'."""
        result = get_system_applications_dirs()
        if result:
            assert any("applications" in str(p) for p in result)


class TestEnsureDirectoryExists:
    """Test directory creation."""

    def test_create_new_directory(self):
        """Test creating a new directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test" / "nested" / "dir"
            success, error = ensure_directory_exists(test_dir)

            assert success is True
            assert error is None
            assert test_dir.exists()

    def test_existing_directory(self):
        """Test with existing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir)
            success, error = ensure_directory_exists(test_dir)

            assert success is True
            assert error is None

    def test_permission_denied(self):
        """Test permission denied scenario."""
        # This test might not work in all environments
        # Skip if running as root
        import os

        if os.geteuid() == 0:
            pytest.skip("Running as root")

        # Try to create in a directory we don't have permission to
        test_dir = Path("/root/test_dir_no_permission")
        success, error = ensure_directory_exists(test_dir)

        # Should fail due to permissions
        assert success is False
        assert error is not None


class TestGetDesktopFilePath:
    """Test getting desktop file path."""

    def test_user_scope_path(self):
        """Test getting user-scoped path."""
        path = get_desktop_file_path("test.desktop", user_scope=True)
        assert "test.desktop" in str(path)
        assert ".local" in str(path)

    def test_system_scope_path(self):
        """Test getting system-scoped path."""
        path = get_desktop_file_path("test.desktop", user_scope=False)
        assert "test.desktop" in str(path)

    def test_filename_preserved(self):
        """Test that filename is preserved."""
        filename = "myapp.desktop"
        path = get_desktop_file_path(filename)
        assert path.name == filename


class TestCheckFileExists:
    """Test file existence checking."""

    def test_existing_file(self):
        """Test checking existing file."""
        with tempfile.NamedTemporaryFile() as tmp:
            result = check_file_exists(Path(tmp.name))
            assert result is True

    def test_nonexistent_file(self):
        """Test checking nonexistent file."""
        result = check_file_exists(Path("/nonexistent/file.txt"))
        assert result is False


class TestCheckWritePermission:
    """Test write permission checking."""

    def test_writable_directory(self):
        """Test checking writable directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = check_write_permission(Path(tmpdir))
            assert result is True

    def test_home_directory(self):
        """Test home directory is writable."""
        result = check_write_permission(Path.home())
        assert result is True

    def test_nonexistent_directory(self):
        """Test nonexistent directory."""
        result = check_write_permission(Path("/nonexistent/dir"))
        assert result is False


class TestSaveDesktopFile:
    """Test saving desktop files."""

    def test_save_to_temp_directory(self):
        """Test saving desktop file to temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock the get_desktop_file_path to use temp directory
            import src.core.file_system as fs_module

            original_func = fs_module.get_desktop_file_path

            def mock_get_path(filename, user_scope=True):
                return Path(tmpdir) / filename

            fs_module.get_desktop_file_path = mock_get_path

            try:
                content = "[Desktop Entry]\nName=Test\nExec=/usr/bin/test\n"
                success, error, path = save_desktop_file(content, "test.desktop")

                assert success is True
                assert error is None
                assert path is not None
                assert path.exists()

                # Verify content
                with open(path) as f:
                    saved_content = f.read()
                assert saved_content == content
            finally:
                fs_module.get_desktop_file_path = original_func

    def test_save_creates_directory(self):
        """Test that save creates necessary directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            import src.core.file_system as fs_module

            original_func = fs_module.get_desktop_file_path

            def mock_get_path(filename, user_scope=True):
                return Path(tmpdir) / "nested" / "dir" / filename

            fs_module.get_desktop_file_path = mock_get_path

            try:
                content = "[Desktop Entry]\nName=Test\nExec=/usr/bin/test\n"
                success, error, path = save_desktop_file(content, "test.desktop")

                assert success is True
                assert path is not None
                assert path.parent.exists()
            finally:
                fs_module.get_desktop_file_path = original_func


class TestGetAppImageExecCommand:
    """Test AppImage exec command generation."""

    def test_simple_path(self):
        """Test generating exec command for simple path."""
        cmd = get_appimage_exec_command("/home/user/app.AppImage")
        assert "/home/user/app.AppImage" in cmd

    def test_relative_path_converted_to_absolute(self):
        """Test that relative paths are converted to absolute."""
        cmd = get_appimage_exec_command("./app.AppImage")
        # Should be converted to absolute path
        assert "/" in cmd
        assert "app.AppImage" in cmd


class TestExtractAppImageName:
    """Test extracting name from AppImage filename."""

    def test_simple_name(self):
        """Test extracting simple name."""
        name = extract_appimage_name("/path/to/MyApp.AppImage")
        assert name == "MyApp"

    def test_name_with_version(self):
        """Test extracting name with version."""
        name = extract_appimage_name("/path/to/MyApp-1.0.AppImage")
        assert name == "MyApp"

    def test_name_with_multiple_dashes(self):
        """Test extracting name with multiple dashes."""
        name = extract_appimage_name("/path/to/My-Cool-App-1.0.AppImage")
        assert name == "My"

    def test_just_filename(self):
        """Test with just filename."""
        name = extract_appimage_name("MyApp.AppImage")
        assert name == "MyApp"


class TestListExistingDesktopFiles:
    """Test listing existing desktop files."""

    def test_returns_list(self):
        """Test that it returns a list."""
        result = list_existing_desktop_files()
        assert isinstance(result, list)

    def test_returns_strings(self):
        """Test that list contains strings."""
        result = list_existing_desktop_files()
        if result:
            assert all(isinstance(f, str) for f in result)

    def test_all_desktop_extension(self):
        """Test that all returned files have .desktop extension."""
        result = list_existing_desktop_files()
        if result:
            assert all(f.endswith(".desktop") for f in result)
