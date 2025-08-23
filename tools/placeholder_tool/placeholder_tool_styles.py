# A theme-agnostic template for the Merge tool's stylesheet.
# The placeholders like {bg_primary}, {text_primary}, etc., will be
# filled in by the StyleManager at runtime with the current theme's colors.

STYLE_TEMPLATE = """
    /* --- Styles for PlaceholderTool --- */

    /* Center-align the text and make it larger */
    PlaceholderTool #placeholder_label {{
        font-size: 18px;
        qproperty-alignment: 'AlignCenter'; /* Use qproperty to set alignment */
        font-weight: bold;
    }}
"""