# tools/min_length_tool.py

import srt
import os
from datetime import timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QSpinBox, 
    QComboBox, QFileDialog, QMessageBox, QHBoxLayout
)
from PySide6.QtCore import Qt

class MinLengthTool(QWidget):
    """
    UI widget for the Minimum Length tool.
    """
    def __init__(self):
        super().__init__()
        self.input_file_path = None

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # File selection
        file_select_button = QPushButton("Select SRT File")
        file_select_button.clicked.connect(self.select_file)
        self.file_path_label = QLabel("No file selected.")
        self.file_path_label.setWordWrap(True)

        # Description
        description_label = QLabel(
            "Set the minimum display time for a subtitle entry."
        )

        # Min length input widgets
        min_length_layout = QHBoxLayout()
        self.min_length_input = QSpinBox()
        self.min_length_input.setRange(1, 10000)
        self.min_length_input.setValue(1000)
        
        self.time_unit_combo = QComboBox()
        self.time_unit_combo.addItems(["Milliseconds", "Seconds", "Minutes"])
        
        min_length_layout.addWidget(self.min_length_input)
        min_length_layout.addWidget(self.time_unit_combo)

        # Apply button
        apply_button = QPushButton("Apply and Save As...")
        apply_button.clicked.connect(self.apply_min_length)

        # Add widgets to layout
        layout.addWidget(file_select_button)
        layout.addWidget(self.file_path_label)
        layout.addSpacing(20)
        layout.addWidget(description_label)
        layout.addLayout(min_length_layout)
        layout.addSpacing(20)
        layout.addWidget(apply_button)

    def select_file(self):
        """
        Open a file dialog to select an SRT file.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Open SRT File", "", "SubRip Files (*.srt)")
        if file_path:
            self.input_file_path = file_path
            self.file_path_label.setText(f"Selected: {file_path}")

    def apply_min_length(self):
        """
        Apply the minimum length to the selected SRT file and save it.
        The suggested save name is based on the original name and the applied settings.
        """
        if not self.input_file_path:
            QMessageBox.warning(self, "Warning", "Please select an SRT file first.")
            return

        min_length_val = self.min_length_input.value()
        time_unit = self.time_unit_combo.currentText()
        
        # Determine time delta and unit abbreviation for filename
        if time_unit == "Milliseconds":
            min_duration = timedelta(milliseconds=min_length_val)
            unit_abbr = "ms"
        elif time_unit == "Seconds":
            min_duration = timedelta(seconds=min_length_val)
            unit_abbr = "s"
        else:  # Minutes
            min_duration = timedelta(minutes=min_length_val)
            unit_abbr = "m"

        try:
            with open(self.input_file_path, 'r', encoding='utf-8-sig') as f:
                subtitle_generator = srt.parse(f.read())
                subtitles = list(subtitle_generator)

            # Apply the minimum duration logic
            for sub in subtitles:
                duration = sub.end - sub.start
                if duration < min_duration:
                    sub.end = sub.start + min_duration
            
            # --- Create the new default filename ---
            directory = os.path.dirname(self.input_file_path)
            base_name = os.path.basename(self.input_file_path)
            file_name, file_ext = os.path.splitext(base_name)
            
            new_file_name = f"{file_name}_{min_length_val}{unit_abbr}{file_ext}"
            default_save_path = os.path.join(directory, new_file_name)
            # --- End of filename creation ---

            output_file_path, _ = QFileDialog.getSaveFileName(self, "Save SRT File As...", default_save_path, "SubRip Files (*.srt)")

            if output_file_path:
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(srt.compose(subtitles))
                QMessageBox.information(self, "Success", f"File saved successfully to {output_file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")