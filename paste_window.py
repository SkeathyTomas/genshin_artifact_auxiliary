'''贴图窗口'''

from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget

import location

class PasteWindow(QWidget):
    def __init__(self):
        super().__init__()
        SCALE = location.get_scale()

        # 设置贴图窗口属性：透明、无边框透明、置顶
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
    
        # 贴图窗口内容
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel('Er!')
        # 字体大小
        font = self.label.font()
        font.setPointSize(14 / SCALE)
        self.label.setFont(font)
        self.label.setFixedSize(40 / SCALE, 40 / SCALE)
        self.label.setAlignment(Qt.AlignCenter)
        # qss = 'border-image: url(paste.png);'
        qss = 'background-color: rgb(255, 255, 255)'
        self.label.setStyleSheet(qss)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 快捷键Ctrl+Z关闭贴图窗口，需焦点在主窗口
        self.shortcut = QShortcut(QKeySequence('Ctrl+Z'), self)
        self.shortcut.activated.connect(self.close)
    
    # 按键关闭/重置对应贴图窗口
    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Z:
    #         print('freshed')
    #         self.hide()
    
    # Ctrl+Z关闭窗口
    def close(self):
        # print('canceled!')
        self.hide()