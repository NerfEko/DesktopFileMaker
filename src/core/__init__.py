"""Core desktop file functionality."""

from .desktop_file import (
    DesktopFileData,
    generate_desktop_content,
    parse_desktop_content,
    generate_filename,
)
from .validation import (
    validate_name,
    validate_exec_path,
    validate_icon_path,
    validate_appimage_path,
    validate_categories,
    validate_mime_types,
    validate_all_fields,
)
from .file_system import (
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
    delete_desktop_file,
)
from .icon_handler import (
    find_icon_in_themes,
    validate_icon_file,
    get_icon_suggestions,
    copy_icon_to_user_share,
    get_common_icon_names,
)

__all__ = [
    # desktop_file
    "DesktopFileData",
    "generate_desktop_content",
    "parse_desktop_content",
    "generate_filename",
    # validation
    "validate_name",
    "validate_exec_path",
    "validate_icon_path",
    "validate_appimage_path",
    "validate_categories",
    "validate_mime_types",
    "validate_all_fields",
    # file_system
    "get_user_applications_dir",
    "get_system_applications_dirs",
    "ensure_directory_exists",
    "get_desktop_file_path",
    "check_file_exists",
    "check_write_permission",
    "save_desktop_file",
    "get_appimage_exec_command",
    "extract_appimage_name",
    "list_existing_desktop_files",
    "delete_desktop_file",
    # icon_handler
    "find_icon_in_themes",
    "validate_icon_file",
    "get_icon_suggestions",
    "copy_icon_to_user_share",
    "get_common_icon_names",
]
