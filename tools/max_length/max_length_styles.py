# tools/max_length/styles.py

def get_stylesheet(colors):
    """
    Returns the stylesheet for the MaxLengthTool placeholder.
    'colors' is a dictionary of the current theme's colors, available for future use.
    """
    return f"""
        /* --- Styles for MaxLengthTool Placeholder --- */

        MaxLengthTool #placeholder_label {{
            font-size: 18px;
            qproperty-alignment: 'AlignCenter';
            font-weight: bold;
            color: {colors["text_primary"]};
        }}
    """