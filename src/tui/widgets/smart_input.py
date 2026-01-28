"""
Custom Input widgets that handle autocomplete suggestions with arrow indicators.

These widgets show the arrow indicator (🠊) for visual hints but strip it
from the actual completed text when users press the right arrow key.
"""

from textual.widgets import Input


class SmartInput(Input):
    """
    Custom Input widget that strips arrow indicators from completed suggestions.
    
    Shows the arrow (🠊) as a visual hint but removes it during completion.
    
    This works by intercepting the suggestion text before it gets applied.
    """
    
    def action_cursor_right(self) -> None:
        """Handle cursor right, cleaning suggestions with arrows."""
        # Check if we're completing a suggestion
        if (self.cursor_position == len(self.value) and 
            self._suggestion and 
            self._suggestion.endswith(" 🠊")):
            
            # Directly set the clean suggestion value
            clean_suggestion = self._suggestion.rstrip(" 🠊")
            self.value = clean_suggestion
            self.cursor_position = len(clean_suggestion)
            self._suggestion = ""
            
            # Post the value changed message to update the display
            self.post_message(self.Changed(self, clean_suggestion))
        else:
            # Normal cursor movement
            super().action_cursor_right()