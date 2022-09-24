import sys, os, requests
from pynput import keyboard

import location, ocr, score, characters
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

        # 背包/角色面板选择（Radio）
        self.radiobtn1 = QRadioButton('背包')
        self.radiobtn1.setChecked(True)
        self.radiobtn1.toggled.connect(lambda: self.radiobtn_state(self.radiobtn1))
        self.radiobtn2 = QRadioButton('角色')
        self.radiobtn2.toggled.connect(lambda: self.radiobtn_state(self.radiobtn2))

        # 默认坐标信息-背包A
        self.position = location.position_A
        self.row, self.col = location.row_A, location.col_A
        self.xarray, self.yarray = location.xarray_A, location.yarray_A
        self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.x_grab_A, location.y_grab_A, location.w_grab_A, location.h_grab_A
        self.SCALE = location.SCALE

        # 角色选择框
        self.combobox = ExtendedComboBox()
        self.combobox.currentTextChanged.connect(self.current_text_changed)
        self.combobox.addItem('--请选择角色--')
        # 添加角色
        for key in characters.config:
            self.combobox.addItem(key)

        # 识别结果显示，初始配置
        self.name1 = QLabel('请选择圣遗物')
        self.name2 = QLabel('然后点击右键')
        self.name3 = QLabel()
        self.name4 = QLabel()
        self.name5 = QLabel('总分')
        self.score1 = QLabel()
        self.score2 = QLabel()
        self.score3 = QLabel()
        self.score4 = QLabel()
        self.score5 = QLabel('0')

        # GitHub图标与项目链接
        # 更新提示
        self.upgrade = QLabel()
        try:
            response = requests.get('https://api.github.com/repos/SkeathyTomas/genshin_artifact_auxiliary/releases/latest')
            tag = response.json()['tag_name']
            if myappid != tag:
                self.upgrade.setText('有新版本，点击右侧图标前往下载~')
        except:
            pass
        # 图标与release下载链接
        self.github = QLabel()
        self.github.setFixedSize(16, 16)
        pixmap = QPixmap('src/GitHub.png')
        pixmap = pixmap.scaled(16, 16)
        self.github.setPixmap(pixmap)
        self.github.setCursor(Qt.PointingHandCursor)
        self.github.mousePressEvent = self.open_github

        # layout
        self.layout = QGridLayout()
        # 面板选择
        self.layout.addWidget(self.radiobtn1, 0, 0)
        self.layout.addWidget(self.radiobtn2, 0, 1)
        # 角色选择
        self.layout.addWidget(self.combobox, 1, 0, 1, 2)
        # 识别结果展示
        self.layout.addWidget(self.name1, 2, 0)
        self.layout.addWidget(self.score1, 2, 1, Qt.AlignRight)
        self.layout.addWidget(self.name2, 3, 0)
        self.layout.addWidget(self.score2, 3, 1, Qt.AlignRight)
        self.layout.addWidget(self.name3, 4, 0)
        self.layout.addWidget(self.score3, 4, 1, Qt.AlignRight)
        self.layout.addWidget(self.name4, 5, 0)
        self.layout.addWidget(self.score4, 5, 1, Qt.AlignRight)
        self.layout.addWidget(self.name5, 6, 0)
        self.layout.addWidget(self.score5, 6, 1, Qt.AlignRight)
        # 更新与项目链接
        self.layout.addWidget(self.upgrade, 7, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.layout.addWidget(self.github, 7, 1, Qt.AlignRight | Qt.AlignBottom)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)        

        # 预先设定好贴图窗口组
        self.pastes = []
        for i in range(self.row * self.col):
            window = PasteWindow()
            self.pastes.append(window)
            self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)

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
                self.position = location.position_A
                self.row, self.col = location.row_A, location.col_A
                self.xarray, self.yarray = location.xarray_A, location.yarray_A
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.x_grab_A, location.y_grab_A, location.w_grab_A, location.h_grab_A

                # 重置贴图窗口组
                self.pastes = []
                for i in range(self.row * self.col):
                    window = PasteWindow()
                    self.pastes.append(window)
                    self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)
        
        if btn.text() == '角色':
            if btn.isChecked() == True:
                # 重置坐标信息
                self.position = location.position_B
                self.row, self.col = location.row_B, location.col_B
                self.xarray, self.yarray = location.xarray_B, location.yarray_B
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.x_grab_B, location.y_grab_B, location.w_grab_B, location.h_grab_B

                # 重置贴图窗口组
                self.pastes = []
                for i in range(self.row * self.col):
                    window = PasteWindow()
                    self.pastes.append(window)
                    self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)
    
    # 选择框选择角色事件
    def current_text_changed(self, s):
        self.character = s

    # 打开外部链接
    def open_github(self, event):
        QDesktopServices.openUrl(QUrl('https://github.com/SkeathyTomas/genshin_artifact_auxiliary/releases/latest'))

    # 启动贴图弹窗
    def open_new_window(self, x, y):
        # 根据鼠标事件定位贴图
        for i in range(self.col):
            if x >= self.xarray[i][0] and x <= self.xarray[i][1]:
                for j in range(self.row):
                    if y >= self.yarray[j][0] and y <= self.yarray[j][1]:
                        id = j * self.col + i
                        print(self.character + 'detected')

                        # ocr识别与结果返回
                        self.ocr_result = ocr.tesseract_ocr(self.x_grab, self.y_grab, self.w_grab, self.h_grab)
                        self.score_result = score.cal_score(self.ocr_result, self.character)

                        # 贴图更新总评分
                        self.pastes[id].label.setText(str(self.score_result[1]))
                        self.pastes[id].show()

                        # 主窗口更新详细评分
                        self.score5.setText(str(self.score_result[1]))
                        self.name1.setText(list(self.ocr_result.keys())[0] + ' ' + str(list(self.ocr_result.values())[0]))
                        self.score1.setText(str(self.score_result[0][0]))
                        self.name2.setText(list(self.ocr_result.keys())[1] + ' ' + str(list(self.ocr_result.values())[1]))
                        self.score2.setText(str(self.score_result[0][1]))
                        self.name3.setText(list(self.ocr_result.keys())[2] + ' ' + str(list(self.ocr_result.values())[2]))
                        self.score3.setText(str(self.score_result[0][2]))
                        self.name4.setText(list(self.ocr_result.keys())[3] + ' ' + str(list(self.ocr_result.values())[3]))
                        self.score4.setText(str(self.score_result[0][3]))
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
    global myappid
    myappid = 'v0.4.0'

    # 任务栏图标问题
    try:
        from ctypes import windll  # Only exists on Windows.
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