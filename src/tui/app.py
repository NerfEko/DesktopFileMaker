"""Main TUI application for desktop file maker."""

from typing import Optional
from textual.app import ComposeResult, App
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import (
    Header,
    Footer,
    Button,
    Static,
    Label,
    Input,
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


class DesktopFileMakerApp(App):
    """Main application screen for creating desktop files."""

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+s", "save", "Save"),
        Binding("tab", "focus_next", "Next"),
        Binding("shift+tab", "focus_previous", "Previous"),
    ]

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
    
    Input {
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
                    yield Input(id="name-input", placeholder="Application name")

                # Exec field
                with Horizontal(classes="form-group"):
                    yield Label("Exec:", classes="form-label")
                    yield Input(id="exec-input", placeholder="/path/to/executable")

                # Icon field with search button
                with Horizontal(classes="form-group"):
                    yield Label("Icon:", classes="form-label")
                    yield Input(id="icon-input", placeholder="Icon name or path")
                    yield Button("Search", id="search-icon-btn", variant="primary")

                # Comment field
                with Horizontal(classes="form-group"):
                    yield Label("Comment:", classes="form-label")
                    yield Input(id="comment-input", placeholder="Brief description")

                # Categories field
                with Horizontal(classes="form-group"):
                    yield Label("Categories:", classes="form-label")
                    yield Input(
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
        name = self.query_one("#name-input", Input).value
        exec_path = self.query_one("#exec-input", Input).value
        icon = self.query_one("#icon-input", Input).value or None
        comment = self.query_one("#comment-input", Input).value or None
        categories_str = self.query_one("#categories-input", Input).value
        terminal = self.query_one("#terminal-select", Select).value

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
        name = self.query_one("#name-input", Input).value
        exec_path = self.query_one("#exec-input", Input).value
        icon = self.query_one("#icon-input", Input).value or None
        comment = self.query_one("#comment-input", Input).value or None
        categories_str = self.query_one("#categories-input", Input).value
        terminal = self.query_one("#terminal-select", Select).value

        # Parse categories
        categories = [c.strip() for c in categories_str.split(";") if c.strip()] or None

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
        self.query_one("#name-input", Input).value = ""
        self.query_one("#exec-input", Input).value = ""
        self.query_one("#icon-input", Input).value = ""
        self.query_one("#comment-input", Input).value = ""
        self.query_one("#categories-input", Input).value = ""
        self.query_one("#terminal-select", Select).value = False
        self.query_one("#preview", TextArea).text = ""

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_search_icons(self) -> None:
        """Search for icons and show selection modal."""
        # Get search terms from form
        name = self.query_one("#name-input", Input).value
        exec_path = self.query_one("#exec-input", Input).value

        # Check if we have something to search for
        if not name.strip() and not exec_path.strip():
            self.notify(
                "Enter an app name or executable path to search for icons",
                severity="warning",
            )
            return

        # Show searching notification
        self.notify(f"Searching for icons...", severity="information")

        # Search for icons (images)
        try:
            results = search_icons(name=name, exec_path=exec_path, limit=20)

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
                    self.notify("Downloading image...", severity="information")

                    # Download the image
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

                    downloaded_path = icon.download_image(download_dir)

                    if downloaded_path:
                        # Set the Icon field to the downloaded file path
                        self.query_one("#icon-input", Input).value = str(
                            downloaded_path
                        )
                        self.notify(
                            f"Icon downloaded: {downloaded_path.name}",
                            severity="information",
                        )
                    else:
                        self.notify("Failed to download image", severity="error")

            self.app.push_screen(IconSelectorModal(results), on_icon_selected)

        except Exception as e:
            self.notify(f"Search failed: {str(e)}", severity="error")
