"""
Icon selector modal widget for choosing icons from image search results.

Displays search results in a popup with keyboard and mouse navigation.
"""

import subprocess
import tempfile
import time
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Label, OptionList
from textual.widgets.option_list import Option
from textual.screen import ModalScreen
from textual.binding import Binding
from typing import Optional, List
from pathlib import Path
from src.core.icon_search import IconResult


class IconSelectorModal(ModalScreen):
    """Modal screen for selecting an icon from image search results."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
        Binding("enter", "accept", "Accept"),
    ]

    CSS = """
    IconSelectorModal {
        align: center middle;
    }

    #icon-selector-container {
        width: 80;
        height: auto;
        max-height: 35;
        border: solid $accent;
        background: $surface;
    }

    #icon-selector-title {
        dock: top;
        height: 1;
        content-align: center middle;
        background: $boost;
        color: $text;
    }

    #icon-list {
        height: auto;
        max-height: 18;
        margin: 1;
    }
    
    /* Override highlight background to use grey for better color contrast */
    #icon-list > .option-list--option-highlighted {
        background: $panel;
        color: $text;
    }
    
    #icon-list:focus > .option-list--option-highlighted {
        background: grey 50%;
        color: $text;
    }
    
    /* Color coding by source */
    .github-source {
        color: green;
    }
    
    .simpleicons-source {
        color: cyan;
    }
    
    .iconify-source {
        color: dodgerblue;
    }
    
    .duckduckgo-source {
        color: $text;
    }

    #color-key {
        dock: bottom;
        height: 3;
        padding: 1;
        background: $panel;
        color: $text-muted;
        border-top: solid $accent;
    }

    #button-container {
        dock: bottom;
        height: auto;
        padding: 1;
        border-top: solid $accent;
        align: center middle;
    }

    #button-container Horizontal {
        width: auto;
        height: auto;
    }

    #button-container Button {
        margin: 0 1;
        min-width: 12;
    }
    
    #help-btn {
        min-width: 5;
        max-width: 5;
        padding: 0 1;
    }

    #icon-selector-help {
        dock: bottom;
        height: 1;
        content-align: center middle;
        background: $panel;
        color: $text-muted;
    }
    """

    def __init__(self, results: List[IconResult], download_dir: Optional[Path] = None):
        """
        Initialize icon selector.

        Args:
            results: List of IconResult objects to display
            download_dir: Directory to download selected icon to
        """
        super().__init__()
        self.results = results
        self.download_dir = download_dir or Path.home() / ".local" / "share" / "icons"
        self.highlighted_index: Optional[int] = None
        self._last_click_time: float = 0
        self._last_click_index: Optional[int] = None
        self._double_click_threshold: float = 0.5  # 500ms for double-click

    def compose(self) -> ComposeResult:
        """Compose the modal layout."""
        with Container(id="icon-selector-container"):
            yield Label(
                f"Select Icon ({len(self.results)} results)", id="icon-selector-title"
            )

            # Create options for OptionList with color coding
            options = []
            for i, result in enumerate(self.results):
                # Format: title (dimensions file_type)
                label_text = result.display_name
                if result.width and result.height:
                    label_text += (
                        f" ({result.width}x{result.height} {result.file_type})"
                    )
                else:
                    # No dimensions available, just show file type
                    label_text += f" ({result.file_type})"

                # Add color coding based on source
                if result.source == "simpleicons":
                    label_text = f"[cyan]{label_text}[/cyan]"
                elif result.source == "iconify":
                    label_text = f"[dodgerblue]{label_text}[/dodgerblue]"
                # duckduckgo stays default color

                options.append(Option(label_text, id=str(i)))

            yield OptionList(*options, id="icon-list")

            # Color key
            yield Label(
                "[cyan]Cyan[/cyan]: SimpleIcons | "
                "[dodgerblue]Blue[/dodgerblue]: Iconify | "
                "White: DuckDuckGo",
                id="color-key",
                markup=True,
            )

            # Help text
            yield Label(
                "Single-click: Highlight | Double-click: Select | Arrow keys: Navigate",
                id="icon-selector-help",
            )

            # Buttons
            with Container(id="button-container"):
                with Horizontal():
                    yield Button("Preview", id="preview-btn", variant="primary")
                    yield Button("Accept", id="accept-btn", variant="success")
                    yield Button("Cancel", id="cancel-btn", variant="default")
                    yield Button("?", id="help-btn", variant="default")

    def on_mount(self) -> None:
        """Initialize on mount - set first item as highlighted."""
        if self.results:
            self.highlighted_index = 0
            option_list = self.query_one("#icon-list", OptionList)
            option_list.highlighted = 0

    def on_option_list_option_highlighted(
        self, event: OptionList.OptionHighlighted
    ) -> None:
        """Handle single-click or arrow key navigation (highlight only)."""
        try:
            self.highlighted_index = int(event.option.id)
        except (ValueError, AttributeError):
            pass

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """
        Handle option selection - detects double-click vs single-click.

        Single-click: Only highlights (via OptionHighlighted event)
        Double-click: Selects and closes modal
        Enter key: Selects and closes modal
        """
        try:
            index = int(event.option.id)
            current_time = time.time()

            # Check if this is a double-click
            is_double_click = (
                index == self._last_click_index
                and (current_time - self._last_click_time)
                < self._double_click_threshold
            )

            if is_double_click:
                # Double-click detected - select and close
                if 0 <= index < len(self.results):
                    selected_icon = self.results[index]
                    self.dismiss(selected_icon)
            else:
                # Single-click - just update tracking (highlight already handled)
                self._last_click_time = current_time
                self._last_click_index = index
                self.highlighted_index = index

        except (ValueError, AttributeError):
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        button_id = event.button.id

        if button_id == "accept-btn":
            self.action_accept()
        elif button_id == "cancel-btn":
            self.action_cancel()
        elif button_id == "preview-btn":
            self.action_preview()
        elif button_id == "help-btn":
            self.action_help()

    def action_accept(self) -> None:
        """Accept the highlighted icon and close modal."""
        if self.highlighted_index is not None and 0 <= self.highlighted_index < len(
            self.results
        ):
            selected_icon = self.results[self.highlighted_index]
            self.dismiss(selected_icon)
        else:
            self.notify("Please select an icon first", severity="warning")

    def action_preview(self) -> None:
        """Download and preview the highlighted icon in system image viewer."""
        if self.highlighted_index is None:
            self.notify("Please select an icon to preview", severity="warning")
            return

        if self.highlighted_index < 0 or self.highlighted_index >= len(self.results):
            return

        icon = self.results[self.highlighted_index]

        try:
            # Download to temp directory
            self.notify("Downloading preview...", severity="information")
            temp_dir = Path(tempfile.gettempdir())
            preview_path = icon.download_image(temp_dir)

            if not preview_path or not preview_path.exists():
                self.notify("Failed to download preview", severity="error")
                return

            # Open in system image viewer
            try:
                # Try xdg-open (Linux)
                subprocess.Popen(
                    ["xdg-open", str(preview_path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self.notify(
                    f"Opening preview: {icon.display_name}", severity="information"
                )
            except FileNotFoundError:
                # Fallback for other systems
                try:
                    import webbrowser

                    webbrowser.open(preview_path.as_uri())
                    self.notify(
                        f"Opening preview: {icon.display_name}", severity="information"
                    )
                except Exception as e:
                    self.notify(f"Could not open preview: {str(e)}", severity="error")

        except Exception as e:
            self.notify(f"Preview failed: {str(e)}", severity="error")

    def action_cancel(self) -> None:
        """Cancel selection and close modal."""
        self.dismiss(None)

    def action_help(self) -> None:
        """Show help dialog with color key."""
        help_message = (
            "COLOR CODING:\n"
            "• Cyan: SimpleIcons (curated brand icons)\n"
            "• Blue: Iconify (large icon collection)\n"
            "• White: DuckDuckGo (web search results)"
        )
        self.notify(help_message, severity="information", timeout=8)
