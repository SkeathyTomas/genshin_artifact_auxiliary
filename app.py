'''主窗口'''

import sys, os
import qdarktheme
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from main_page import MainPage
from settings_page import SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'src/keqing.ico')))
        self.setWindowTitle("刻晴办公桌")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(0, 0)

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.setContentsMargins(0, 0, 0, 0)

        self.main_page = MainPage()
        self.settings_page = SettingsPage()

        self.stacked_layout.addWidget(self.main_page)
        self.stacked_layout.addWidget(self.settings_page)

        self.main_page.open_settings.connect(self.show_settings)
        self.settings_page.go_back.connect(self.show_main)

        central_widget = QWidget()
        central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(central_widget)

    def show_settings(self):
        self.main_page.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.settings_page.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.stacked_layout.setCurrentWidget(self.settings_page)
        self.adjustSize()

    def show_main(self):
        self.main_page.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.settings_page.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.stacked_layout.setCurrentWidget(self.main_page)
        self.adjustSize()

def main():

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()