def get_stylesheet(colors):
    """
    Returns the stylesheet for the MinLengthTool.
    'colors' is a dictionary of the current theme's colors.
    """
    return f"""
        /* --- Styles for MinLengthTool --- */

        /* Style the file path label to be smaller and italic */
        MinLengthTool #file_path_label {{
            font-size: 13px;
            font-style: italic;
            color: {colors["text_primary"]};
            padding: 5px 10px;
        }}
        
        /* Make the buttons in the tool have a bold font */
        MinLengthTool QPushButton {{
            font-weight: bold;
        }}
    """