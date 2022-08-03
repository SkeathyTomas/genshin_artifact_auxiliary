import sys

from random import randint
from pynput import keyboard

from PySide6.QtCore import Qt
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

# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("My App")
        self.move(0, 0)

        # 快捷键Shift+F5关闭所有贴图窗口，需焦点在主窗口
        self.shortcut = QShortcut(QKeySequence('Shift+F5'), self)
        self.shortcut.activated.connect(self.reset)

        # 主窗口内容
        self.button = QPushButton('Press me!')
        self.setCentralWidget(self.button)

        # 蒙版窗口
        self.window_all_screen = AllScreenWindow()
        self.window_all_screen.showMaximized()

    # 快捷键Shift+F5重置贴图窗口
    def reset(self):
        print('reset')
        for item in self.window_all_screen.pastes:
            item.hide()
    
    # # 快捷键CTRL启动蒙版窗口
    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Control:
    #         print('start')
    #         self.window_all_screen.showMaximized()
    
    # 主窗口关闭则所有贴图窗口也关闭
    def closeEvent(self, event):
        for item in self.window_all_screen.pastes:
            item.close()
        self.window_all_screen.close()

# 蒙版窗口
class AllScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 预先设定好贴图窗口组
        self.pastes = []
        for i in range(28):
            window = PasteWindow()
            self.pastes.append(window)

        # 提示文案、字体、样式等内容
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel('right click!')
        self.label.setAlignment(Qt.AlignCenter)
        font = self.label.font()
        font.setPointSize(30)
        self.label.setFont(font)
        qss = 'background-color: rgba(0, 0, 0, 100);'
        self.label.setStyleSheet(qss)
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    # 右键点击事件启动识别、贴图窗口
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            position = event.globalPosition()
            self.show_paste_window(position.x(), position.y())

    # 贴图窗口坐标、覆盖检测逻辑
    def show_paste_window(self, x, y):
        # 贴图坐标组
        position = [(400, 320), (550, 320), (700, 320), (850, 320),
                    (400, 500), (550, 500), (700, 500), (850, 500),
                    (400, 680), (550, 680), (700, 680), (850, 680),
                    (400, 860), (550, 860), (700, 860), (850, 860)]
        xarray = [(295, 429), (446, 580), (597, 731), (748, 882)]
        yarray = [(188, 350), (368, 530), (548, 710), (728, 890)]

        # 根据鼠标事件定位贴图，i列j行
        for i in range(4):
            for j in range(4):
                if x >= xarray[i][0] // SCALE and x <= xarray[i][1] // SCALE and y >= yarray[j][0] // SCALE and y <= yarray[j][1] // SCALE:
                    id = j * 4 + i
                    # 判断贴图是否存在，存在则不更新，不在则更新
                    if self.pastes[id].isVisible():
                        break
                    else:
                        # self.hide()
                        print('detected')
                        print(x, y)
                        self.pastes[id].show()
                        self.pastes[id].move(position[id][0] // SCALE, position[id][1] // SCALE)
                        break

# 贴图窗口
class PasteWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置贴图窗口属性：透明、无边框透明、置顶
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # 贴图窗口内容
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel("%d" % randint(0, 40))
        self.label.setFixedSize(32, 32)
        self.label.setAlignment(Qt.AlignCenter)
        qss = 'background-color: rgb(255, 255, 255);'
        self.label.setStyleSheet(qss)
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    # 按键F5关闭/重置对应贴图窗口
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            print('freshed')
            self.hide()

def main():
    # 手动解决一些分辨率缩放问题
    global SCALE
    SCALE = 1.25

    # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # 全局热键
    # def on_activate():
    #     print('<ctrl> pressed')
    #     window.window_all_screen.showMaximized()
        
    # with keyboard.GlobalHotKeys({'<ctrl>': on_activate}) as h:
    #     h.join()

    app.exec()

if __name__ == '__main__':
    main()