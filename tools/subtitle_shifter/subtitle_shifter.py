# tools/subtitle_shifter/subtitle_shifter_tool.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

# Self-definition for the Subtitle Shifter tool
TOOL_DEFINITION = {
    "display_name": "⏰ Subtitle Shifter",
    "description": "Shift subtitle timings forwards or backwards.",
    "widget_class_name": "SubtitleShifterTool"
}

class SubtitleShifterTool(QWidget):
    """Placeholder widget for the Subtitle Shifter tool."""
    def __init__(self):
        super().__init__()
        self.setProperty("class", "tool-widget")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label = QLabel(f"{TOOL_DEFINITION['display_name']} - Placeholder")
        label.setObjectName("placeholder_label")
        
        layout.addWidget(label)