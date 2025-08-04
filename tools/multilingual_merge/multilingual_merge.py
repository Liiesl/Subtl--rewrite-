# tools/multilingual_merge/multilingual_merge_tool.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

# Self-definition for the Multilingual Merge tool
TOOL_DEFINITION = {
    "display_name": "🌍 Multilingual Merge",
    "description": "Merge subtitles from different languages.",
    "widget_class_name": "MultilingualMergeTool"
}

class MultilingualMergeTool(QWidget):
    """Placeholder widget for the Multilingual Merge tool."""
    def __init__(self):
        super().__init__()
        self.setProperty("class", "tool-widget")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel(f"{TOOL_DEFINITION['display_name']} - Placeholder")
        label.setObjectName("placeholder_label")
        
        layout.addWidget(label)