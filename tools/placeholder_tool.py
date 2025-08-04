# tools/placeholder_tool.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class PlaceholderTool(QWidget):
    """
    A generic placeholder widget for an unimplemented tool.
    """
    def __init__(self, tool_name="Placeholder"):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel(f"{tool_name} Tool - Placeholder")
        layout.addWidget(label)