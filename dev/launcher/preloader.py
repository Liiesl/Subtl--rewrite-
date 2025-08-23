# preloader.py

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import QSettings, Qt
import sys

class PreloaderWindow(QWidget):
    """
    A pre-loader window to configure Python interpreter and script paths.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subtle Launcher Settings")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(300, 300, 500, 250)

        # Initialize QSettings
        self.settings = QSettings("Subtle", "SubtleLauncher")

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title Label
        title_label = QLabel("Configure Launcher")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # --- Python Interpreter Path ---
        py_path_layout = QHBoxLayout()
        self.py_path_input = QLineEdit()
        self.py_path_input.setPlaceholderText("Path to Python Interpreter (e.g., python.exe)")
        py_browse_button = QPushButton("Browse")
        py_browse_button.clicked.connect(self.browse_python_interpreter)
        py_path_layout.addWidget(self.py_path_input)
        py_path_layout.addWidget(py_browse_button)

        # --- Main.py Script Path ---
        script_path_layout = QHBoxLayout()
        self.script_path_input = QLineEdit()
        self.script_path_input.setPlaceholderText("Path to main.py script")
        script_browse_button = QPushButton("Browse")
        script_browse_button.clicked.connect(self.browse_main_script)
        script_path_layout.addWidget(self.script_path_input)
        script_path_layout.addWidget(script_browse_button)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save and Close")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Add widgets to main layout
        main_layout.addWidget(title_label)
        main_layout.addLayout(py_path_layout)
        main_layout.addLayout(script_path_layout)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.load_settings()

    def browse_python_interpreter(self):
        """Opens a file dialog to select the Python interpreter."""
        # The filter is platform-dependent
        if sys.platform == "win32":
            filter_str = "Python Executable (python.exe)"
        else:
            filter_str = "All files (*)"

        path, _ = QFileDialog.getOpenFileName(self, "Select Python Interpreter", "", filter_str)
        if path:
            self.py_path_input.setText(path)

    def browse_main_script(self):
        """Opens a file dialog to select the main.py script."""
        path, _ = QFileDialog.getOpenFileName(self, "Select main.py", "", "Python Files (*.py)")
        if path:
            self.script_path_input.setText(path)

    def load_settings(self):
        """Loads saved paths from QSettings."""
        py_path = self.settings.value("python_path", "")
        script_path = self.settings.value("script_path", "")
        self.py_path_input.setText(py_path)
        self.script_path_input.setText(script_path)

    def save_settings(self):
        """Saves the current paths to QSettings and closes the window."""
        py_path = self.py_path_input.text()
        script_path = self.script_path_input.text()

        if not py_path or not script_path:
            QMessageBox.warning(self, "Missing Information", "Both paths are required to save.")
            return

        self.settings.setValue("python_path", py_path)
        self.settings.setValue("script_path", script_path)

        QMessageBox.information(self, "Settings Saved", "Launcher settings have been saved successfully.")
        self.close()