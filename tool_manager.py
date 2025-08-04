# tool_manager.py

from tools.min_length_tool import MinLengthTool
from tools.placeholder_tool import PlaceholderTool

"""
The single source of truth for all available tools in the application.

Each key is a unique identifier for the tool.
The value is a dictionary containing:
    - 'display_name': The user-facing name for the tool.
    - 'widget_class': The class responsible for creating the tool's UI.
    - 'description': A brief description for the dashboard (optional).
"""
AVAILABLE_TOOLS = {
    "min_length": {
        "display_name": "📏 Minimum Length",
        "widget_class": MinLengthTool,
        "description": "Adjust the minimum display time of subtitles.",
    },
    "max_length": {
        "display_name": "📏 Maximum Length",
        "widget_class": PlaceholderTool,
        "description": "Adjust the maximum display time of subtitles.",
    },
    "merge": {
        "display_name": "🔗 Merge Lines",
        "widget_class": PlaceholderTool,
        "description": "Combine multiple subtitle lines into one.",
    },
    "split": {
        "display_name": "✂️ Split Lines",
        "widget_class": PlaceholderTool,
        "description": "Split long subtitle lines into two.",
    },
    "subtitle_shifter": {
        "display_name": "⏰ Subtitle Shifter",
        "widget_class": PlaceholderTool,
        "description": "Shift subtitle timings forwards or backwards.",
    },
    "subtitle_converter": {
        "display_name": "🔄 Subtitle Converter",
        "widget_class": PlaceholderTool,
        "description": "Convert subtitles to various formats.",
    },
    "multilingual_merge": {
        "display_name": "🌍 Multilingual Merge",
        "widget_class": PlaceholderTool,
        "description": "Merge subtitles from different languages.",
    },
}