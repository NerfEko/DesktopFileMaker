"""Main TUI application for desktop file maker."""

import os
import stat
from typing import Optional
from textual.app import ComposeResult, App
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import (
    Header,
    Footer,
    Button,
    Label,
    Select,
    TextArea,
)
from textual.binding import Binding
from src.core import (
    DesktopFileData,
    generate_desktop_content,
    generate_filename,
    validate_all_fields,
    save_desktop_file,
    get_user_applications_dir,
)
from src.core.icon_search import search_icons, IconResult
from src.tui.widgets.icon_selector import IconSelectorModal
from src.tui.widgets.exec_suggester import ExecutableSuggester
from src.tui.widgets.icon_path_suggester import IconPathSuggester
from src.tui.widgets.smart_input import SmartInput


class DesktopFileMakerApp(App):
    """Main application screen for creating desktop files."""

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+s", "save", "Save"),
        Binding("tab", "focus_next", "Next"),
        Binding("shift+tab", "focus_previous", "Previous"),
    ]

    def __init__(self, *args, **kwargs):
        """Initialize the app with pending icon state."""
        super().__init__(*args, **kwargs)
        self._pending_icon: Optional[IconResult] = None

    CSS = """
    Screen {
        layout: vertical;
    }
    
    #header {
        dock: top;
        height: 3;
    }
    
    #footer {
        dock: bottom;
        height: 2;
    }
    
    #main-container {
        height: 1fr;
        border: solid $accent;
    }
    
    .form-group {
        height: auto;
        margin: 1 0;
    }
    
    .form-label {
        width: 20;
        text-align: right;
        margin-right: 1;
    }
    
    SmartInput {
        width: 1fr;
    }
    
    Select {
        width: 1fr;
    }
    
    #preview {
        height: 10;
        border: solid $primary;
        margin-top: 1;
    }
    
    #button-group {
        height: auto;
        margin-top: 1;
    }
    
    Button {
        margin-right: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header(show_clock=True)

        with Container(id="main-container"):
            with Vertical():
                yield Label("Desktop File Maker", id="title")

                # Name field
                with Horizontal(classes="form-group"):
                    yield Label("Name:", classes="form-label")
                    yield SmartInput(id="name-input", placeholder="Application name")

                # Exec field
                with Horizontal(classes="form-group"):
                    yield Label("Exec:", classes="form-label")
                    yield SmartInput(
                        id="exec-input",
                        placeholder="/path/to/executable",
                        suggester=ExecutableSuggester(case_sensitive=True),
                    )

                # Icon field with search button
                with Horizontal(classes="form-group"):
                    yield Label("Icon:", classes="form-label")
                    yield SmartInput(
                        id="icon-input",
                        placeholder="/path/to/icon or select search",
                        suggester=IconPathSuggester(case_sensitive=True),
                    )
                    yield Button("Search", id="search-icon-btn", variant="primary")

                # Comment field
                with Horizontal(classes="form-group"):
                    yield Label("Comment:", classes="form-label")
                    yield SmartInput(id="comment-input", placeholder="Brief description")

                # Categories field
                with Horizontal(classes="form-group"):
                    yield Label("Categories:", classes="form-label")
                    yield SmartInput(
                        id="categories-input", placeholder="Development;Utility"
                    )

                # Terminal checkbox
                with Horizontal(classes="form-group"):
                    yield Label("Terminal:", classes="form-label")
                    yield Select(
                        [("No", False), ("Yes", True)],
                        id="terminal-select",
                        value=False,
                    )

                # Preview section
                yield Label("Preview:", id="preview-label")
                yield TextArea(id="preview", read_only=True)

                # Button group
                with Horizontal(id="button-group"):
                    yield Button(
                        "Generate Preview", id="preview-btn", variant="primary"
                    )
                    yield Button("Save", id="save-btn", variant="success")
                    yield Button("Clear", id="clear-btn", variant="warning")
                    yield Button("Quit", id="quit-btn", variant="error")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the application."""
        self.title = "Desktop File Maker"
        self.sub_title = f"Files will be saved to {get_user_applications_dir()}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "preview-btn":
            self.action_preview()
        elif button_id == "save-btn":
            self.action_save()
        elif button_id == "clear-btn":
            self.action_clear()
        elif button_id == "quit-btn":
            self.action_quit()
        elif button_id == "search-icon-btn":
            self.action_search_icons()

    def action_preview(self) -> None:
        """Generate and show preview of desktop file."""
        # Get form values
        name = self.query_one("#name-input", SmartInput).value
        exec_path = self.query_one("#exec-input", SmartInput).value
        icon_field = self.query_one("#icon-input", SmartInput).value or None
        comment = self.query_one("#comment-input", SmartInput).value or None
        categories_str = self.query_one("#categories-input", SmartInput).value
        terminal = self.query_one("#terminal-select", Select).value

        # Handle pending icon for preview
        icon = icon_field
        if self._pending_icon and icon_field and icon_field.startswith("[Selected:"):
            # For preview, show what the icon will be named
            icon = f"{self._pending_icon.title[:50]}.png (will be downloaded)"

        # Parse categories
        categories = [c.strip() for c in categories_str.split(";") if c.strip()] or None

        # Validate
        valid, errors = validate_all_fields(name, exec_path, icon, categories)

        if not valid:
            preview_text = "Validation Errors:\n" + "\n".join(f"• {e}" for e in errors)
        else:
            # Generate preview
            data = DesktopFileData(
                name=name,
                exec_path=exec_path,
                icon=icon,
                comment=comment,
                categories=categories,
                terminal=terminal,
            )
            preview_text = generate_desktop_content(data)

        # Update preview
        preview = self.query_one("#preview", TextArea)
        preview.text = preview_text

    def action_save(self) -> None:
        """Save the desktop file."""
        # Get form values
        name = self.query_one("#name-input", SmartInput).value
        exec_path = self.query_one("#exec-input", SmartInput).value
        icon_field = self.query_one("#icon-input", SmartInput).value or None
        comment = self.query_one("#comment-input", SmartInput).value or None
        categories_str = self.query_one("#categories-input", SmartInput).value
        terminal = self.query_one("#terminal-select", Select).value

        # Handle pending icon download
        icon = icon_field
        if self._pending_icon and icon_field and icon_field.startswith("[Selected:"):
            # Download the pending icon permanently
            self.notify("Downloading icon...", severity="information")

            from pathlib import Path

            download_dir = (
                Path.home()
                / ".local"
                / "share"
                / "icons"
                / "hicolor"
                / "512x512"
                / "apps"
            )
            download_dir.mkdir(parents=True, exist_ok=True)

            downloaded_path = self._pending_icon.download_image(download_dir)

            if downloaded_path:
                icon = str(downloaded_path)
                self.notify(
                    f"Icon downloaded: {downloaded_path.name}", severity="information"
                )
            else:
                self.notify(
                    "Failed to download icon, saving without it", severity="warning"
                )
                icon = None

            # Clear pending icon after download
            self._pending_icon = None

        # Parse categories
        categories = [c.strip() for c in categories_str.split(";") if c.strip()] or None

        # Check if exec_path is an AppImage and make it executable if needed
        if exec_path and exec_path.lower().endswith('.appimage'):
            from pathlib import Path
            
            exec_file = Path(exec_path)
            if exec_file.exists() and not os.access(exec_file, os.X_OK):
                try:
                    # Make AppImage executable (user, group, other)
                    current_mode = exec_file.stat().st_mode
                    exec_file.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                    self.notify(f"Made {exec_file.name} executable", severity="information")
                except (OSError, PermissionError) as e:
                    self.notify(f"Failed to make AppImage executable: {str(e)}", severity="warning")

        # Validate
        valid, errors = validate_all_fields(name, exec_path, icon, categories)

        if not valid:
            self.notify(f"Validation failed: {errors[0]}", severity="error")
            return

        # Generate desktop file
        data = DesktopFileData(
            name=name,
            exec_path=exec_path,
            icon=icon,
            comment=comment,
            categories=categories,
            terminal=terminal,
        )

        content = generate_desktop_content(data)
        filename = generate_filename(name)

        # Save file
        success, error, path = save_desktop_file(content, filename, user_scope=True)

        if success:
            self.notify(f"Saved to {path}", severity="information")
            self.action_clear()
        else:
            self.notify(f"Save failed: {error}", severity="error")

    def action_clear(self) -> None:
        """Clear all form fields."""
        self.query_one("#name-input", SmartInput).value = ""
        self.query_one("#exec-input", SmartInput).value = ""
        self.query_one("#icon-input", SmartInput).value = ""
        self.query_one("#comment-input", SmartInput).value = ""
        self.query_one("#categories-input", SmartInput).value = ""
        self.query_one("#terminal-select", Select).value = False
        self.query_one("#preview", TextArea).text = ""

        # Clear pending icon download
        self._pending_icon = None

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_search_icons(self) -> None:
        """Search for icons and show selection modal."""
        # Get search terms from form
        name = self.query_one("#name-input", SmartInput).value
        exec_path = self.query_one("#exec-input", SmartInput).value

        # Check if we have something to search for
        if not name.strip() and not exec_path.strip():
            self.notify(
                "Enter an app name or executable path to search for icons",
                severity="warning",
            )
            return

        # Show searching notification
        self.notify(f"Searching for icons...", severity="information")

        # Search for icons (images) with timeout protection
        try:
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Search timed out")
            
            # Set a 10 second timeout for the entire search
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(10)
            
            try:
                results = search_icons(name=name, exec_path=exec_path, limit=40)
            finally:
                signal.alarm(0)  # Cancel the timeout

            if not results:
                # This should rarely happen since we're searching the internet
                self.notify(
                    f"No images found for '{name or exec_path}'",
                    severity="warning",
                )
                return

            # Show selection modal
            def on_icon_selected(icon: Optional[IconResult]) -> None:
                """Handle icon selection from modal."""
                if icon:
                    # Store the icon result for later download when saving
                    self._pending_icon = icon

                    # Show icon info in the Icon field (not a file path yet)
                    self.query_one(
                        "#icon-input", SmartInput
                    ).value = f"[Selected: {icon.display_name}]"

                    self.notify(
                        f"Icon selected: {icon.display_name} (will download when saved)",
                        severity="information",
                    )

            self.app.push_screen(IconSelectorModal(results), on_icon_selected)

        except TimeoutError:
            self.notify("Search timed out. Try with a simpler search term.", severity="error")
        except Exception as e:
            self.notify(f"Search failed: {str(e)}", severity="error")
