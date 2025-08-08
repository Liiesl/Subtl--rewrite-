# tools/srt_editor/srt_editor.py

import re
import qtawesome as qta
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QPlainTextEdit, QLineEdit, QLabel
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QTextDocument, QTextCursor

# Import the global style manager to get the current theme
from styles import style_manager
# Import this tool's specific style definitions
from . import srt_editor_styles

TOOL_DEFINITION = {
    "display_name": "📝 SRT Editor",
    "description": "A color-coded editor for SRT subtitle files.",
    "widget_class_name": "SrtEditorTool",
    "can_open_file": True
}

# --- Syntax Highlighter ---
class SrtHighlighter(QSyntaxHighlighter):
    """A syntax highlighter for the SRT subtitle format."""
    def __init__(self, parent, formats):
        super().__init__(parent)
        self.formats = formats
        
        # Regex for SRT parts
        self.rules = [
            # Rule for the timestamp line
            (QRegularExpression(r"^\d{2}:\d{2}:\d{2},\d{3}\s-->\s\d{2}:\d{2}:\d{2},\d{3}$"), "time"),
            # Rule for the sequence number line (must be a line containing only digits)
            (QRegularExpression(r"^\d+$"), "index"),
        ]

    def highlightBlock(self, text):
        """Highlights a block of text (a line in this case)."""
        # Default to the text format
        self.setFormat(0, len(text), self.formats["text"])

        for pattern, format_name in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.formats[format_name])


# --- Main Tool Widget ---
class SrtEditorTool(QWidget):
    """A tool for editing SRT files with syntax highlighting."""
    def __init__(self):
        super().__init__()
        self.setProperty("class", "tool-widget")

        # --- Main Layout ---
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # --- Editor Widget ---
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Open an .srt file or paste its content here...")

        # --- Button Layout ---
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        open_button = QPushButton(qta.icon('fa5s.folder-open'), " Open File")
        save_button = QPushButton(qta.icon('fa5s.save'), " Save File")
        top_button = QPushButton(qta.icon('fa5s.arrow-up'), " Move to Top")
        bottom_button = QPushButton(qta.icon('fa5s.arrow-down'), " Move to Bottom")
        
        # --- Find Layout ---
        find_layout = QHBoxLayout()
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Find...")
        find_button = QPushButton(qta.icon('fa5s.search'), " Find Next")
        find_layout.addWidget(self.find_input)
        find_layout.addWidget(find_button)
        
        button_layout.addWidget(open_button)
        button_layout.addWidget(save_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(top_button)
        button_layout.addWidget(bottom_button)
        button_layout.addSpacing(20)
        button_layout.addLayout(find_layout)


        main_layout.addWidget(self.editor, 1) # The '1' makes the editor take up available space
        main_layout.addWidget(button_container)

        # --- Connections ---
        open_button.clicked.connect(self.open_file)
        save_button.clicked.connect(self.save_file)
        top_button.clicked.connect(self.move_to_top)
        bottom_button.clicked.connect(self.move_to_bottom)
        find_button.clicked.connect(self.find_next)
        self.find_input.returnPressed.connect(self.find_next)

        # --- Highlighter Setup ---
        self.setup_highlighter()

    def setup_highlighter(self):
        """Initializes the syntax highlighter with colors from the tool's style file."""
        # Get the current theme name ('dark', 'light', etc.)
        current_theme = style_manager.current_theme
        
        # Get the color palette for the current theme from our tool's style definitions
        # Default to 'dark' if the theme isn't found in our definition.
        color_palette = srt_editor_styles.HIGHLIGHTING_COLORS.get(
            current_theme, srt_editor_styles.HIGHLIGHTING_COLORS['dark']
        )
        
        # Create QTextCharFormat objects for each part of the SRT syntax
        formats = {}
        
        # Index format
        index_format = QTextCharFormat()
        index_format.setForeground(QColor(color_palette['index']))
        index_format.setFontWeight(QFont.Weight.Bold)
        formats['index'] = index_format
        
        # Time format
        time_format = QTextCharFormat()
        time_format.setForeground(QColor(color_palette['time']))
        formats['time'] = time_format

        # Text format (the default)
        text_format = QTextCharFormat()
        text_format.setForeground(QColor(color_palette['text']))
        formats['text'] = text_format
        
        # Create and apply the highlighter
        self.highlighter = SrtHighlighter(self.editor.document(), formats)

    # NEW: This method allows the TabManager to open a file when the tool is created.
    def load_file_on_startup(self, file_path):
        """
        Loads a file's content directly into the editor. Used for 'Open With...'.
        The TabManager that calls this method is responsible for handling exceptions.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            self.editor.setPlainText(f.read())

    def open_file(self):
        """Opens a file dialog to load an SRT file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open SRT File", "", "SubRip Files (*.srt);;All Files (*)")
        if file_path:
            try:
                self.load_file_on_startup(file_path)
            except Exception as e:
                # In a real app, a QMessageBox would be better
                print(f"Error opening file: {e}")

    def save_file(self):
        """Opens a file dialog to save the editor content."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save SRT File", "", "SubRip Files (*.srt);;All Files (*)")
        if file_path:
            # Ensure the file has an srt extension if the user didn't add one
            if not file_path.lower().endswith('.srt'):
                file_path += '.srt'
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.editor.toPlainText())
            except Exception as e:
                print(f"Error saving file: {e}")

    def move_to_top(self):
        """Moves the cursor to the beginning of the document."""
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.editor.setTextCursor(cursor)

    def move_to_bottom(self):
        """Moves the cursor to the end of the document."""
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.editor.setTextCursor(cursor)

    def find_next(self):
        """Finds the next occurrence of the text in the find input."""
        query = self.find_input.text()
        if query:
            self.editor.find(query)