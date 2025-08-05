# tools/placeholder_tool.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

TOOL_DEFINITION = {
    "display_name": "✂️ coming soon",
    "description": "This tool is a placeholder for future development.",
    "widget_class_name": "PlaceholderTool"
}

class PlaceholderTool(QWidget):
    """
    A generic placeholder widget for an unimplemented tool.
    """
    def __init__(self, tool_name="Placeholder"):
        super().__init__()
        
        # Add a property to identify this as a tool widget for styling
        self.setProperty("class", "tool-widget")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel(f"{tool_name} Tool - Placeholder")
        
        # Set an object name for specific styling from the styles.py module
        label.setObjectName("placeholder_label")
        
        layout.addWidget(label)