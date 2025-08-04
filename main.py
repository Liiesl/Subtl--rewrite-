# main.py

import sys
from PySide6.QtWidgets import ( QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget)
from PySide6.QtCore import Qt
from titlebar import CustomTitleBar, WindowResizer
from tab import TabContainer, TabManager
from styles import get_stylesheet

class SubtitleToolUI(QMainWindow):
    """
    The main window for the Subtitle Manipulation Tool with a Chrome-like UI.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subtitle Manipulator")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        main_widget = QWidget()
        main_widget.setObjectName("main_content")
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # The QStackedWidget will hold the content for each tab page
        self.pages_widget = QStackedWidget()

        # The CustomTitleBar now contains and manages the tab UI container
        self.title_bar = CustomTitleBar(self)

        # The TabManager handles all tab logic, linking the UI to the content
        self.tab_manager = TabManager(self, self.pages_widget, self.title_bar.tab_container)

        # Connect title bar controls to the tab manager's navigation methods
        self.title_bar.back_button.clicked.connect(self.tab_manager.go_back)
        self.title_bar.forward_button.clicked.connect(self.tab_manager.go_forward)

        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.pages_widget)
        
        self.resizer = WindowResizer(self)
        
        self.setStyleSheet(get_stylesheet('dark'))
        
        # Open the initial tab via the manager
        self.tab_manager.open_new_dashboard_tab()

        self.setCentralWidget(main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubtitleToolUI()
    window.show()
    sys.exit(app.exec())