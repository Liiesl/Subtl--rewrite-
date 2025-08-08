import os
import re
from datetime import timedelta

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton,
                               QFileDialog, QMessageBox, QLineEdit, QStackedWidget, QFrame,
                               QSizePolicy, QListWidget, QComboBox, QCheckBox, QSpacerItem)
from PySide6.QtGui import QColor, QPixmap, QIcon
from PySide6.QtCore import Qt, Signal

# Self-definition for the Merge Lines tool
TOOL_DEFINITION = {
    "display_name": "🔗 Merge Lines",
    "description": "Combine multiple subtitle lines into one.",
    "widget_class_name": "MergeTool"
}

class MergeTool(QWidget):
    """
    A tool to merge multiple SRT subtitle files in two different modes:
    1. Glue End to End: Appends a subtitle file to another, offsetting the timestamps.
    2. Stacked Merge: Combines subtitles that overlap in time into single entries.
    """
    def __init__(self):
        super().__init__()
        self.setProperty("class", "tool-widget")

        self.main_subtitle_path = ""
        self.secondary_subtitle_paths = []

        self._setup_ui()

    def _setup_ui(self):
        """Initializes the entire user interface for the tool."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Mode Selection
        self._setup_mode_selection(main_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setObjectName("separator")
        main_layout.addWidget(separator)

        # Stacked widget to switch between modes
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Create and add mode widgets to the stack
        self._setup_glue_end_to_end_mode()
        self._setup_stacked_merge_mode()

        # Set initial mode
        self.show_glue_end_to_end()

    def _setup_mode_selection(self, layout):
        """Sets up the 'Glue End to End' and 'Stacked Merge' mode buttons."""
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Select Mode:")
        mode_label.setObjectName("mode_label")
        mode_layout.addWidget(mode_label)

        self.glue_end_to_end_button = QPushButton("Glue End to End")
        self.glue_end_to_end_button.setObjectName("mode_button")
        self.glue_end_to_end_button.setCheckable(True)
        self.glue_end_to_end_button.clicked.connect(self.show_glue_end_to_end)
        mode_layout.addWidget(self.glue_end_to_end_button)

        self.stacked_merge_button = QPushButton("Stacked Merge")
        self.stacked_merge_button.setObjectName("mode_button")
        self.stacked_merge_button.setCheckable(True)
        self.stacked_merge_button.clicked.connect(self.show_stacked_merge)
        mode_layout.addWidget(self.stacked_merge_button)

        mode_layout.addStretch()
        layout.addLayout(mode_layout)

    def _setup_glue_end_to_end_mode(self):
        """Sets up the UI for the 'Glue End to End' merge mode."""
        self.glue_end_to_end_widget = QWidget()
        layout = QVBoxLayout(self.glue_end_to_end_widget)
        layout.setSpacing(15)

        # Main subtitle file
        layout.addWidget(QLabel("1. Select the first subtitle file:"))
        main_file_layout = QHBoxLayout()
        self.glue_main_button = QPushButton("Select Main Subtitle")
        self.glue_main_button.clicked.connect(self._select_main_subtitle)
        self.glue_main_file_preview = QLabel("No file selected.")
        self.glue_main_file_preview.setObjectName("file_preview")
        main_file_layout.addWidget(self.glue_main_button)
        main_file_layout.addWidget(self.glue_main_file_preview)
        main_file_layout.addStretch()
        layout.addLayout(main_file_layout)

        # Secondary subtitle file
        layout.addWidget(QLabel("2. Select the subtitle file to append:"))
        secondary_file_layout = QHBoxLayout()
        self.glue_secondary_button = QPushButton("Select Secondary Subtitle")
        self.glue_secondary_button.clicked.connect(self._select_secondary_subtitle_glue)
        self.glue_secondary_file_preview = QLabel("No file selected.")
        self.glue_secondary_file_preview.setObjectName("file_preview")
        secondary_file_layout.addWidget(self.glue_secondary_button)
        secondary_file_layout.addWidget(self.glue_secondary_file_preview)
        secondary_file_layout.addStretch()
        layout.addLayout(secondary_file_layout)

        # Auto-decide option
        auto_decide_layout = QHBoxLayout()
        self.auto_decide_checkbox = QCheckBox("Auto-decide end time from main subtitle's last line")
        self.auto_decide_checkbox.stateChanged.connect(self._toggle_base_length_input)
        auto_decide_layout.addWidget(self.auto_decide_checkbox)
        auto_decide_layout.addStretch()
        layout.addLayout(auto_decide_layout)

        # Base length input
        self.base_length_label = QLabel("3. Or, enter the length of the first subtitle's video (hh:mm:ss):")
        layout.addWidget(self.base_length_label)
        base_length_layout = QHBoxLayout()
        self.base_length_input = QLineEdit("00:00:00")
        self.base_length_input.setObjectName("time_input")
        self.base_length_input.setFixedWidth(100)
        base_length_layout.addWidget(self.base_length_input)
        base_length_layout.addStretch()
        layout.addLayout(base_length_layout)
        
        layout.addStretch()

        # Export button
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        self.glue_export_button = QPushButton("Export Merged File")
        self.glue_export_button.setObjectName("export_button")
        self.glue_export_button.clicked.connect(self._glue_end_to_end_merge)
        export_layout.addWidget(self.glue_export_button)
        layout.addLayout(export_layout)

        self.stacked_widget.addWidget(self.glue_end_to_end_widget)
        self.auto_decide_checkbox.setChecked(False)


    def _setup_stacked_merge_mode(self):
        """Sets up the UI for the 'Stacked Merge' mode."""
        self.stacked_merge_widget = QWidget()
        layout = QVBoxLayout(self.stacked_merge_widget)
        layout.setSpacing(15)

        # Main subtitle file selection
        layout.addWidget(QLabel("1. Select the main subtitle file (base timings):"))
        main_file_layout = QHBoxLayout()
        self.stack_main_button = QPushButton("Select Main Subtitle")
        self.stack_main_button.clicked.connect(self._select_main_subtitle)
        self.stack_main_file_preview = QLabel("No file selected.")
        self.stack_main_file_preview.setObjectName("file_preview")
        main_file_layout.addWidget(self.stack_main_button)
        main_file_layout.addWidget(self.stack_main_file_preview)
        main_file_layout.addStretch()
        layout.addLayout(main_file_layout)

        # Secondary subtitle files selection
        layout.addWidget(QLabel("2. Select one or more secondary subtitles to merge:"))
        secondary_file_layout = QHBoxLayout()
        self.stack_secondary_button = QPushButton("Select Secondary Subtitles")
        self.stack_secondary_button.clicked.connect(self._select_multiple_secondary_subtitles)
        secondary_file_layout.addWidget(self.stack_secondary_button)
        secondary_file_layout.addStretch()
        layout.addLayout(secondary_file_layout)
        
        self.secondary_file_list = QListWidget()
        self.secondary_file_list.setObjectName("file_list")
        self.secondary_file_list.setFixedHeight(100)
        layout.addWidget(self.secondary_file_list)

        # Color options
        self._setup_color_options(layout)
        
        layout.addStretch()

        # Export button
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        self.stack_export_button = QPushButton("Export Merged File")
        self.stack_export_button.setObjectName("export_button")
        self.stack_export_button.clicked.connect(self._stacked_merge)
        export_layout.addWidget(self.stack_export_button)
        layout.addLayout(export_layout)

        self.stacked_widget.addWidget(self.stacked_merge_widget)

    def _setup_color_options(self, layout):
        """Sets up the color selection UI for stacked merge."""
        color_group_layout = QHBoxLayout()
        self.color_checkbox = QCheckBox("Color the merged subtitles?")
        self.color_checkbox.setObjectName("color_checkbox")
        self.color_checkbox.stateChanged.connect(self._toggle_color_options)
        color_group_layout.addWidget(self.color_checkbox)
        color_group_layout.addStretch()
        layout.addLayout(color_group_layout)
        
        self.color_options_widget = QWidget()
        color_layout = QHBoxLayout(self.color_options_widget)
        color_layout.setContentsMargins(0, 5, 0, 5)

        self.color_palette = QComboBox()
        self.color_palette.setObjectName("color_palette")
        self._add_color_options_to_palette()
        color_layout.addWidget(QLabel("Color:"))
        color_layout.addWidget(self.color_palette)

        self.hex_input = QLineEdit()
        self.hex_input.setObjectName("hex_input")
        self.hex_input.setPlaceholderText("#RRGGBB")
        color_layout.addWidget(QLabel("or HEX:"))
        color_layout.addWidget(self.hex_input)
        color_layout.addStretch()
        layout.addWidget(self.color_options_widget)

        self.color_options_widget.setVisible(False)

    def _toggle_color_options(self, state):
        """Shows or hides the color selection widgets."""
        is_checked = (state == Qt.CheckState.Checked.value)
        self.color_options_widget.setVisible(is_checked)
        
    def _toggle_base_length_input(self, state):
        """Disables the manual time input if auto-decide is checked."""
        is_checked = (state == Qt.CheckState.Checked.value)
        self.base_length_input.setEnabled(not is_checked)
        self.base_length_label.setEnabled(not is_checked)
        if is_checked:
            self.base_length_input.setText("Auto")
        else:
            self.base_length_input.setText("00:00:00")

    def _add_color_options_to_palette(self):
        """Populates the color dropdown with predefined colors."""
        colors = {
            "Red": "#FF0000", "Orange": "#FFA500", "Yellow": "#FFFF00",
            "Green": "#008000", "Blue": "#0000FF", "Indigo": "#4B0082", "Violet": "#EE82EE"
        }
        for name, hex_code in colors.items():
            pixmap = QPixmap(20, 20)
            pixmap.fill(QColor(hex_code))
            icon = QIcon(pixmap)
            self.color_palette.addItem(icon, name, userData=hex_code)

    def show_glue_end_to_end(self):
        """Switches the view to the 'Glue End to End' mode."""
        self.stacked_widget.setCurrentWidget(self.glue_end_to_end_widget)
        self.glue_end_to_end_button.setChecked(True)
        self.stacked_merge_button.setChecked(False)

    def show_stacked_merge(self):
        """Switches the view to the 'Stacked Merge' mode."""
        self.stacked_widget.setCurrentWidget(self.stacked_merge_widget)
        self.glue_end_to_end_button.setChecked(False)
        self.stacked_merge_button.setChecked(True)

    def _select_main_subtitle(self):
        """Opens a file dialog to select the main .srt file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Main Subtitle File", "", "Subtitle Files (*.srt)")
        if file_path:
            self.main_subtitle_path = file_path
            base_name = os.path.basename(file_path)
            self.glue_main_file_preview.setText(base_name)
            self.stack_main_file_preview.setText(base_name)

    def _select_secondary_subtitle_glue(self):
        """Opens a file dialog for the single secondary subtitle in glue mode."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Secondary Subtitle File", "", "Subtitle Files (*.srt)")
        if file_path:
            # Use a list for consistency, even though it's just one file
            self.secondary_subtitle_paths = [file_path]
            self.glue_secondary_file_preview.setText(os.path.basename(file_path))

    def _select_multiple_secondary_subtitles(self):
        """Opens a file dialog to select multiple secondary .srt files."""
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Secondary Subtitle Files", "", "Subtitle Files (*.srt)")
        if file_paths:
            self.secondary_subtitle_paths = file_paths
            self.secondary_file_list.clear()
            for path in file_paths:
                self.secondary_file_list.addItem(os.path.basename(path))

    def _glue_end_to_end_merge(self):
        """Performs the 'Glue End to End' merge operation."""
        if not self.main_subtitle_path or not self.secondary_subtitle_paths:
            self._show_error("Please select both main and secondary subtitle files.")
            return

        try:
            offset_delta = None
            if self.auto_decide_checkbox.isChecked():
                main_content = self._read_file(self.main_subtitle_path)
                main_subs = self._parse_srt(main_content)
                if not main_subs:
                    self._show_error("Could not find any subtitles in the main file to auto-decide the time.")
                    return
                offset_delta = max(sub['end'] for sub in main_subs)
            else:
                base_length_str = self.base_length_input.text()
                if not re.match(r'^\d{2}:\d{2}:\d{2}$', base_length_str):
                    self._show_error("Invalid time format for manual input. Please use hh:mm:ss.")
                    return
                h, m, s = map(int, base_length_str.split(':'))
                offset_delta = timedelta(hours=h, minutes=m, seconds=s)
            
            main_content = self._read_file(self.main_subtitle_path)
            secondary_content = self._read_file(self.secondary_subtitle_paths[0])

            offset_content = self._offset_subtitle_times(secondary_content, offset_delta)
            
            # Renumber the second subtitle part before merging
            last_main_index = len(self._parse_srt(main_content))
            renumbered_offset_content = self._renumber_srt(offset_content, last_main_index + 1)
            
            merged_content = main_content.strip() + '\n\n' + renumbered_offset_content.strip()

            default_save_name = self._generate_output_filename()
            export_dir = os.path.dirname(self.main_subtitle_path) #. [1, 2, 3, 5, 6]
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Merged File", os.path.join(export_dir, default_save_name), "Subtitle Files (*.srt)") #. [4, 11, 12, 13]
            if save_path:
                self._write_file(save_path, merged_content)
                self._show_success("Merged file saved successfully!")
        except Exception as e:
            self._show_error(f"An error occurred while merging:\n\n{e}")


    def _stacked_merge(self):
        """Performs the 'Stacked Merge' operation."""
        if not self.main_subtitle_path or not self.secondary_subtitle_paths:
            self._show_error("Please select the main subtitle and at least one secondary subtitle.")
            return

        color_hex = None
        if self.color_checkbox.isChecked():
            color_hex = self.hex_input.text().strip()
            if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color_hex):
                # If hex is invalid, use the palette selection
                color_hex = self.color_palette.currentData()

        try:
            merged_content = self._merge_subtitles_stacked(self.main_subtitle_path, self.secondary_subtitle_paths, color_hex)
            default_save_name = self._generate_output_filename()
            export_dir = os.path.dirname(self.main_subtitle_path) #. [1, 2, 3, 5, 6]
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Merged File", os.path.join(export_dir, default_save_name), "Subtitle Files (*.srt)") #. [4, 11, 12, 13]
            if save_path:
                self._write_file(save_path, merged_content)
                self._show_success("Merged file saved successfully!")
        except Exception as e:
            self._show_error(f"An error occurred while merging:\n\n{e}")

    def _generate_output_filename(self):
        """Generates a default output filename based on the main subtitle file."""
        if not self.main_subtitle_path:
            return "merged.srt"  # Fallback

        base_name, extension = os.path.splitext(os.path.basename(self.main_subtitle_path))

        # Check if "_Subtl" or "_Subtl_" is already in the name
        if "_Subtl_" in base_name or base_name.endswith("_Subtl"):
            new_base_name = base_name + "Merged"
        else:
            new_base_name = base_name + "_Subtl_Merged"
        
        return new_base_name + extension

    # --- Backend and Utility Methods ---

    def _read_file(self, path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            return f.read()

    def _write_file(self, path, content):
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(content)

    def _srt_time_to_timedelta(self, srt_time):
        h, m, s, ms = map(int, re.split('[:,]', srt_time))
        return timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms)

    def _timedelta_to_srt_time(self, td):
        total_seconds = td.total_seconds()
        h, rem = divmod(total_seconds, 3600)
        m, s = divmod(rem, 60)
        ms = td.microseconds / 1000
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(ms):03d}"

    def _offset_subtitle_times(self, content, offset_delta):
        """Offsets all timestamps in an SRT content string by a given timedelta."""
        new_content = []
        for line in content.splitlines():
            if '-->' in line:
                start_str, end_str = line.split(' --> ')
                start_time = self._srt_time_to_timedelta(start_str) + offset_delta
                end_time = self._srt_time_to_timedelta(end_str) + offset_delta
                new_content.append(f"{self._timedelta_to_srt_time(start_time)} --> {self._timedelta_to_srt_time(end_time)}")
            else:
                new_content.append(line)
        return '\n'.join(new_content)
    
    def _renumber_srt(self, content, start_index):
        """Renumbers all entries in an SRT content string starting from a given index."""
        lines = content.splitlines()
        new_lines = []
        is_subtitle_entry = False
        for line in lines:
            if line.strip().isdigit() and not is_subtitle_entry:
                new_lines.append(str(start_index))
                start_index += 1
                is_subtitle_entry = True
            elif '-->' in line:
                new_lines.append(line)
            elif not line.strip():
                is_subtitle_entry = False
                new_lines.append(line)
            else:
                new_lines.append(line)
        return '\n'.join(new_lines)


    def _parse_srt(self, content):
        """Parses SRT content into a list of subtitle objects."""
        pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
        subs = []
        for match in pattern.finditer(content + "\n\n"):
            subs.append({
                'index': int(match.group(1)),
                'start': self._srt_time_to_timedelta(match.group(2)),
                'end': self._srt_time_to_timedelta(match.group(3)),
                'text': match.group(4).strip()
            })
        return subs
    
    def _merge_subtitles_stacked(self, main_path, secondary_paths, color_hex):
        """Merges secondary subtitles into the main one based on time overlap."""
        main_subs = self._parse_srt(self._read_file(main_path))
        
        all_secondary_subs = []
        for path in secondary_paths:
            all_secondary_subs.extend(self._parse_srt(self._read_file(path)))
            
        for main_sub in main_subs:
            for sec_sub in all_secondary_subs:
                # Check for time overlap
                if main_sub['start'] < sec_sub['end'] and main_sub['end'] > sec_sub['start']:
                    sec_text = sec_sub['text']
                    if color_hex:
                        sec_text = f'<font color="{color_hex}">{sec_text}</font>'
                    main_sub['text'] += '\n' + sec_text
        
        # Reconstruct the SRT content
        new_content = []
        for i, sub in enumerate(main_subs, 1):
            new_content.append(str(i))
            new_content.append(f"{self._timedelta_to_srt_time(sub['start'])} --> {self._timedelta_to_srt_time(sub['end'])}")
            new_content.append(sub['text'])
            new_content.append('')
            
        return '\n'.join(new_content)

    def _show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def _show_success(self, message):
        QMessageBox.information(self, "Success", message)