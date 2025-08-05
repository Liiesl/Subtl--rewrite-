# titlebar.py

from PySide6.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QStyle,
                               QStyleOption, QMenu, QLabel, QTabBar) # QTabBar imported
from PySide6.QtCore import Qt, QObject, QEvent, QRect, QPoint, Signal
from PySide6.QtGui import QCursor, QPainter, QAction
import qtawesome as qta
from chrome.tab import TabContainer

class CustomTitleBar(QWidget):
    """
    Custom title bar that can be configured for a main window, dialog, or settings window.
    """
    settings_requested = Signal()

    def __init__(self, parent, bar_type='main_window', tabs_config=None):
        """
        Initializes the title bar.

        Args:
            parent: The parent widget.
            bar_type (str): 'main_window', 'dialog', or 'settings' to determine the layout.
            tabs_config (list, optional): A list of strings for tab names, used when bar_type is 'settings'.
        """
        super().__init__(parent)
        self.parent = parent
        self.resizer = None # Will hold the resizer instance

        # Install resizer by default for non-dialog types
        if bar_type != 'dialog':
            self.set_resizer(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 0) # there should be no gap at the bottom
        layout.setSpacing(5)

        # --- Common Elements ---
        self.start_pos = None
        self.pressing = False

        # --- Layout based on bar_type ---
        if bar_type == 'main_window':
            self._setup_main_window_bar(layout)
        elif bar_type == 'dialog':
            self._setup_dialog_bar(layout)
        elif bar_type == 'settings':
            self._setup_settings_bar(layout, tabs_config)
        else:
            # Default to a minimal bar if type is unknown
            self._setup_dialog_bar(layout)

        # Set object name for styling
        self.setObjectName("custom_title_bar")

    def _setup_main_window_bar(self, layout):
        """Sets up the title bar for the main application window."""
        self.back_button = QPushButton(qta.icon('mdi.chevron-left'), "")
        self.forward_button = QPushButton(qta.icon('mdi.chevron-right'), "")
        self.back_button.setFixedSize(30, 30)
        self.forward_button.setFixedSize(30, 30)
        layout.addWidget(self.back_button)
        layout.addWidget(self.forward_button)

        self.tab_container = TabContainer(self)
        layout.addWidget(self.tab_container)

        layout.addStretch(1)

        self.menu_button = QPushButton(qta.icon('mdi.dots-vertical'), "")
        self.menu_button.setFixedSize(30, 30)
        self.menu_button.clicked.connect(self.show_options_menu)
        layout.addWidget(self.menu_button)

        self.minimize_button = QPushButton(qta.icon('mdi.window-minimize'), "")
        self.maximize_button = QPushButton()
        self.close_button = QPushButton(qta.icon('mdi.close'), "")
        self.close_button.setObjectName("close_button")

        for btn in [self.minimize_button, self.maximize_button, self.close_button]:
            btn.setFixedSize(30, 30)

        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(self.parent.close)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

        self.update_maximize_icon()

    def _setup_dialog_bar(self, layout):
        """Sets up a simplified title bar for dialog windows."""
        self.title_label = QLabel(self.parent.windowTitle())
        self.title_label.setObjectName("title_label") # For specific styling

        layout.addWidget(self.title_label)
        layout.addStretch(1)

        # Dialogs typically only need minimize and close
        self.minimize_button = QPushButton(qta.icon('mdi.window-minimize'), "")
        self.close_button = QPushButton(qta.icon('mdi.close'), "")
        self.close_button.setObjectName("close_button")

        for btn in [self.minimize_button, self.close_button]:
            btn.setFixedSize(30, 30)

        self.minimize_button.clicked.connect(self.parent.showMinimized)
        # For QDialog, reject() is often preferred over close()
        self.close_button.clicked.connect(self.parent.reject)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.close_button)

    def _setup_settings_bar(self, layout, tabs_config):
        """Sets up a title bar with fixed tabs for settings dialogs."""
        self.settings_tab_bar = QTabBar()
        self.settings_tab_bar.setTabsClosable(False)
        self.settings_tab_bar.setObjectName("settings_tab_bar")

        if tabs_config:
            for tab_name in tabs_config:
                self.settings_tab_bar.addTab(tab_name)

        layout.addWidget(self.settings_tab_bar, 1) # Add tab bar with stretch factor
        layout.addStretch(0)

        self.minimize_button = QPushButton(qta.icon('mdi.window-minimize'), "")
        self.close_button = QPushButton(qta.icon('mdi.close'), "")
        self.close_button.setObjectName("close_button")

        for btn in [self.minimize_button, self.close_button]:
            btn.setFixedSize(30, 30)

        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.close_button.clicked.connect(self.parent.reject)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.close_button)

    def set_resizer(self, install: bool):
        """
        Installs or uninstalls the window resizer.

        Args:
            install (bool): True to install the resizer, False to uninstall.
        """
        top_level_window = self.window()
        if not top_level_window:
            return # Cannot do anything if not attached to a window

        if install:
            if self.resizer is None:
                self.resizer = WindowResizer(top_level_window)
        else:
            if self.resizer is not None:
                self.resizer.uninstall()
                self.resizer = None

    def show_options_menu(self):
        """Creates and displays the options context menu."""
        context_menu = QMenu(self)
        settings_action = QAction(qta.icon('mdi.cog'), "Settings", self)
        settings_action.triggered.connect(self.settings_requested.emit)
        help_action = QAction(qta.icon('mdi.help-circle-outline'), "Help", self)
        help_action.triggered.connect(lambda: print("Help placeholder"))
        changelog_action = QAction(qta.icon('mdi.history'), "Changelog", self)
        changelog_action.triggered.connect(lambda: print("Changelog placeholder"))
        context_menu.addAction(settings_action)
        context_menu.addAction(help_action)
        context_menu.addAction(changelog_action)
        button_pos = self.menu_button.mapToGlobal(QPoint(0, self.menu_button.height()))
        context_menu.exec(button_pos)

    def paintEvent(self, event):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, option, painter, self)

    def update_tab_container_width(self):
        """Calculate available width for the tab container (main window only)."""
        if hasattr(self, 'tab_container'):
            button_width = 30
            spacing = 5
            fixed_elements_width = (6 * button_width) + (7 * spacing) + 100
            available_width = self.width() - fixed_elements_width
            self.tab_container.update_tab_bar_width(available_width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'tab_container'):
            self.update_tab_container_width()
        if hasattr(self, 'maximize_button'):
            self.update_maximize_icon()

    def update_maximize_icon(self):
        if self.parent.isMaximized():
            self.maximize_button.setIcon(qta.icon('mdi.window-restore'))
        else:
            self.maximize_button.setIcon(qta.icon('mdi.window-maximize'))

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
        self.update_maximize_icon()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Don't start dragging if a button on the title bar is clicked
            child = self.childAt(event.position().toPoint())
            if not isinstance(child, (QPushButton, QTabBar)):
                self.start_pos = event.globalPosition().toPoint()
                self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            if hasattr(self, 'maximize_button') and self.parent.isMaximized():
                self.parent.showNormal()
                self.update_maximize_icon()
                # Center the window on the cursor
                self.parent.move(event.globalPosition().toPoint() - self.rect().center())
                self.start_pos = event.globalPosition().toPoint() # Reset start position
                return

            delta = event.globalPosition().toPoint() - self.start_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = False
            self.start_pos = None

class WindowResizer(QObject):
    """
    An event filter that captures mouse events on the main window to allow resizing
    from the window borders.
    """
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.margin = 5
        self.resizing = False
        self.resize_edges = {}
        self.start_pos = None
        self.start_geo = None
        self.window.setMouseTracking(True)
        self.window.installEventFilter(self)

    def uninstall(self):
        """Removes the event filter and cleans up."""
        if self.window:
            self.window.removeEventFilter(self)
            # Only turn off mouse tracking if no other part of the app needs it
            self.window.setMouseTracking(False)
            self.window.unsetCursor()
        self.window = None # Break reference to allow garbage collection

    def eventFilter(self, obj, event):
        # Add a check to ensure 'window' attribute exists and is not None
        # to prevent errors during object destruction or after uninstallation.
        if not hasattr(self, 'window') or not self.window:
            return super().eventFilter(obj, event)

        if obj is not self.window or event.type() not in [QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease, QEvent.Type.HoverMove, QEvent.Type.WindowStateChange]:
            return super().eventFilter(obj, event)

        if event.type() == QEvent.Type.WindowStateChange:
            try:
                title_bar = self.window.findChild(CustomTitleBar)
                if title_bar and hasattr(title_bar, 'update_maximize_icon'):
                    title_bar.update_maximize_icon()
            except AttributeError:
                pass
            return super().eventFilter(obj, event)

        global_pos = QCursor.pos()
        pos_in_window = self.window.mapFromGlobal(global_pos)

        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            if not self.window.isMaximized() and self._check_edges(pos_in_window):
                self.resizing = True
                self.start_pos = global_pos
                self.start_geo = self.window.geometry()
                return True

        elif event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            if self.resizing:
                self.resizing = False
                self.resize_edges = {}
                return True

        elif event.type() == QEvent.Type.MouseMove or event.type() == QEvent.Type.HoverMove:
            if self.resizing:
                self._resize_window(global_pos)
                return True
            else:
                self._update_cursor(pos_in_window)

        return super().eventFilter(obj, event)

    def _check_edges(self, pos):
        rect = self.window.rect()
        self.resize_edges['top'] = pos.y() < self.margin
        self.resize_edges['bottom'] = pos.y() > rect.bottom() - self.margin
        self.resize_edges['left'] = pos.x() < self.margin
        self.resize_edges['right'] = pos.x() > rect.right() - self.margin
        return any(self.resize_edges.values())

    def _update_cursor(self, pos):
        if self.window.isMaximized() or self.resizing:
            self.window.unsetCursor()
            return

        rect = self.window.rect()
        on_top = pos.y() < self.margin
        on_bottom = pos.y() > rect.bottom() - self.margin
        on_left = pos.x() < self.margin
        on_right = pos.x() > rect.right() - self.margin

        if (on_top and on_left) or (on_bottom and on_right):
            self.window.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif (on_top and on_right) or (on_bottom and on_left):
            self.window.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif on_top or on_bottom:
            self.window.setCursor(Qt.CursorShape.SizeVerCursor)
        elif on_left or on_right:
            self.window.setCursor(Qt.CursorShape.SizeHorCursor)
        else:
            self.window.unsetCursor()

    def _resize_window(self, global_pos):
        delta = global_pos - self.start_pos
        start_rect = self.start_geo
        min_size = self.window.minimumSize()
        new_rect = QRect(start_rect)

        if self.resize_edges.get('left'):
            new_left = start_rect.left() + delta.x()
            if start_rect.width() - delta.x() < min_size.width():
                new_left = start_rect.right() - min_size.width()
            new_rect.setLeft(new_left)

        if self.resize_edges.get('right'):
            new_right = start_rect.right() + delta.x()
            if start_rect.width() + delta.x() < min_size.width():
                new_right = start_rect.left() + min_size.width()
            new_rect.setRight(new_right)

        if self.resize_edges.get('top'):
            new_top = start_rect.top() + delta.y()
            if start_rect.height() - delta.y() < min_size.height():
                new_top = start_rect.bottom() - min_size.height()
            new_rect.setTop(new_top)

        if self.resize_edges.get('bottom'):
            new_bottom = start_rect.bottom() + delta.y()
            if start_rect.height() + delta.y() < min_size.height():
                new_bottom = start_rect.top() + min_size.height()
            new_rect.setBottom(new_bottom)

        self.window.setGeometry(new_rect)