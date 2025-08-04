# tools/split/split_tool.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

# Self-definition for the Split Lines tool
TOOL_DEFINITION = {
    "display_name": "✂️ Split Lines",
    "description": "Split long subtitle lines into two.",
    "widget_class_name": "SplitTool"
}

class SplitTool(QWidget):
    """Placeholder widget for the Split Lines tool."""
    def __init__(self):
        super().__init__()
        self.setProperty("class", "tool-widget")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel(f"{TOOL_DEFINITION['display_name']} - Placeholder")
        label.setObjectName("placeholder_label")
        
        layout.addWidget(label)