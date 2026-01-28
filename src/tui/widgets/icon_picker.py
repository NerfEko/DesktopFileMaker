"""Icon picker widget for selecting icons."""

from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Button, Label, Static, OptionList
from textual.widgets.option_list import Option
from textual.binding import Binding
from src.core.icon_search import (
    search_icons,
    IconResult,
)


class IconPickerWidget(Container):
    """Widget for picking icons with search suggestions."""

    BINDINGS = [
        Binding("escape", "close", "Close"),
    ]

    def __init__(self, app_name: str = "", selected_callback=None):
        """
        Initialize icon picker.

        Args:
            app_name: Application name to search for icons
            selected_callback: Callback function when icon is selected
        """
        super().__init__()
        self.app_name = app_name
        self.selected_callback = selected_callback
        self.selected_icon = None

    def compose(self):
        """Compose the widget."""
        with Vertical():
            yield Label("Select an Icon")
            yield Label(
                f"Suggestions for: {self.app_name or 'Application'}",
                id="icon-search-label",
            )

            # Icon list
            yield OptionList(id="icon-list")

            # Buttons
            with Horizontal(id="icon-picker-buttons"):
                yield Button("Select", id="icon-select-btn", variant="primary")
                yield Button("Search", id="icon-search-btn", variant="default")
                yield Button("Cancel", id="icon-cancel-btn", variant="error")

    def on_mount(self):
        """Load initial icon suggestions."""
        self.load_icon_suggestions(self.app_name)

    def load_icon_suggestions(self, query: str):
        """
        Load icon suggestions for a query.

        Args:
            query: Search query
        """
        # Get suggestions using search_icons function
        if query:
            suggestions = search_icons(name=query, limit=8)
        else:
            suggestions = search_icons(name="application", limit=8)

        # Update list
        icon_list = self.query_one("#icon-list", OptionList)
        icon_list.clear_options()

        for icon in suggestions:
            # Display name with source
            display_name = f"{icon.display_name} ({icon.source})"
            option = Option(display_name, id=icon.display_name)
            icon_list.add_option(option)

        # Store icons for later retrieval
        self.icons = suggestions

    def on_button_pressed(self, event: Button.Pressed):
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "icon-select-btn":
            self.select_icon()
        elif button_id == "icon-search-btn":
            self.search_icons()
        elif button_id == "icon-cancel-btn":
            self.close()

    def select_icon(self):
        """Select the currently highlighted icon."""
        icon_list = self.query_one("#icon-list", OptionList)

        if icon_list.option_count == 0:
            return

        # Get selected option
        selected_index = icon_list.highlighted
        if selected_index is not None and selected_index < len(self.icons):
            self.selected_icon = self.icons[selected_index]

            if self.selected_callback:
                self.selected_callback(self.selected_icon)

            self.close()

    def search_icons(self):
        """Open search dialog."""
        # This would open a text input for custom search
        # For now, just close the picker
        self.close()

    def close(self):
        """Close the picker."""
        self.display = False
