# tab.py

from PySide6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QStackedWidget,
                               QTabBar, QGridLayout, QSizePolicy)
from PySide6.QtCore import QObject, Qt
import qtawesome as qta

from tool_manager import AVAILABLE_TOOLS
from tools.placeholder_tool.placeholder_tool import PlaceholderTool

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
        """Creates the dashboard widget with a grid of available tools."""
        dashboard_widget = QWidget()
        layout = QGridLayout(dashboard_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        row, col = 0, 0
        for tool_key, tool_info in AVAILABLE_TOOLS.items():
            button = QPushButton(tool_info['display_name'])
            button.clicked.connect(lambda checked, key=tool_key: self.open_tool(key))
            layout.addWidget(button, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
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

        history_data['history'] = history_data['history'][:current_pos + 1]
        history_data['history'].append({'widget_index': tool_widget_index, 'title': tool_display_name})
        history_data['current_index'] += 1

        stacked_widget.setCurrentWidget(tool_widget)
        self.tab_container.tab_bar.setTabText(current_tab_index, tool_display_name)

    def open_new_dashboard_tab(self):
        """Opens a new tab with the dashboard view."""
        new_dashboard = self.create_dashboard()
        stacked_widget = QStackedWidget()
        dashboard_index_in_stack = stacked_widget.addWidget(new_dashboard)

        self.tab_histories.append({
            'history': [{'widget_index': dashboard_index_in_stack, 'title': 'Dashboard'}],
            'current_index': 0
        })
        
        self.pages_widget.addWidget(stacked_widget)
        new_tab_index = self.tab_container.tab_bar.addTab("Dashboard")
        self.tab_container.tab_bar.setCurrentIndex(new_tab_index)
        self.tab_container.tab_bar.setTabsClosable(True)

    def close_tab(self, index):
        """Closes the tab at the given index, ensuring at least one tab remains."""
        if self.tab_container.tab_bar.count() <= 1: return

        widget = self.pages_widget.widget(index)
        self.pages_widget.removeWidget(widget)
        if widget is not None:
            widget.deleteLater()
            
        self.tab_container.tab_bar.removeTab(index)
        del self.tab_histories[index]
        self.tab_container.tab_bar.setTabIcon(index, qta.icon('mdi.close'))