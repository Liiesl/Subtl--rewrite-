# main.py

import sys, os
import traceback
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QMessageBox,
    QDialog, QLabel, QPushButton
)
from PySide6.QtCore import Qt, QSettings
from functools import partial

# Assuming these are in the correct path
from chrome.titlebar import CustomTitleBar
from chrome.tab import TabManager
from styles import style_manager
from settings_dialog import SettingsDialog
from tools.tool_loader import AVAILABLE_TOOLS # NEW: Import available tools

# MODIFIED: Centralized application constants to match Nuitka build
ORGANIZATION_NAME = "Liiesl"
APPLICATION_NAME = "Subtl"

# NEW: This class is the repurposed preloader.py, now acting as a tool selector.
class ChooseToolWindow(QDialog):
    """
    A dialog that appears when a file is opened, asking the user to choose
    which tool to open it with.
    """
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose a Tool")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(300, 300, 400, 200)

        self.file_path = file_path
        self.selected_tool_id = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        title_label = QLabel(f"Open With...")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        file_label = QLabel(f"File: {os.path.basename(file_path)}")
        file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addWidget(title_label)
        main_layout.addWidget(file_label)
        main_layout.addStretch()

        # MODIFIED: Dynamically create a button for each tool that can open files
        for tool_id, tool_data in AVAILABLE_TOOLS.items():
            if tool_data.get('can_open_file'): # Check the new flag
                tool_button = QPushButton(tool_data['display_name'])
                tool_button.setToolTip(tool_data.get('description', ''))
                # Use partial to pass the tool_id to the handler
                tool_button.clicked.connect(partial(self.on_tool_selected, tool_id))
                main_layout.addWidget(tool_button)

        main_layout.addStretch()
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        main_layout.addWidget(cancel_button)

    def on_tool_selected(self, tool_id):
        """Stores the selected tool and closes the dialog successfully."""
        self.selected_tool_id = tool_id
        self.accept() # Close the dialog with an "Accepted" result

class Subtle(QMainWindow):
    """
    The main window for the Subtitle Manipulation Tool with a Chrome-like UI.
    """
    # MODIFIED: __init__ now accepts startup parameters
    def __init__(self, tool_to_open=None, file_to_open=None):
        super().__init__()
        # MODIFIED: Use constant for the window title
        self.setWindowTitle(APPLICATION_NAME)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # MODIFIED: Use constants for QSettings organization and application names
        self.settings = QSettings(ORGANIZATION_NAME, APPLICATION_NAME)

        main_widget = QWidget()
        main_widget.setObjectName("main_content")
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.pages_widget = QStackedWidget()
        self.title_bar = CustomTitleBar(self, bar_type='main_window')
        self.tab_manager = TabManager(self, self.pages_widget, self.title_bar.tab_container)

        self.title_bar.back_button.clicked.connect(self.tab_manager.go_back)
        self.title_bar.forward_button.clicked.connect(self.tab_manager.go_forward)
        self.title_bar.settings_requested.connect(self.open_settings_dialog)

        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.pages_widget)

        self.load_and_apply_style()

        # MODIFIED: Conditional startup logic
        if tool_to_open and file_to_open:
            # A tool and file were specified, open them directly
            self.tab_manager.open_tool_directly(tool_to_open, file_to_open)
        else:
            # Standard startup, open the dashboard
            self.tab_manager.open_new_dashboard_tab()

        self.setCentralWidget(main_widget)
        self.error_dialog = None

    def load_and_apply_style(self):
        saved_theme = self.settings.value("theme", "dark")
        saved_font_size = self.settings.value("font_size", 14, type=int)
        style_manager.set_style_properties(theme=saved_theme, font_size=saved_font_size)
        self.setStyleSheet(style_manager.get_stylesheet())

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            self.load_and_apply_style()

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        error_message = f"An unexpected error occurred:\n\n{exc_value}\n\nSee the console for more details."
        self.error_dialog = QMessageBox(self)
        self.error_dialog.setIcon(QMessageBox.Icon.Critical)
        self.error_dialog.setText("Application Error")
        self.error_dialog.setInformativeText(error_message)
        self.error_dialog.setWindowTitle("Error")
        self.error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.error_dialog.setModal(False)
        self.error_dialog.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # MODIFIED: Main entry point logic
    file_to_open = sys.argv[1] if len(sys.argv) > 1 else None

    if file_to_open and os.path.exists(file_to_open):
        # A file was passed via the command line (from launcher.exe)
        # Show the "Choose Tool" dialog first
        chooser = ChooseToolWindow(file_to_open)
        
        # .exec() opens the dialog modally and waits for user interaction
        if chooser.exec():
            # The user chose a tool and clicked its button
            selected_tool = chooser.selected_tool_id
            
            # Launch the main window with instructions to open the specific tool and file
            window = Subtle(tool_to_open=selected_tool, file_to_open=file_to_open)
            sys.excepthook = window.handle_exception
            window.show()
            sys.exit(app.exec())
        else:
            # The user cancelled the "Choose Tool" dialog
            sys.exit(0)
    else:
        # No file argument was passed, start the application normally
        window = Subtle()
        sys.excepthook = window.handle_exception
        window.show()
        sys.exit(app.exec())