def get_stylesheet(colors):
    """
    Returns the stylesheet for the PlaceholderTool.
    'colors' is a dictionary of the current theme's colors.
    """
    return f"""
        /* --- Styles for PlaceholderTool --- */

        /* Center-align the text and make it larger */
        PlaceholderTool #placeholder_label {{
            font-size: 18px;
            qproperty-alignment: 'AlignCenter'; /* Use qproperty to set alignment */
            font-weight: bold;
        }}
    """