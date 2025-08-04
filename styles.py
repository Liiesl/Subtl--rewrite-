# styles.py

import os
import inspect
import importlib.util
from tool_manager import AVAILABLE_TOOLS

# Dictionary to hold color values for different themes
COLORS = {
    'dark': {
        "widget_background": "#1b1b1b",
        "title_bar_background": "#2c2c2c",
        "text_color": "#ecf0f1",
        "tab_selected_background": "#1b1b1b",
        "tab_selected_text": "#ffffff",
        "label_text": "#ecf0f1",
        "button_background": "#555555",
        "button_text": "#ffffff",
        "button_hover": "#666666",
        "spinbox_border": "#555555",
        "titlebar_button_background": "transparent",
        "titlebar_button_hover": "#4f4f4f",
        "close_button_hover": "#e74c3c",
    },
    'light': {
        "widget_background": "#ffffff",
        "title_bar_background": "#d2d7db",
        "text_color": "#2c3e50",
        "tab_selected_background": "#ffffff",
        "tab_selected_text": "#2c3e50",
        "label_text": "#2c3e50",
        "button_background": "#3498db",
        "button_text": "white",
        "button_hover": "#2980b9",
        "spinbox_border": "#95a5a6",
        "titlebar_button_background": "transparent",
        "titlebar_button_hover": "#bdc3c7",
        "close_button_hover": "#e74c3c",
    },
    'contrast': {
        "widget_background": "yellow",              # Main content area
        "title_bar_background": "magenta",          # Title bar and inactive tabs
        "text_color": "black",                      # Text on inactive tabs
        "tab_selected_background": "lime",          # Active tab background
        "tab_selected_text": "red",                 # Active tab text
        "label_text": "blue",                       # Label text color
        "button_background": "orange",              # Regular button background
        "button_text": "purple",                    # Regular button text
        "button_hover": "cyan",                     # Regular button hover
        "spinbox_border": "green",                  # Spinbox border
        "titlebar_button_background": "turquoise",  # Title bar button background
        "titlebar_button_hover": "navy",            # Title bar button hover
        "close_button_hover": "red",                # Close button hover
    }
}

def get_tool_stylesheets(colors):
    """
    Dynamically finds, imports, and gets the stylesheet for each available tool.
    """
    tool_styles = []
    for tool_id, tool_data in AVAILABLE_TOOLS.items():
        widget_class = tool_data['widget_class']
        try:
            # Find the directory of the tool's widget class file
            class_file_path = inspect.getfile(widget_class)
            class_dir = os.path.dirname(class_file_path)
            
            # The stylesheet is in a '{tool_id}_styles.py' file in the same directory
            style_module_path = os.path.join(class_dir, f'{tool_id}_styles.py')

            if os.path.exists(style_module_path):
                # Dynamically import the module from its file path
                spec = importlib.util.spec_from_file_location(f"tools.{tool_id}.styles", style_module_path)
                style_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(style_module)
                
                # Check if the module has the required function
                if hasattr(style_module, 'get_stylesheet'):
                    # Call the function and append the returned style string
                    style_string = style_module.get_stylesheet(colors)
                    tool_styles.append(style_string)
        except Exception as e:
            # This allows the main app to run even if a tool's style is missing/broken
            print(f"Warning: Could not load stylesheet for '{tool_id}': {e}")
            
    return "\n".join(tool_styles)

def get_stylesheet(theme='dark'):
    """Returns the stylesheet for the application based on the selected theme."""
    colors = COLORS.get(theme, COLORS['dark']) # Default to dark theme if not found
    
    # The main stylesheet string
    main_stylesheet = f"""
        /* Style the custom title bar and the tab bar within it for a unified background.
           Using a descendant selector (CustomTitleBar QTabBar) makes the rule more specific. */
        CustomTitleBar, CustomTitleBar QTabBar {{
            background-color: {colors["title_bar_background"]};
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        }}

        /* Target the main content area specifically using its object name */
        QWidget#main_content {{
            background-color: {colors["widget_background"]};
            border-radius: 20px;
        }}
        
        /* Style for individual tabs within the custom title bar */
        CustomTitleBar QTabBar::tab {{
            background: {colors["title_bar_background"]};
            color: {colors["text_color"]};
            padding: 8px 15px;
            margin-top: 2px; /* Pushes inactive tabs down slightly */
            border: 1px solid {colors["title_bar_background"]};
            border-bottom: none;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}

        /* Style for the currently selected tab within the custom title bar */
        CustomTitleBar QTabBar::tab:selected {{
            background: {colors["tab_selected_background"]};
            color: {colors["tab_selected_text"]};
            margin-top: 2px; /* Aligns active tab with the top */
            padding-bottom: 10px; /* Extends tab slightly to overlap the pane */
        }}

        CustomTitleBar QTabBar::tab:!selected:hover {{
            background: {colors["titlebar_button_hover"]};
        }}

        /* Ensure the close button is visible */
        CustomTitleBar QTabBar::close-button {{
            image: url(close.png); /* A placeholder, ideally use an icon font or a resource file */
            background: transparent;
            subcontrol-position: right;
            subcontrol-origin: padding;
            padding: 2px;
            border-radius: 5px;
        }}
        CustomTitleBar QTabBar::close-button:hover {{
            background: #c0392b;
        }}

        /* Set explicit styles for other widgets instead of a generic QWidget rule */
        QLabel {{
            background-color: transparent; /* Prevent labels from having a solid background */
            color: {colors["label_text"]};
            font-size: 16px;
            padding: 10px;
        }}

        QPushButton {{
            background-color: {colors["button_background"]};
            color: {colors["button_text"]};
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {colors["button_hover"]};
        }}

        QSpinBox {{
            background-color: {colors["widget_background"]};
            color: {colors["label_text"]};
            padding: 5px;
            border: 1px solid {colors["spinbox_border"]};
            border-radius: 5px;
            font-size: 14px;
        }}
        
        QStackedWidget {{
            background-color: {colors["widget_background"]};
        }}

        /* Style the buttons specifically within the CustomTitleBar */
        CustomTitleBar QPushButton {{
            padding: 5px;
            font-size: 12px;
            border-radius: 4px;
            background-color: {colors["titlebar_button_background"]};
            color: {colors["text_color"]};
        }}
         CustomTitleBar QPushButton:hover {{
            background-color: {colors["titlebar_button_hover"]};
        }}
        CustomTitleBar QPushButton#close_button:hover {{
            background-color: {colors["close_button_hover"]};
            color: {colors["text_color"]};
        }}
    """
    
    # Append the dynamically loaded tool-specific styles
    return main_stylesheet + "\n" + get_tool_stylesheets(colors)