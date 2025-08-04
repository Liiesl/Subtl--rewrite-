# titlebar.py

from PySide6.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QStyle, QStyleOption)
from PySide6.QtCore import Qt, QObject, QEvent, QRect, QPoint
from PySide6.QtGui import QCursor, QPainter
import qtawesome as qta
from tab import TabContainer

class CustomTitleBar(QWidget):
    """
    Custom title bar to hold the tab container and window controls.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 0)
        layout.setSpacing(5)

        # Navigation buttons are now on the left
        self.back_button = QPushButton(qta.icon('mdi.chevron-left'), "")
        self.forward_button = QPushButton(qta.icon('mdi.chevron-right'), "")
        self.back_button.setFixedSize(30, 30)
        self.forward_button.setFixedSize(30, 30)
        layout.addWidget(self.back_button)
        layout.addWidget(self.forward_button)

        # The TabContainer holds the tab bar and add button
        self.tab_container = TabContainer(self)
        layout.addWidget(self.tab_container)
        
        layout.addStretch(1)
        
        # Window control buttons
        self.minimize_button = QPushButton(qta.icon('mdi.window-minimize'), "")
        self.maximize_button = QPushButton()
        self.close_button = QPushButton(qta.icon('mdi.close'), "")
        self.close_button.setObjectName("close_button")
        
        for btn in [self.minimize_button, self.maximize_button, self.close_button]:
            btn.setFixedSize(30, 30)
        
        self.minimize_button.clicked.connect(parent.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(parent.close)
        
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)
        
        self.start_pos = None
        self.pressing = False

        self.update_maximize_icon()

    def paintEvent(self, event):
        option = QStyleOption()
        option.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, option, painter, self)

    def update_tab_container_width(self):
        """Calculate available width for the tab container."""
        button_width = 30
        spacing = 5
        # Width of back, forward, min, max, close buttons and spacings
        fixed_elements_width = (5 * button_width) + (6 * spacing) + 100
        available_width = self.width() - fixed_elements_width
        self.tab_container.update_tab_bar_width(available_width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_tab_container_width()
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
        RESIZE_MARGIN = 5
        if event.button() == Qt.MouseButton.LeftButton:
            if self.parent.isMaximized() or event.position().y() >= RESIZE_MARGIN:
                self.start_pos = event.globalPosition().toPoint()
                self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            if self.parent.isMaximized():
                self.parent.showNormal()
                self.update_maximize_icon()
                self.parent.move(event.globalPosition().toPoint() - self.parent.rect().center())
                self.start_pos = event.globalPosition().toPoint()
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
    from the window borders. (This class remains unchanged).
    """
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.margin = 5  # The size of the resize handles in pixels
        self.resizing = False
        self.resize_edges = {}
        self.start_pos = None
        self.start_geo = None

        # Install the event filter on the window
        self.window.setMouseTracking(True)
        self.window.installEventFilter(self)

    def eventFilter(self, obj, event):
        # Ensure the event is for the main window and is a relevant mouse event
        if obj is not self.window or event.type() not in [QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease, QEvent.Type.HoverMove, QEvent.Type.WindowStateChange]:
            return super().eventFilter(obj, event)

        # Handle window state changes to update the maximize icon
        if event.type() == QEvent.Type.WindowStateChange:
            try:
                title_bar = self.window.findChild(CustomTitleBar)
                if title_bar:
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
        """Check which edge(s) the mouse is on and store them."""
        rect = self.window.rect()
        self.resize_edges['top'] = pos.y() < self.margin
        self.resize_edges['bottom'] = pos.y() > rect.bottom() - self.margin
        self.resize_edges['left'] = pos.x() < self.margin
        self.resize_edges['right'] = pos.x() > rect.right() - self.margin
        return any(self.resize_edges.values())

    def _update_cursor(self, pos):
        """Update the cursor icon based on the mouse position over the edges."""
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
        """Calculate the new window geometry and apply it, respecting minimum size."""
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