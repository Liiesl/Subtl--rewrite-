# tools/split/styles.py

# A theme-agnostic template for the Merge tool's stylesheet.
# The placeholders like {bg_primary}, {text_primary}, etc., will be
# filled in by the StyleManager at runtime with the current theme's colors.

STYLE_TEMPLATE = """
    /* --- Styles for SplitTool Placeholder --- */

    SplitTool #placeholder_label {{
        font-size: 18px;
        qproperty-alignment: 'AlignCenter';
        font-weight: bold;
        color: {colors["text_primary"]};
    }}
"""