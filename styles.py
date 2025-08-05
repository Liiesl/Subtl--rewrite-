# styles.py

import os
import inspect
import importlib.util
from tool_manager import AVAILABLE_TOOLS

class StyleManager:
    """
    Manages the application's visual styles, including themes and fonts.
    
    The color scheme is structured hierarchically:
    - bg_primary, bg_secondary, bg_tertiary: Background colors.
    - text_primary, text_accent, text_active: Text colors for different contexts.
    - accent_primary, accent_hover, accent_subtle_hover: Interactive element colors.
    - accent_close: Specific color for the close button's hover state.
    - border_color: Color for borders and separators.
    """
    def __init__(self, initial_theme='dark', initial_font_size=14):
        self.themes = {
            'dark': {
                "bg_primary": "#1b1b1b",
                "bg_secondary": "#2c2c2c",
                "bg_tertiary": "#3a3a3a",
                "text_primary": "#ecf0f1",
                "text_accent": "#ffffff",
                "text_active": "#ffffff",
                "accent_primary": "#555555",
                "accent_hover": "#666666",
                "accent_subtle_hover": "#4f4f4f",
                "accent_close": "#e74c3c",
                "border_color": "#555555",
            },
            'light': {
                "bg_primary": "#ffffff",
                "bg_secondary": "#d2d7db",
                "bg_tertiary": "#f0f0f0",
                "text_primary": "#2c3e50",
                "text_accent": "#ffffff",
                "text_active": "#2c3e50",
                "accent_primary": "#3498db",
                "accent_hover": "#2980b9",
                "accent_subtle_hover": "#bdc3c7",
                "accent_close": "#e74c3c",
                "border_color": "#95a5a6",
            },
            'contrast': {
                "bg_primary": "yellow",
                "bg_secondary": "magenta",
                "bg_tertiary": "black",
                "text_primary": "blue",
                "text_accent": "purple",
                "text_active": "red",
                "accent_primary": "orange",
                "accent_hover": "cyan",
                "accent_subtle_hover": "purple",
                "accent_close": "red",
                "border_color": "green",
            }
        }
        self.current_theme = initial_theme
        self.font_size = int(initial_font_size)

    def set_style_properties(self, theme=None, font_size=None):
        """Sets the current theme and/or font size."""
        if theme and theme in self.themes:
            self.current_theme = theme
        if font_size is not None:
            self.font_size = int(font_size)

    def get_available_themes(self):
        """Returns a list of available theme names."""
        return list(self.themes.keys())

    def _get_tool_stylesheets(self, colors):
        """
        Dynamically finds, imports, and gets the stylesheet for each available tool.
        Note: This change to the color dictionary is a breaking change for external tool stylesheets.
        """
        tool_styles = []
        for tool_id, tool_data in AVAILABLE_TOOLS.items():
            widget_class = tool_data['widget_class']
            try:
                class_file_path = inspect.getfile(widget_class)
                class_dir = os.path.dirname(class_file_path)
                
                style_module_path = os.path.join(class_dir, f'{tool_id}_styles.py')

                if os.path.exists(style_module_path):
                    spec = importlib.util.spec_from_file_location(f"tools.{tool_id}.styles", style_module_path)
                    style_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(style_module)
                    
                    if hasattr(style_module, 'get_stylesheet'):
                        style_string = style_module.get_stylesheet(colors)
                        tool_styles.append(style_string)
            except Exception as e:
                print(f"Warning: Could not load stylesheet for '{tool_id}': {e}")
                
        return "\n".join(tool_styles)

    def get_stylesheet(self):
        """Returns the full stylesheet for the application based on the current style."""
        colors = self.themes.get(self.current_theme, self.themes['dark'])
        font_size = self.font_size
        
        main_stylesheet = f"""
            CustomTitleBar, CustomTitleBar QTabBar {{
                background-color: {colors["bg_secondary"]};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }}
            /* Style for the content area of windows/dialogs */
            QWidget#main_content {{
                background-color: {colors["bg_primary"]};
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }}
            /* Title label specific to the custom title bar */
            CustomTitleBar QLabel#title_label {{
                color: {colors["text_primary"]};
                font-size: {font_size + 2}px;
                font-weight: bold;
                padding-left: 10px;
            }}
            CustomTitleBar QTabBar::tab {{
                background: {colors["bg_secondary"]};
                color: {colors["text_primary"]};
                padding: 8px 15px;
                margin-top: 2px;
                border: 1px solid {colors["bg_secondary"]};
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }}
            CustomTitleBar QTabBar::tab:selected {{
                background: {colors["bg_primary"]};
                color: {colors["text_active"]};
                margin-top: 2px;
                padding-bottom: 10px;
                 border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }}
            CustomTitleBar QTabBar::tab:!selected:hover {{
                background: {colors["accent_subtle_hover"]};
            }}
            CustomTitleBar QTabBar::close-button {{
                image: url(close.png);
                background: transparent;
                subcontrol-position: right;
                subcontrol-origin: padding;
                padding: 2px;
                border-radius: 5px;
            }}
            CustomTitleBar QTabBar::close-button:hover {{
                background: #c0392b;
            }}
            QLabel {{
                background-color: transparent;
                color: {colors["text_primary"]};
                font-size: {font_size}px;
                padding: 10px;
            }}
            QPushButton {{
                background-color: {colors["accent_primary"]};
                color: {colors["text_accent"]};
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: {font_size - 1}px;
            }}
            QPushButton:hover {{
                background-color: {colors["accent_hover"]};
            }}
            QSpinBox {{
                background-color: {colors["bg_primary"]};
                color: {colors["text_primary"]};
                padding: 5px;
                border: 1px solid {colors["border_color"]};
                border-radius: 5px;
                font-size: {font_size - 1}px;
            }}
            QStackedWidget {{
                background-color: {colors["bg_primary"]};
            }}
            CustomTitleBar QPushButton {{
                padding: 5px;
                font-size: {font_size - 2}px;
                border-radius: 4px;
                background-color: transparent;
                color: {colors["text_primary"]};
            }}
             CustomTitleBar QPushButton:hover {{
                background-color: {colors["accent_subtle_hover"]};
            }}
            CustomTitleBar QPushButton#close_button:hover {{
                background-color: {colors["accent_close"]};
                color: {colors["text_primary"]};
            }}
            QMenu {{
                background-color: {colors["bg_tertiary"]};
                color: {colors["text_primary"]};
                border: 1px solid {colors["accent_subtle_hover"]};
                border-radius: 5px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 8px 25px 8px 20px;
                border-radius: 5px;
            }}
            QMenu::item:selected {{
                background-color: {colors["accent_subtle_hover"]};
            }}
            QMenu::separator {{
                height: 1px;
                background: {colors["border_color"]};
                margin-left: 10px;
                margin-right: 5px;
            }}
            /* Add styles for QComboBox and QDialog */
            QComboBox {{
                background-color: {colors["accent_primary"]};
                color: {colors["text_accent"]};
                padding: 5px;
                border: 1px solid {colors["border_color"]};
                border-radius: 5px;
            }}
             QComboBox:hover {{
                background-color: {colors["accent_hover"]};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                 background-color: {colors["bg_tertiary"]};
                 color: {colors["text_primary"]};
                 selection-background-color: {colors["accent_subtle_hover"]};
                 border: 1px solid {colors["accent_subtle_hover"]};
            }}
             QDialog {{
                /* The main background is now handled by main_content and CustomTitleBar */
                background-color: transparent;
            }}
        """
        
        return main_stylesheet + "\n" + self._get_tool_stylesheets(colors)

# Create a single instance of the StyleManager for the entire application to use.
style_manager = StyleManager()