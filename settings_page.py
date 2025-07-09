'''参数设置页面'''

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal

class SettingsPage(QWidget):
    go_back = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("这是设置页面"))
        self.btn_back = QPushButton("返回主页面")
        self.btn_back.clicked.connect(self.go_back.emit)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)