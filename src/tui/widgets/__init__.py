"""Custom widgets for desktop file maker TUI."""

from .icon_selector import IconSelectorModal
from .exec_suggester import ExecutableSuggester
from .icon_path_suggester import IconPathSuggester
from .smart_input import SmartInput

__all__ = ["IconSelectorModal", "ExecutableSuggester", "IconPathSuggester", "SmartInput"]
