# A theme-agnostic template for the Merge tool's stylesheet.
# The placeholders like {bg_primary}, {text_primary}, etc., will be
# filled in by the StyleManager at runtime with the current theme's colors.

STYLE_TEMPLATE = """
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