import sys, os
import win32con, win32api, win32gui, win32print
from pynput import keyboard

import img_process
from extention import OutsideMouseManager, ExtendedComboBox

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QKeySequence, QShortcut, QIcon, QPixmap, QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QGridLayout
)

# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'src/keqing.ico')))
        self.setWindowTitle("刻晴办公桌")
        self.move(0, 0)
        self.character = ''

        # 选择框
        self.combobox = ExtendedComboBox()
        self.combobox.currentTextChanged.connect(self.current_text_changed)
        self.combobox.addItem('--请选择角色--')

        # 风
        self.combobox.addItem('鹿野院平藏')
        self.combobox.addItem('旅行者-风')
        self.combobox.addItem('枫原万叶')
        self.combobox.addItem('温迪')
        self.combobox.addItem('琴')
        self.combobox.addItem('魈')
        self.combobox.addItem('早柚')
        self.combobox.addItem('砂糖')

        # 火
        self.combobox.addItem('托马')
        self.combobox.addItem('胡桃')
        self.combobox.addItem('宵宫')
        self.combobox.addItem('可莉')
        self.combobox.addItem('迪卢克')
        self.combobox.addItem('班尼特')
        self.combobox.addItem('安柏')
        self.combobox.addItem('香菱')
        self.combobox.addItem('辛焱')
        self.combobox.addItem('烟绯')

        # 水
        self.combobox.addItem('夜兰')
        self.combobox.addItem('神里绫人')
        self.combobox.addItem('达达利亚')
        self.combobox.addItem('珊瑚宫心海')
        self.combobox.addItem('莫娜')
        self.combobox.addItem('行秋')
        self.combobox.addItem('芭芭拉')

        # 冰
        self.combobox.addItem('申鹤')
        self.combobox.addItem('优菈')
        self.combobox.addItem('埃洛伊')
        self.combobox.addItem('神里绫华')
        self.combobox.addItem('七七')
        self.combobox.addItem('甘雨')
        self.combobox.addItem('迪奥娜')
        self.combobox.addItem('重云')
        self.combobox.addItem('罗莎莉亚')
        self.combobox.addItem('凯亚')

        # 雷
        self.combobox.addItem('九岐忍')
        self.combobox.addItem('旅行者-雷')
        self.combobox.addItem('八重神子')
        self.combobox.addItem('雷电将军')
        self.combobox.addItem('刻晴')
        self.combobox.addItem('九条裟罗')
        self.combobox.addItem('菲谢尔')
        self.combobox.addItem('丽莎')
        self.combobox.addItem('雷泽')
        self.combobox.addItem('北斗')

        # 岩
        self.combobox.addItem('旅行者-岩')
        self.combobox.addItem('云堇')
        self.combobox.addItem('荒泷一斗')
        self.combobox.addItem('五郎')
        self.combobox.addItem('阿贝多')
        self.combobox.addItem('钟离')
        self.combobox.addItem('凝光')
        self.combobox.addItem('诺艾尔')

        # 草

        # 图标
        self.label = QLabel()
        self.label.setFixedSize(16, 16)
        pixmap = QPixmap('src/GitHub.png')
        pixmap = pixmap.scaled(16, 16)
        self.label.setPixmap(pixmap)
        self.label.setCursor(Qt.PointingHandCursor)
        self.label.mousePressEvent = self.open_github

        # layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.combobox, 0, 0)
        self.layout.addWidget(self.label, 1, 0, Qt.AlignRight | Qt.AlignBottom)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)        

        # 预先设定好贴图窗口组
        self.pastes = []
        for i in range(row * col):
            window = PasteWindow()
            self.pastes.append(window)

        # 快捷键Ctrl+Z关闭所有贴图窗口，需焦点在主窗口
        self.shortcut = QShortcut(QKeySequence('Ctrl+Z'), self)
        self.shortcut.activated.connect(self.reset)

        # 外部鼠标事件启动识别和贴图弹窗
        self.manager = OutsideMouseManager()
        self.manager.released.connect(self.open_new_window)

    # 选择框事件
    def current_text_changed(self, s):
        self.character = s

    # 打开外部链接
    def open_github(self, event):
        QDesktopServices.openUrl(QUrl('https://github.com/SkeathyTomas/genshin_artifact_auxiliary'))

    # 启动贴图弹窗
    def open_new_window(self, x, y):
        # 根据鼠标事件定位贴图
        for i in range(row):
            if x >= xarray[i][0] and x <= xarray[i][1]:
                for j in range(col):
                    if y >= yarray[j][0] and y <= yarray[j][1]:
                        id = j * row + i
                        # 判断贴图是否存在，存在则不更新，不在则更新
                        if self.pastes[id].isVisible():
                            break
                        else:
                            print('detected')
                            score = img_process.main(self.character, x_grab, y_grab, w_grab, h_grab)
                            self.pastes[id].label.setText(str(score))
                            self.pastes[id].show()
                            self.pastes[id].move(position[id][0] / SCALE, position[id][1] / SCALE)
                            break
                break

    # 快捷键Ctrl+Z重置贴图窗口
    def reset(self):
        for item in self.pastes:
            item.hide()
    
    # 主窗口关闭则所有贴图窗口也关闭
    def closeEvent(self, event):
        for item in self.pastes:
            item.close()
    
    # 全局快捷键Ctrl+Z重置贴图窗口
    def hotkey(self):
        def on_activate():
            print('reset!')
            self.reset()
        
        def for_canonical(f):
            return lambda k: f(l.canonical(k))
        
        hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+z'), on_activate)
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
        self.label = QLabel('Er!')
        # 字体大小
        font = self.label.font()
        font.setPointSize(14 / SCALE)
        self.label.setFont(font)
        self.label.setFixedSize(36 / SCALE, 36 / SCALE)
        self.label.setAlignment(Qt.AlignCenter)
        # qss = 'border-image: url(paste.png);'
        qss = 'background-color: rgb(255, 255, 255)'
        self.label.setStyleSheet(qss)
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    # 按键关闭/重置对应贴图窗口
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Z:
            print('freshed')
            self.hide()

def main():
    # 手动解决一些不同缩放情况下窗口定位的问题
    # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    global SCALE
    hDC = win32gui.GetDC(0)
    width_r = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    height_r = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    width_s = win32api.GetSystemMetrics(0)
    print(width_r, height_r)
    SCALE = width_r / width_s

    # 分辨率适配
    global x_grab, y_grab, w_grab, h_grab # 截图x, y, w, h
    global row, col # 圣遗物行列数
    # 2560*1600
    if width_r == 2560 and height_r == 1600:
        x_initial, y_initial, x_offset, y_offset = (400, 320, 150, 180) # 第一个贴图坐标及偏移
        x_left, x_right, y_top, y_bottom = (295, 429, 188, 350) # 第一个圣遗物坐标
        x_grab, y_grab, w_grab, h_grab = (1820, 422, 364, 152)
        row, col = (4, 7)
    # 1920*1080 | 2560*1440
    elif (width_r == 1920 and height_r == 1080) or (width_r == 2560 and height_r == 1440):
        x_initial, y_initial, x_offset, y_offset = (310 / 1920 * width_r, 242 / 1080 * height_r, 128 / 1920 * width_r, 152 / 1080 * height_r)
        x_left, x_right, y_top, y_bottom = (223 / 1920 * width_r, 333 / 1920 * width_r, 132 / 1080 * height_r, 267 / 1080 * height_r)
        x_grab, y_grab, w_grab, h_grab = (1283 / 1920 * width_r, 437 / 1080 * height_r, 308 / 1920 * width_r, 141 / 1080 * height_r)
        row, col = (4, 6)
    else:
        print('暂不支持该分辨率，请联系作者。')
    
    # 贴图坐标组
    global position
    position = [(x_initial, y_initial), (x_initial + x_offset, y_initial), (x_initial + 2 * x_offset, y_initial), (x_initial + 3 * x_offset, y_initial),
                (x_initial, y_initial + y_offset), (x_initial + x_offset, y_initial + y_offset), (x_initial + 2 * x_offset, y_initial + y_offset), (x_initial + 3 * x_offset, y_initial + y_offset),
                (x_initial, y_initial + 2 * y_offset), (x_initial + x_offset, y_initial + 2 * y_offset), (x_initial + 2 * x_offset, y_initial + 2 * y_offset), (x_initial + 3 * x_offset, y_initial + 2 * y_offset),
                (x_initial, y_initial + 3 * y_offset), (x_initial + x_offset, y_initial + 3 * y_offset), (x_initial + 2 * x_offset, y_initial + 3 * y_offset), (x_initial + 3 * x_offset, y_initial + 3 * y_offset),
                (x_initial, y_initial + 4 * y_offset), (x_initial + x_offset, y_initial + 4 * y_offset), (x_initial + 2 * x_offset, y_initial + 4 * y_offset), (x_initial + 3 * x_offset, y_initial + 4 * y_offset),
                (x_initial, y_initial + 5 * y_offset), (x_initial + x_offset, y_initial + 5 * y_offset), (x_initial + 2 * x_offset, y_initial + 5 * y_offset), (x_initial + 3 * x_offset, y_initial + 5 * y_offset),
                (x_initial, y_initial + 6 * y_offset), (x_initial + x_offset, y_initial + 6 * y_offset), (x_initial + 2 * x_offset, y_initial + 6 * y_offset), (x_initial + 3 * x_offset, y_initial + 6 * y_offset)]
    # 鼠标事件有效坐标区间
    global xarray, yarray
    xarray = [(x_left, x_right), (x_left + x_offset, x_right + x_offset), (x_left + 2 * x_offset, x_right + 2 * x_offset), (x_left + 3 * x_offset, x_right + 3 * x_offset)]
    yarray = [(y_top, y_bottom), (y_top + y_offset, y_bottom + y_offset), (y_top + 2 * y_offset, y_bottom + 2 * y_offset), (y_top + 3 * y_offset, y_bottom + 3 * y_offset), (y_top + 4 * y_offset, y_bottom + 4 * y_offset), (y_top + 5 * y_offset, y_bottom + 5 * y_offset), (y_top + 6 * y_offset, y_bottom + 6 * y_offset), (y_top + 7 * y_offset, y_bottom + 7 * y_offset)]

    # 任务栏图标问题
    try:
        from ctypes import windll  # Only exists on Windows.
        myappid = 'skeathy.keqing.v0.1.1'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.hotkey()

    app.exec()

if __name__ == '__main__':
    main()