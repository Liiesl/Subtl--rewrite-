# tools/merge/styles.py

def get_stylesheet(colors):
    """
    Returns the stylesheet for the MergeTool.
    'colors' is a dictionary of the current theme's colors.
    """
    return f"""
        MergeTool #placeholder_label {{
            font-size: 18px;
            qproperty-alignment: 'AlignCenter';
            font-weight: bold;
            color: {colors["text_primary"]};
        }}

        /* --- General Styles for MergeTool --- */
        MergeTool, MergeTool QWidget {{
            background-color: {colors["bg_primary"]};
            color: {colors["text_primary"]};
            font-size: 14px;
        }}

        MergeTool QLabel {{
            color: {colors["text_primary"]};
            padding: 2px 0;
        }}

        MergeTool #mode_label {{
            font-weight: bold;
            font-size: 15px;
        }}

        MergeTool #file_preview, MergeTool #glue_secondary_file_preview {{
            color: {colors["text_primary"]};
            font-style: italic;
            margin-left: 10px;
        }}

        MergeTool QPushButton {{
            background-color: {colors["accent_primary"]};
            color: {colors["text_accent"]};
            border: 1px solid {colors["border_color"]};
            border-radius: 4px;
            padding: 8px 12px;
            min-height: 20px;
        }}

        MergeTool QPushButton:hover {{
            background-color: {colors["accent_hover"]};
        }}

        MergeTool QPushButton:pressed {{
            background-color: {colors["accent_hover"]};
        }}

        MergeTool #mode_button {{
            padding: 6px 10px;
        }}
        
        MergeTool #mode_button:checked {{
            background-color: {colors["accent_primary"]};
            color: {colors["text_accent"]};
            border: 1px solid {colors["accent_primary"]};
        }}

        MergeTool #export_button {{
            font-weight: bold;
            padding: 10px 20px;
        }}

        MergeTool QLineEdit, MergeTool QComboBox, MergeTool QListWidget {{
            background-color: {colors["bg_secondary"]};
            border: 1px solid {colors["border_color"]};
            border-radius: 4px;
            padding: 6px;
            color: {colors["text_primary"]};
        }}
        
        MergeTool QLineEdit:focus, MergeTool QComboBox:focus, MergeTool QListWidget:focus {{
            border: 1px solid {colors["accent_primary"]};
        }}
        
        MergeTool #time_input {{
             font-family: "Courier New", "Lucida Console", monospace;
        }}

        MergeTool QFrame#separator {{
            background-color: {colors["border_color"]};
            height: 1px;
            border: none;
        }}

        MergeTool QCheckBox::indicator {{
            width: 18px;
            height: 18px;
        }}
        
        MergeTool QCheckBox::indicator:unchecked {{
            background-color: {colors["bg_secondary"]};
            border: 1px solid {colors["border_color"]};
            border-radius: 4px;
        }}

        MergeTool QCheckBox::indicator:checked {{
            background-color: {colors["accent_primary"]};
            border: 1px solid {colors["accent_primary"]};
            image: url(check-icon.svg); /* A checkmark icon would be needed */
        }}

        MergeTool QComboBox::drop-down {{
            border: none;
        }}
    """