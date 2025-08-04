# tools/subtitle_shifter/styles.py

def get_stylesheet(colors):
    """
    Returns the stylesheet for the SubtitleShifterTool placeholder.
    'colors' is a dictionary of the current theme's colors, available for future use.
    """
    return f"""
        /* --- Styles for SubtitleShifterTool Placeholder --- */

        SubtitleShifterTool #placeholder_label {{
            font-size: 18px;
            qproperty-alignment: 'AlignCenter';
            font-weight: bold;
            color: {colors["label_text"]};
        }}
    """