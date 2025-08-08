# tab.py

# MODIFIED: Added os and QMessageBox for the new direct-opening functionality
import os
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QStackedWidget,
                               QTabBar, QGridLayout, QSizePolicy, QMessageBox)
from PySide6.QtCore import QObject, Qt
import qtawesome as qta

# MODIFIED: AVAILABLE_TOOLS is now needed for the new method
from tool_manager import AVAILABLE_TOOLS
from tools.placeholder_tool.placeholder_tool import PlaceholderTool
from dashboard import DashboardWidget

class DraggableTabBar(QTabBar):
    """
    A custom QTabBar that allows window dragging. It forwards mouse events to
    its parent title bar to handle the window movement.
    """
    def __init__(self, parent_title_bar):
        super().__init__(parent_title_bar)
        self.parent_title_bar = parent_title_bar

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.tabAt(event.position().toPoint()) == -1:
            self.parent_title_bar.mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.parent_title_bar.pressing:
            self.parent_title_bar.mouseMoveEvent(event)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.parent_title_bar.mouseReleaseEvent(event)
        super().mouseReleaseEvent(event)

class TabContainer(QWidget):
    """
    A widget that contains the DraggableTabBar and the 'add tab' button.
    This is the primary UI component for tab management.
    """
    def __init__(self, parent_title_bar):
        super().__init__(parent_title_bar)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.tab_bar = DraggableTabBar(parent_title_bar)
        self.tab_bar.setDocumentMode(True)
        self.tab_bar.setUsesScrollButtons(True)
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.tab_bar.setSizePolicy(size_policy)
        
        layout.addWidget(self.tab_bar)
        
        self.add_tab_button = QPushButton(qta.icon('mdi.plus'), "")
        self.add_tab_button.setFixedSize(30, 30)
        layout.addWidget(self.add_tab_button)

    def update_tab_bar_width(self, available_width):
        """Calculates and sets the maximum width for the tab bar."""
        max_tab_width = max(200, available_width)
        self.tab_bar.setMaximumWidth(max_tab_width)


class TabManager(QObject):
    """
    A non-visual class to manage the logic behind the tab system.
    """
    def __init__(self, main_window, pages_widget, tab_container):
        super().__init__(main_window)
        self.main_window = main_window
        self.pages_widget = pages_widget
        self.tab_container = tab_container
        self.tab_histories = []

        # Connect signals from the TabContainer UI to the manager's logic
        self.tab_container.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_container.tab_bar.currentChanged.connect(self.pages_widget.setCurrentIndex)
        self.tab_container.add_tab_button.clicked.connect(self.open_new_dashboard_tab)

    def go_back(self):
        """Navigates to the previous widget in the current tab's history."""
        current_tab_index = self.tab_container.tab_bar.currentIndex()
        if current_tab_index == -1: return

        history_data = self.tab_histories[current_tab_index]
        if history_data['current_index'] > 0:
            history_data['current_index'] -= 1
            stacked_widget = self.pages_widget.widget(current_tab_index)
            history_item = history_data['history'][history_data['current_index']]
            stacked_widget.setCurrentIndex(history_item['widget_index'])
            self.tab_container.tab_bar.setTabText(current_tab_index, history_item['title'])

    def go_forward(self):
        """Navigates to the next widget in the current tab's history."""
        current_tab_index = self.tab_container.tab_bar.currentIndex()
        if current_tab_index == -1: return

        history_data = self.tab_histories[current_tab_index]
        if history_data['current_index'] < len(history_data['history']) - 1:
            history_data['current_index'] += 1
            stacked_widget = self.pages_widget.widget(current_tab_index)
            history_item = history_data['history'][history_data['current_index']]
            stacked_widget.setCurrentIndex(history_item['widget_index'])
            self.tab_container.tab_bar.setTabText(current_tab_index, history_item['title'])

    def create_dashboard(self):
        """Creates the dashboard widget and connects its tool selection signal."""
        dashboard_widget = DashboardWidget()
        # When a tool is selected in the dashboard, open it.
        dashboard_widget.tool_selected.connect(self.open_tool)
        return dashboard_widget

    def open_tool(self, tool_key):
        """Adds the selected tool to the current tab's content stack."""
        current_tab_index = self.tab_container.tab_bar.currentIndex()
        if current_tab_index == -1: return

        if tool_key not in AVAILABLE_TOOLS:
            print(f"Error: Tool '{tool_key}' not found in tool manager.")
            return

        tool_info = AVAILABLE_TOOLS[tool_key]
        ToolWidgetClass = tool_info['widget_class']
        tool_display_name = tool_info['display_name']
        
        tool_widget = ToolWidgetClass(tool_display_name) if issubclass(ToolWidgetClass, PlaceholderTool) else ToolWidgetClass()

        stacked_widget = self.pages_widget.widget(current_tab_index)
        tool_widget_index = stacked_widget.addWidget(tool_widget)

        history_data = self.tab_histories[current_tab_index]
        current_pos = history_data['current_index']

        # Clear forward history when a new tool is opened
        history_data['history'] = history_data['history'][:current_pos + 1]
        history_data['history'].append({'widget_index': tool_widget_index, 'title': tool_display_name})
        history_data['current_index'] += 1

        stacked_widget.setCurrentWidget(tool_widget)
        self.tab_container.tab_bar.setTabText(current_tab_index, tool_display_name)

    def open_new_dashboard_tab(self):
        """Opens a new tab with the dashboard view."""
        new_dashboard = self.create_dashboard()
        
        # Each tab needs its own QStackedWidget to manage its history
        stacked_widget = QStackedWidget()
        dashboard_index_in_stack = stacked_widget.addWidget(new_dashboard)

        # Initialize the history for this new tab
        self.tab_histories.append({
            'history': [{'widget_index': dashboard_index_in_stack, 'title': 'Dashboard'}],
            'current_index': 0
        })
        
        # Add the tab's QStackedWidget to the main pages widget
        page_index = self.pages_widget.addWidget(stacked_widget)
        
        # Add a tab to the UI and make it current
        new_tab_index = self.tab_container.tab_bar.addTab("Dashboard")
        self.tab_container.tab_bar.setTabsClosable(True)
        self.tab_container.tab_bar.setCurrentIndex(new_tab_index)
        self.pages_widget.setCurrentIndex(page_index)


    # NEW: This method handles opening a file directly into a chosen tool
    def open_tool_directly(self, tool_id, file_path):
        """
        Creates a new tab for a specific tool and instructs it to load a file.
        This bypasses the dashboard and is used for file-opening startups.
        """
        if tool_id not in AVAILABLE_TOOLS:
            QMessageBox.critical(self.main_window, "Tool Not Found",
                                 f"The tool '{tool_id}' could not be found.")
            self.open_new_dashboard_tab()
            return

        tool_info = AVAILABLE_TOOLS[tool_id]
        ToolWidgetClass = tool_info['widget_class']
        tool_display_name = tool_info['display_name']
        tool_widget = ToolWidgetClass(tool_display_name) if issubclass(ToolWidgetClass, PlaceholderTool) else ToolWidgetClass()

        # Convention: Check for a method to load the file on startup
        if hasattr(tool_widget, 'load_file_on_startup'):
            try:
                tool_widget.load_file_on_startup(file_path)
            except Exception as e:
                QMessageBox.critical(self.main_window, "File Load Error",
                                     f"Failed to load '{os.path.basename(file_path)}' in {tool_display_name}.\n\nError: {e}")
                self.open_new_dashboard_tab()
                return
        else:
            QMessageBox.warning(self.main_window, "Tool Incompatible",
                                f"The tool '{tool_display_name}' cannot open files directly.")
            self.open_new_dashboard_tab()
            return

        # Create a new tab for this tool (logic adapted from open_new_dashboard_tab)
        stacked_widget = QStackedWidget()
        tool_widget_index = stacked_widget.addWidget(tool_widget)
        self.tab_histories.append({
            'history': [{'widget_index': tool_widget_index, 'title': tool_display_name}],
            'current_index': 0
        })
        page_index = self.pages_widget.addWidget(stacked_widget)
        new_tab_index = self.tab_container.tab_bar.addTab(tool_display_name)
        self.tab_container.tab_bar.setTabsClosable(True)
        self.tab_container.tab_bar.setCurrentIndex(new_tab_index)
        self.pages_widget.setCurrentIndex(page_index)


    def close_tab(self, index):
        """Closes the tab at the given index, ensuring at least one tab remains."""
        if self.tab_container.tab_bar.count() <= 1: return

        widget = self.pages_widget.widget(index)
        self.pages_widget.removeWidget(widget)
        if widget is not None:
            # Ensure the widget and its children are deleted to free memory
            widget.deleteLater()
            
        self.tab_container.tab_bar.removeTab(index)
        # Remove the corresponding history for the closed tab
        del self.tab_histories[index]