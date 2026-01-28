"""
Icon selector modal widget for choosing icons from image search results.

Displays search results in a popup with keyboard and mouse navigation.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Label
from textual.screen import ModalScreen
from textual.binding import Binding
from typing import Optional, List
from pathlib import Path
from src.core.icon_search import IconResult


class IconSelectorModal(ModalScreen):
    """Modal screen for selecting an icon from image search results."""

    BINDINGS = [
        Binding("up", "select_previous", "Previous"),
        Binding("down", "select_next", "Next"),
        Binding("enter", "select_icon", "Select"),
        Binding("escape", "cancel", "Cancel"),
    ]

    CSS = """
    Screen {
        align: center middle;
    }

    #icon-selector-container {
        width: 70;
        height: auto;
        max-height: 20;
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

    #icon-list-container {
        height: auto;
        max-height: 15;
        overflow-y: scroll;
    }

    #icon-list {
        height: auto;
        width: 1fr;
    }

    .icon-item {
        width: 1fr;
        height: auto;
        padding: 0 1;
    }

    .icon-item.selected {
        background: $accent;
        color: $surface;
    }

    #icon-selector-footer {
        dock: bottom;
        height: 3;
        border-top: solid $accent;
        padding: 1;
    }

    #icon-selector-footer Label {
        margin-right: 2;
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
        self.selected_index = 0
        self.selected_icon: Optional[IconResult] = None

    def compose(self) -> ComposeResult:
        """Compose the modal layout."""
        with Container(id="icon-selector-container"):
            yield Label(
                f"Select Icon ({len(self.results)} results)", id="icon-selector-title"
            )

            with Container(id="icon-list-container"):
                with Vertical(id="icon-list"):
                    for i, result in enumerate(self.results):
                        # Format: title (dimensions)
                        label_text = result.display_name
                        if result.width and result.height:
                            label_text += f" ({result.width}x{result.height})"

                        yield Label(
                            label_text,
                            id=f"icon-item-{i}",
                            classes="icon-item" + (" selected" if i == 0 else ""),
                        )

            with Vertical(id="icon-selector-footer"):
                with Horizontal():
                    yield Label("↑↓ Navigate")
                    yield Label("Enter Select")
                    yield Label("Esc Cancel")
                yield Label("Selected image will be downloaded as icon", markup=False)

    def on_mount(self) -> None:
        """Initialize on mount."""
        if self.results:
            self.selected_icon = self.results[0]

    def action_select_previous(self) -> None:
        """Select previous icon."""
        if not self.results:
            return

        # Deselect current
        current_item = self.query_one(f"#icon-item-{self.selected_index}", Label)
        current_item.remove_class("selected")

        # Move to previous
        self.selected_index = (self.selected_index - 1) % len(self.results)

        # Select new
        new_item = self.query_one(f"#icon-item-{self.selected_index}", Label)
        new_item.add_class("selected")

        # Scroll into view
        new_item.scroll_visible()

        self.selected_icon = self.results[self.selected_index]

    def action_select_next(self) -> None:
        """Select next icon."""
        if not self.results:
            return

        # Deselect current
        current_item = self.query_one(f"#icon-item-{self.selected_index}", Label)
        current_item.remove_class("selected")

        # Move to next
        self.selected_index = (self.selected_index + 1) % len(self.results)

        # Select new
        new_item = self.query_one(f"#icon-item-{self.selected_index}", Label)
        new_item.add_class("selected")

        # Scroll into view
        new_item.scroll_visible()

        self.selected_icon = self.results[self.selected_index]

    def action_select_icon(self) -> None:
        """Select the current icon and close modal."""
        if self.selected_icon:
            # Download the image
            self.dismiss(self.selected_icon)

    def action_cancel(self) -> None:
        """Cancel selection and close modal."""
        self.dismiss(None)
