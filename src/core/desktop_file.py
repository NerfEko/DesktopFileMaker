"""
Desktop file generation and parsing.

Pure functions for creating and validating .desktop file content.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DesktopFileData:
    """Immutable desktop file data structure."""

    name: str
    exec_path: str
    icon: Optional[str] = None
    comment: Optional[str] = None
    categories: Optional[List[str]] = None
    type_: str = "Application"
    terminal: bool = False
    no_display: bool = False
    hidden: bool = False
    mime_types: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    startup_notify: bool = True

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary representation."""
        return {
            "Name": self.name,
            "Exec": self.exec_path,
            "Icon": self.icon or "",
            "Comment": self.comment or "",
            "Type": self.type_,
            "Terminal": "true" if self.terminal else "false",
            "NoDisplay": "true" if self.no_display else "false",
            "Hidden": "true" if self.hidden else "false",
            "Categories": ";".join(self.categories) if self.categories else "",
            "MimeType": ";".join(self.mime_types) if self.mime_types else "",
            "Keywords": ";".join(self.keywords) if self.keywords else "",
            "StartupNotify": "true" if self.startup_notify else "false",
        }


def generate_desktop_content(data: DesktopFileData) -> str:
    """
    Generate .desktop file content from data.

    Args:
        data: DesktopFileData instance

    Returns:
        Formatted .desktop file content as string

    Example:
        >>> data = DesktopFileData(name="MyApp", exec_path="/path/to/app")
        >>> content = generate_desktop_content(data)
        >>> "[Desktop Entry]" in content
        True
    """
    lines = ["[Desktop Entry]"]

    data_dict = data.to_dict()

    # Add fields in standard order
    field_order = [
        "Type",
        "Version",
        "Name",
        "Comment",
        "Exec",
        "Icon",
        "Terminal",
        "Categories",
        "Keywords",
        "MimeType",
        "NoDisplay",
        "Hidden",
        "StartupNotify",
    ]

    for field in field_order:
        if field in data_dict and data_dict[field]:
            lines.append(f"{field}={data_dict[field]}")

    return "\n".join(lines) + "\n"


def parse_desktop_content(content: str) -> Optional[DesktopFileData]:
    """
    Parse .desktop file content into DesktopFileData.

    Args:
        content: Raw .desktop file content

    Returns:
        DesktopFileData instance or None if invalid
    """
    lines = content.strip().split("\n")

    if not lines or lines[0] != "[Desktop Entry]":
        return None

    data = {}
    for line in lines[1:]:
        if "=" not in line or line.startswith("#"):
            continue

        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()

    # Required fields
    if "Name" not in data or "Exec" not in data:
        return None

    # Parse boolean fields
    terminal = data.get("Terminal", "false").lower() == "true"
    no_display = data.get("NoDisplay", "false").lower() == "true"
    hidden = data.get("Hidden", "false").lower() == "true"
    startup_notify = data.get("StartupNotify", "true").lower() == "true"

    # Parse list fields
    categories = [c.strip() for c in data.get("Categories", "").split(";") if c.strip()]
    mime_types = [m.strip() for m in data.get("MimeType", "").split(";") if m.strip()]
    keywords = [k.strip() for k in data.get("Keywords", "").split(";") if k.strip()]

    return DesktopFileData(
        name=data["Name"],
        exec_path=data["Exec"],
        icon=data.get("Icon"),
        comment=data.get("Comment"),
        categories=categories or None,
        type_=data.get("Type", "Application"),
        terminal=terminal,
        no_display=no_display,
        hidden=hidden,
        mime_types=mime_types or None,
        keywords=keywords or None,
        startup_notify=startup_notify,
    )


def generate_filename(name: str) -> str:
    """
    Generate valid .desktop filename from application name.

    Args:
        name: Application name

    Returns:
        Valid filename (lowercase, spaces to dashes, .desktop extension)

    Example:
        >>> generate_filename("My Cool App")
        'my-cool-app.desktop'
    """
    # Convert to lowercase and replace spaces with dashes
    filename = name.lower().replace(" ", "-")

    # Remove invalid characters
    valid_chars = set("abcdefghijklmnopqrstuvwxyz0123456789-_")
    filename = "".join(c for c in filename if c in valid_chars)

    # Remove leading/trailing dashes
    filename = filename.strip("-")

    return f"{filename}.desktop"
