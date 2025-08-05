# main.py

import sys
import traceback
from PySide6.QtWidgets import ( QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QMessageBox)
from PySide6.QtCore import Qt, QSettings
from chrome.titlebar import CustomTitleBar
from chrome.tab import TabManager
from styles import style_manager # Import the new style_manager instance
from settings_dialog import SettingsDialog # Import the settings dialog

class Subtle(QMainWindow):
    """
    The main window for the Subtitle Manipulation Tool with a Chrome-like UI.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subtl (rewrite)")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Initialize QSettings
        self.settings = QSettings("Subtle", "Subtle")

        main_widget = QWidget()
        main_widget.setObjectName("main_content")
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # The QStackedWidget will hold the content for each tab page
        self.pages_widget = QStackedWidget()

        # The CustomTitleBar now contains and manages the tab UI container
        # The resizer is now auto-installed by default for 'main_window' type
        self.title_bar = CustomTitleBar(self, bar_type='main_window')

        # The TabManager handles all tab logic, linking the UI to the content
        self.tab_manager = TabManager(self, self.pages_widget, self.title_bar.tab_container)

        # Connect title bar controls to the tab manager's navigation methods
        self.title_bar.back_button.clicked.connect(self.tab_manager.go_back)
        self.title_bar.forward_button.clicked.connect(self.tab_manager.go_forward)

        # Connect signals from the title bar menu
        self.title_bar.settings_requested.connect(self.open_settings_dialog)

        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.pages_widget)

        # Load and set the initial stylesheet using the style manager
        self.load_and_apply_style()

        # Open the initial tab via the manager
        self.tab_manager.open_new_dashboard_tab()

        self.setCentralWidget(main_widget)
        self.error_dialog = None # To hold a reference to the error dialog

    def load_and_apply_style(self):
        """Loads the theme and font size from QSettings and applies the style."""
        # Get saved theme, defaulting to 'dark' if not found
        saved_theme = self.settings.value("theme", "dark")
        # Get saved font size, defaulting to 14 if not found
        saved_font_size = self.settings.value("font_size", 14, type=int)
        
        # Configure the style manager with the loaded settings
        style_manager.set_style_properties(theme=saved_theme, font_size=saved_font_size)
        
        # Apply the generated stylesheet to the application
        self.setStyleSheet(style_manager.get_stylesheet())

    def open_settings_dialog(self):
        """
        Opens the settings dialog and reloads the style if settings were changed.
        """
        dialog = SettingsDialog(self)
        # The dialog's accept() method saves settings and updates the style_manager.
        # We just need to react and re-apply the stylesheet.
        if dialog.exec():
            print("Settings dialog accepted. Reloading styles from settings.")
            # Reload and apply all styles, as the dialog has already saved them
            self.load_and_apply_style()
        else:
            print("Settings dialog cancelled.")

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """
        Custom exception handler to display errors in a non-blocking GUI dialog
        while also printing the full traceback to the console.
        """
        # Print the traceback to the console
        print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))

        # Create and show a non-blocking error message box
        error_message = f"An unexpected error occurred:\n\n{exc_value}\n\nSee the console for more details."
        self.error_dialog = QMessageBox(self)
        self.error_dialog.setIcon(QMessageBox.Icon.Critical)
        self.error_dialog.setText("Application Error")
        self.error_dialog.setInformativeText(error_message)
        self.error_dialog.setWindowTitle("Error")
        self.error_dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.error_dialog.setModal(False) # Make it non-blocking
        self.error_dialog.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Subtle()

    # Set the global exception handler
    sys.excepthook = window.handle_exception

    window.show()
    sys.exit(app.exec())