import sys

from random import randint
from pynput import mouse, keyboard

from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QWidget,
    QVBoxLayout,
)

import img_process

# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("My App")
        self.move(0, 0)

        # 预先设定好贴图窗口组
        self.pastes = []
        for i in range(28):
            window = PasteWindow()
            self.pastes.append(window)

        # 快捷键Ctrl+F5关闭所有贴图窗口，需焦点在主窗口
        self.shortcut = QShortcut(QKeySequence('Ctrl+F5'), self)
        self.shortcut.activated.connect(self.reset)

        # 主窗口内容
        self.button = QPushButton('Press me!')
        self.setCentralWidget(self.button)
        self.button.clicked.connect(self.open_new_window)

        # 外部鼠标事件启动识别和贴图弹窗
        self.manager = OutsideMouseManager()
        self.manager.released.connect(self.open_new_window)

    # 启动贴图弹窗
    def open_new_window(self, x, y):
        # 贴图坐标组
        position = [(400, 320), (550, 320), (700, 320), (850, 320),
                    (400, 500), (550, 500), (700, 500), (850, 500),
                    (400, 680), (550, 680), (700, 680), (850, 680),
                    (400, 860), (550, 860), (700, 860), (850, 860),
                    (400, 1040), (550, 1040), (700, 1040), (850, 1040),
                    (400, 1220), (550, 1220), (700, 1220), (850, 1220),
                    (400, 1440), (550, 1440), (700, 1440), (850, 1440)]
        xarray = [(295, 429), (446, 580), (597, 731), (748, 882)]
        yarray = [(188, 350), (368, 530), (548, 710), (728, 890)]

        # 根据鼠标事件定位贴图，i列j行
        for i in range(4):
            for j in range(4):
                if x >= xarray[i][0] and x <= xarray[i][1] and y >= yarray[j][0] and y <= yarray[j][1]:
                    id = j * 4 + i
                    # 判断贴图是否存在，存在则不更新，不在则更新
                    if self.pastes[id].isVisible():
                        break
                    else:
                        print('detected')
                        try:
                            score = img_process.main()
                            self.pastes[id].label.setText(str(score))
                        except:
                            print('图像识别有误！')
                        self.pastes[id].show()
                        self.pastes[id].move(position[id][0] // SCALE, position[id][1] // SCALE)
                        break

    # 快捷键Ctrl+F5重置贴图窗口
    def reset(self):
        print('reset')
        for item in self.pastes:
            item.hide()
    
    # 主窗口关闭则所有贴图窗口也关闭
    def closeEvent(self, event):
        for item in self.pastes:
            item.close()
    
    # 全局快捷键
    def hotkey(self):
        def on_activate():
            # print('global reset!')
            self.reset()
        
        def for_canonical(f):
            return lambda k: f(l.canonical(k))
        
        hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+y'), on_activate)
        l = keyboard.Listener(
            on_press = for_canonical(hotkey.press),
            on_release = for_canonical(hotkey.release))
        l.start()

# 新增贴图窗口
class PasteWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置贴图窗口属性：透明、无边框透明、置顶
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    
        # 贴图窗口内容
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel('E!')
        # 字体大小
        font = self.label.font()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setFixedSize(48 // SCALE, 48 // SCALE)
        self.label.setAlignment(Qt.AlignCenter)
        # qss = 'border-image: url(paste.png);'
        qss = 'background-color: rgb(255, 255, 255)'
        self.label.setStyleSheet(qss)
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    # 按键关闭/重置对应贴图窗口
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            print('freshed')
            self.hide()

# 外部/系统级鼠标事件处理
class OutsideMouseManager(QObject):
    released = Signal(int, int)
    def __init__(self, parent = None):
        super().__init__(parent)
        self._listener = mouse.Listener(on_click = self._handle_click)
        self._listener.start()
    
    def _handle_click(self, x, y, button, pressed):
        if button == mouse.Button.right and pressed:
            self.released.emit(x, y)

def main():
    # 手动解决一些分辨率缩放问题
    global SCALE
    SCALE = 2

    # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.hotkey()

    app.exec()

if __name__ == '__main__':
    main()