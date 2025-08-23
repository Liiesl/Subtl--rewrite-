# dashboard.py

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from tools.tool_loader import AVAILABLE_TOOLS

class DashboardWidget(QWidget):
    """
    The dashboard widget that displays available tools in a grid.
    It emits a signal when a tool is selected.
    """
    # Signal to emit the tool key (a string) when a tool button is clicked
    tool_selected = Signal(str)

    def __init__(self, parent=None):
        """Initializes the dashboard widget."""
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Initializes the UI components of the dashboard."""
        layout = QGridLayout(self)
        # Align the grid to the top, so buttons don't spread out vertically
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        row, col = 0, 0
        # Iterate through the tools defined in the tool manager
        for tool_key, tool_info in AVAILABLE_TOOLS.items():
            button = QPushButton(tool_info['display_name'])
            # Connect the button's click to a lambda that emits the tool's key.
            # This ensures that the correct tool_key is captured for each button.
            button.clicked.connect(lambda checked, key=tool_key: self.tool_selected.emit(key))
            layout.addWidget(button, row, col)
            
            # Arrange the buttons in a grid with 3 columns
            col += 1
            if col > 2:
                col = 0
                row += 1