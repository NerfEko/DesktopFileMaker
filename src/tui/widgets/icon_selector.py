"""
Icon selector modal widget for choosing icons from search results.

Displays search results in a popup with keyboard and mouse navigation.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Label
from textual.screen import ModalScreen
from textual.binding import Binding
from typing import Optional, List
from src.core.icon_search import IconResult


class IconSelectorModal(ModalScreen):
    """Modal screen for selecting an icon from search results."""

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
        width: 60;
        height: auto;
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
        width: 1fr;
        border: solid $primary;
    }

    .icon-item {
        width: 1fr;
        height: 1;
        padding: 0 1;
    }

    .icon-item.selected {
        background: $accent;
        color: $surface;
    }

    #icon-selector-footer {
        dock: bottom;
        height: 2;
        border-top: solid $accent;
        padding: 1;
    }

    #icon-selector-footer Label {
        margin-right: 2;
    }
    """

    def __init__(self, results: List[IconResult]):
        """
        Initialize icon selector.

        Args:
            results: List of IconResult objects to display
        """
        super().__init__()
        self.results = results
        self.selected_index = 0
        self.selected_icon: Optional[IconResult] = None

    def compose(self) -> ComposeResult:
        """Compose the modal layout."""
        with Container(id="icon-selector-container"):
            yield Label("Select Icon", id="icon-selector-title")

            with Vertical(id="icon-list"):
                for i, result in enumerate(self.results):
                    # Format: "collection:name"
                    label_text = f"{result.full_name}"
                    if result.description:
                        label_text += f" - {result.description}"

                    yield Label(
                        label_text,
                        id=f"icon-item-{i}",
                        classes="icon-item" + (" selected" if i == 0 else ""),
                    )

            with Horizontal(id="icon-selector-footer"):
                yield Label("↑↓ Navigate")
                yield Label("Enter Select")
                yield Label("Esc Cancel")

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

        self.selected_icon = self.results[self.selected_index]

    def action_select_icon(self) -> None:
        """Select the current icon and close modal."""
        if self.selected_icon:
            self.dismiss(self.selected_icon)

    def action_cancel(self) -> None:
        """Cancel selection and close modal."""
        self.dismiss(None)
