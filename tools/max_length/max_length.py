# tools/max_length/max_length_tool.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

# Self-definition for the Max Length tool
TOOL_DEFINITION = {
    "display_name": "📏 Maximum Length",
    "description": "Adjust the maximum display time of subtitles.",
    "widget_class_name": "MaxLengthTool"
}

class MaxLengthTool(QWidget):
    """A generic placeholder widget for an unimplemented tool."""
    def __init__(self):
        super().__init__()
        self.setProperty("class", "tool-widget")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel(f"{TOOL_DEFINITION['display_name']} - Placeholder")
        label.setObjectName("placeholder_label")
        layout.addWidget(label)