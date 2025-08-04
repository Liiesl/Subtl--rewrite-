# tools/split/styles.py

def get_stylesheet(colors):
    """
    Returns the stylesheet for the SplitTool placeholder.
    'colors' is a dictionary of the current theme's colors, available for future use.
    """
    return f"""
        /* --- Styles for SplitTool Placeholder --- */

        SplitTool #placeholder_label {{
            font-size: 18px;
            qproperty-alignment: 'AlignCenter';
            font-weight: bold;
            color: {colors["label_text"]};
        }}
    """