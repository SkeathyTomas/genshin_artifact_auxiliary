import sys, os
from pynput import keyboard

import location
import img_process
from extention import OutsideMouseManager, ExtendedComboBox
from paste_window import PasteWindow

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QKeySequence, QShortcut, QIcon, QPixmap, QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QRadioButton
)

# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'src/keqing.ico')))
        self.setWindowTitle("刻晴办公桌")
        self.move(0, 0)
        self.character = ''

        # 背包/角色面板选择（Radio）
        self.radiobtn1 = QRadioButton('背包')
        self.radiobtn1.setChecked(True)
        self.radiobtn1.toggled.connect(lambda: self.radiobtn_state(self.radiobtn1))
        self.radiobtn2 = QRadioButton('角色')
        self.radiobtn2.toggled.connect(lambda: self.radiobtn_state(self.radiobtn2))

        # 默认坐标信息
        self.position = location.get_position_A()
        self.row, self.col = location.get_row_col_A()
        self.xarray, self.yarray = location.get_xarray_yarray_A()
        self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.get_x_y_w_h_A()
        self.SCALE = location.get_scale()

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
        self.combobox.addItem('多莉')

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
        self.combobox.addItem('旅行者-草')
        self.combobox.addItem('提纳里')
        self.combobox.addItem('柯莱')

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
        self.layout.addWidget(self.radiobtn1, 0, 0)
        self.layout.addWidget(self.radiobtn2, 0, 1)
        self.layout.addWidget(self.combobox, 1, 0, 1, 2)
        self.layout.addWidget(self.label, 2, 0, 1, 2, Qt.AlignRight | Qt.AlignBottom)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)        

        # 预先设定好贴图窗口组
        self.pastes = []
        for i in range(self.row * self.col):
            window = PasteWindow()
            self.pastes.append(window)

        # 快捷键Ctrl+Z关闭所有贴图窗口，需焦点在主窗口
        self.shortcut = QShortcut(QKeySequence('Ctrl+Shift+Z'), self)
        self.shortcut.activated.connect(self.reset)

        # 外部鼠标事件启动识别和贴图弹窗
        self.manager = OutsideMouseManager()
        self.manager.released.connect(self.open_new_window)

    # 单选框面板选择事件
    def radiobtn_state(self, btn):
        if btn.text() == '背包':
            if btn.isChecked() == True:
                # 重置坐标信息
                self.position = location.get_position_A()
                self.row, self.col = location.get_row_col_A()
                self.xarray, self.yarray = location.get_xarray_yarray_A()
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.get_x_y_w_h_A()

                # 重置贴图窗口组
                self.pastes = []
                for i in range(self.row * self.col):
                    window = PasteWindow()
                    self.pastes.append(window)
        
        if btn.text() == '角色':
            if btn.isChecked() == True:
                # 重置坐标信息
                self.position = location.get_position_B()
                self.row, self.col = location.get_row_col_B()
                self.xarray, self.yarray = location.get_xarray_yarray_B()
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.get_x_y_w_h_B()

                # 重置贴图窗口组
                self.pastes = []
                for i in range(self.row * self.col):
                    window = PasteWindow()
                    self.pastes.append(window)
    
    # 选择框选择角色事件
    def current_text_changed(self, s):
        self.character = s

    # 打开外部链接
    def open_github(self, event):
        QDesktopServices.openUrl(QUrl('https://github.com/SkeathyTomas/genshin_artifact_auxiliary'))

    # 启动贴图弹窗
    def open_new_window(self, x, y):
        # 根据鼠标事件定位贴图
        for i in range(self.col):
            if x >= self.xarray[i][0] and x <= self.xarray[i][1]:
                for j in range(self.row):
                    if y >= self.yarray[j][0] and y <= self.yarray[j][1]:
                        id = j * self.col + i
                        print('detected')
                        score = img_process.main(self.character, self.x_grab, self.y_grab, self.w_grab, self.h_grab)
                        self.pastes[id].label.setText(str(score))
                        self.pastes[id].show()
                        self.pastes[id].move(self.position[id][0] / self.SCALE, self.position[id][1] / self.SCALE)
                        break
                break
    
    # 主窗口关闭则所有贴图窗口也关闭
    def closeEvent(self, event):
        for item in self.pastes:
            item.close()
    
    # 快捷键Ctrl+Shift+Z重置贴图窗口
    def reset(self):
        for item in self.pastes:
            item.hide()

    # 全局快捷键Ctrl+Shift+Z重置贴图窗口
    def hotkey(self):
        def on_activate():
            print('reset!')
            self.reset()
        
        def for_canonical(f):
            return lambda k: f(l.canonical(k))
        
        hotkey = keyboard.HotKey(keyboard.HotKey.parse('<ctrl>+<shift>+z'), on_activate)
        l = keyboard.Listener(
            on_press = for_canonical(hotkey.press),
            on_release = for_canonical(hotkey.release))
        l.start()

def main():
    # 任务栏图标问题
    try:
        from ctypes import windll  # Only exists on Windows.
        myappid = 'skeathy.keqing.v0.3.0'
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