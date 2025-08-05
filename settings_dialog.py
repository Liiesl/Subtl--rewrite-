# settings_dialog.py

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QComboBox,
                               QDialogButtonBox, QLabel, QWidget, QStackedWidget, QSpinBox)
from PySide6.QtCore import QSettings, Qt
from styles import style_manager
from chrome.titlebar import CustomTitleBar

class SettingsDialog(QDialog):
    """
    A dialog for configuring application settings, using a custom title bar with tabs.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Make the dialog frameless to use the custom title bar
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)

        self.settings = QSettings("Subtle", "Subtle")

        # --- Main Layout ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0) # No margins for the main layout
        main_layout.setSpacing(0)

        # --- Tab Configuration ---
        self.tabs = ["Appearance", "General"]

        # --- Custom Title Bar ---
        # Create a 'settings' type title bar with tabs
        self.title_bar = CustomTitleBar(self, bar_type='settings', tabs_config=self.tabs)

        # --- Content Area ---
        # This widget will hold the actual settings controls
        content_widget = QWidget()
        content_widget.setObjectName("main_content") # For styling
        content_layout = QVBoxLayout(content_widget)

        # --- Stacked Widget for Tab Content ---
        self.stacked_widget = QStackedWidget()

        # --- Create and Add Pages ---
        self.create_appearance_page()
        self.create_general_page()

        # Connect tab bar signal to stacked widget slot
        if hasattr(self.title_bar, 'settings_tab_bar'):
            self.title_bar.settings_tab_bar.currentChanged.connect(self.stacked_widget.setCurrentIndex)

        content_layout.addWidget(self.stacked_widget)

        # --- Button Box ---
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        content_layout.addWidget(button_box)

        # --- Add Title Bar and Content to Main Layout ---
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(content_widget)

    def create_appearance_page(self):
        """Creates the content widget for the 'Appearance' tab."""
        appearance_page = QWidget()
        form_layout = QFormLayout(appearance_page)
        # By setting the RowWrapPolicy to DontWrapRows, we ensure that the input
        # controls stay on the same line as their labels.
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)

        # --- Theme Setting ---
        self.theme_combo = QComboBox()
        available_themes = style_manager.get_available_themes()
        self.theme_combo.addItems([theme.capitalize() for theme in available_themes])
        current_theme = self.settings.value("theme", "dark")
        self.theme_combo.setCurrentText(current_theme.capitalize())
        form_layout.addRow(QLabel("Theme:"), self.theme_combo)

        # --- Font Size Setting ---
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(10, 22)
        self.font_size_spinbox.setSuffix(" pt")
        current_font_size = self.settings.value("font_size", 14, type=int)
        self.font_size_spinbox.setValue(current_font_size)
        form_layout.addRow(QLabel("Base Font Size:"), self.font_size_spinbox)

        self.stacked_widget.addWidget(appearance_page)

    def create_general_page(self):
        """Creates a placeholder content widget for the 'General' tab."""
        general_page = QWidget()
        layout = QVBoxLayout(general_page)
        label = QLabel("General settings will go here.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.stacked_widget.addWidget(general_page)

    def get_selected_settings(self):
        """Returns the selected appearance settings from the dialog."""
        return {
            "theme": self.theme_combo.currentText().lower(),
            "font_size": self.font_size_spinbox.value()
        }

    def accept(self):
        """
        Saves the settings when the OK button is clicked.
        """
        selected = self.get_selected_settings()
        self.settings.setValue("theme", selected["theme"])
        self.settings.setValue("font_size", selected["font_size"])

        # Update the style manager instance with the new settings
        style_manager.set_style_properties(
            theme=selected["theme"],
            font_size=selected["font_size"]
        )
        super().accept()