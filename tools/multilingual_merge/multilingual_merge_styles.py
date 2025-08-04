# tools/multilingual_merge/styles.py

def get_stylesheet(colors):
    """
    Returns the stylesheet for the MultilingualMergeTool placeholder.
    'colors' is a dictionary of the current theme's colors, available for future use.
    """
    return f"""
        /* --- Styles for MultilingualMergeTool Placeholder --- */

        MultilingualMergeTool #placeholder_label {{
            font-size: 18px;
            qproperty-alignment: 'AlignCenter';
            font-weight: bold;
            color: {colors["label_text"]};
        }}
    """