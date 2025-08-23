# tools/srt_editor/srt_editor_styles.py

# Define the specific colors for the syntax highlighter.
# This keeps the tool's color definitions separate from the main styles.
HIGHLIGHTING_COLORS = {
    'dark': {
        'index': '#e67e22',       # A shade of orange
        'time': '#5dade2',        # A soft blue
        'text': '#ecf0f1'         # Primary text color from dark theme
    },
    'light': {
        'index': '#d35400',       # A stronger orange
        'time': '#2980b9',        # A stronger blue
        'text': '#2c3e50'         # Primary text color from light theme
    },
    'contrast': {
        'index': 'blue',
        'time': 'red',
        'text': 'black'
    }
}

# A theme-agnostic template for the Merge tool's stylesheet.
# The placeholders like {bg_primary}, {text_primary}, etc., will be
# filled in by the StyleManager at runtime with the current theme's colors.

STYLE_TEMPLATE = """
    /* --- Styles for SrtEditorTool --- */

    SrtEditorTool > QPlainTextEdit {{
        background-color: {colors["bg_tertiary"]};
        color: {colors["text_primary"]}; /* This is the default text color */
        border: 1px solid {colors["border_color"]};
        border-radius: 5px;
        padding: 5px;
        font-family: Consolas, "Courier New", monospace;
    }}

    SrtEditorTool > QWidget > QPushButton {{
        margin-bottom: 5px; /* Add some space between buttons */
    }}
"""