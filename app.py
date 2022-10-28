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
    QRadioButton,
    QComboBox,
    QLineEdit
)

# 主窗口
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'src/keqing.ico')))
        self.setWindowTitle("刻晴办公桌")
        self.setFocusPolicy(Qt.StrongFocus)
        self.move(0, 0)

        # 默认坐标信息-背包A
        self.position = location.position_A
        self.row, self.col = location.row_A, location.col_A
        self.xarray, self.yarray = location.xarray_A, location.yarray_A
        self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.x_grab_A, location.y_grab_A, location.w_grab_A, location.h_grab_A
        self.SCALE = location.SCALE

        # 预先设定好贴图窗口组&每一个窗口的圣遗物数据
        self.pastes = []
        self.id = -1
        self.artifact = {}
        self.score_result = [[0, 0 ,0 ,0], 0]
        for i in range(self.row * self.col):
            window = PasteWindow()
            self.pastes.append(window)
            self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)

        # 背包/角色面板选择（Radio）
        self.radiobtn1 = QRadioButton('背包')
        self.radiobtn1.setChecked(True)
        self.radiobtn2 = QRadioButton('角色')

        # 角色选择框
        self.character = '默认攻击双爆'
        self.combobox = ExtendedComboBox()
        self.combobox.addItem('--请选择角色--')
        # 添加角色
        for key in characters.config:
            self.combobox.addItem(key)

        # 识别结果显示，初始配置
        self.title = QLabel('请选择圣遗物，然后点击右键')
        self.name = []
        self.digit = []
        self.score = []
        for i in range(4):
            self.name.append(QComboBox())
            text = QLineEdit()
            # text.setFixedWidth(50)
            text.setAlignment(Qt.AlignRight)
            self.digit.append(text)
            self.score.append(QLabel())
            self.name[i].addItem('副属性词条'+ str(i + 1))
            self.name[i].addItems(score.coefficient.keys())
            self.name[i].addItem('无')
            self.name[i].addItem('识别错误')
        self.name5 = QLabel('总分')
        self.score5 = QLabel('0')

        # GitHub图标与项目链接
        # 更新提示
        self.upgrade = QLabel()
        try:
            response = requests.get('https://api.github.com/repos/SkeathyTomas/genshin_artifact_auxiliary/releases/latest')
            tag = response.json()['tag_name']
            if myappid != tag:
                self.upgrade.setText('有新版本，点击右侧图标前往下载~')
            else:
                self.upgrade.setText(myappid)
        except:
            pass
        # 图标与release下载链接
        self.github = QLabel()
        self.github.setFixedSize(16, 16)
        pixmap = QPixmap('src/GitHub.png')
        pixmap = pixmap.scaled(16, 16)
        self.github.setPixmap(pixmap)

        # layout
        self.layout = QGridLayout()
        # 面板选择
        self.layout.addWidget(self.radiobtn1, 0, 0)
        self.layout.addWidget(self.radiobtn2, 0, 1)
        # 角色选择
        self.layout.addWidget(self.combobox, 1, 0, 1, 3)
        # 识别结果展示
        self.layout.addWidget(self.title, 2, 0, 1, 3)
        for i in range(4):
            self.layout.addWidget(self.name[i], i + 3, 0)
            self.layout.addWidget(self.digit[i], i + 3, 1)
            self.layout.addWidget(self.score[i], i + 3, 2, Qt.AlignRight)
        self.layout.addWidget(self.name5, 7, 0)
        self.layout.addWidget(self.score5, 7, 2, Qt.AlignRight)
        # 更新与项目链接
        self.layout.addWidget(self.upgrade, 8, 0, Qt.AlignLeft | Qt.AlignBottom)
        self.layout.addWidget(self.github, 8, 2, Qt.AlignRight | Qt.AlignBottom)
        # layout载入widget中
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # 事件链接
        # 背包、角色单选
        self.radiobtn1.toggled.connect(lambda: self.radiobtn_state(self.radiobtn1))
        self.radiobtn2.toggled.connect(lambda: self.radiobtn_state(self.radiobtn2))
        # 角色下拉框选择
        self.combobox.currentIndexChanged.connect(self.current_index_changed)
        # 图标外部链接
        self.github.setCursor(Qt.PointingHandCursor)
        self.github.mousePressEvent = self.open_github
        # 外部鼠标事件启动识别和贴图弹窗
        self.manager = OutsideMouseManager()
        self.manager.right_click.connect(self.open_new_window)
        self.manager.left_click.connect(self.left_click_artifact)

    # 单选框面板选择事件
    def radiobtn_state(self, btn):
        if btn.text() == '背包':
            if btn.isChecked() == True:
                # 重置坐标信息
                self.position = location.position_A
                self.row, self.col = location.row_A, location.col_A
                self.xarray, self.yarray = location.xarray_A, location.yarray_A
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.x_grab_A, location.y_grab_A, location.w_grab_A, location.h_grab_A

                # 重置贴图窗口组&圣遗物数据&主窗口信息
                self.pastes = []
                self.artifact = {}
                for i in range(self.row * self.col):
                    window = PasteWindow()
                    self.pastes.append(window)
                    self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)
                self.title.setText('请选择圣遗物，然后点击右键')
                for i in range(4):
                    self.name[i].setCurrentText('副属性词条'+ str(i + 1))
                    self.digit[i].setText('')
                    self.score[i].setText('')
                self.score5.setText('0')
        
        if btn.text() == '角色':
            if btn.isChecked() == True:
                # 重置坐标信息
                self.position = location.position_B
                self.row, self.col = location.row_B, location.col_B
                self.xarray, self.yarray = location.xarray_B, location.yarray_B
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.x_grab_B, location.y_grab_B, location.w_grab_B, location.h_grab_B

                # 重置贴图窗口组&圣遗物数据
                self.pastes = []
                self.artifact = {}
                for i in range(self.row * self.col):
                    window = PasteWindow()
                    self.pastes.append(window)
                    self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)
                self.title.setText('请选择圣遗物，然后点击右键')
                for i in range(4):
                    self.name[i].setCurrentText('副属性词条'+ str(i + 1))
                    self.digit[i].setText('')
                    self.score[i].setText('')
                self.score5.setText('0')
    
    # 选择框选择角色事件
    def current_index_changed(self, index):
        self.character = self.combobox.currentText()
        # 更新评分贴图
        for i in range(len(self.pastes)):
            if self.pastes[i].isVisible() == True:
                self.score_result = score.cal_score(self.artifact[i], self.character)
                self.pastes[i].label.setText(str(self.score_result[1]))
        
        # 更新主程序评分详情
        if self.id != -1:
            self.fresh_ocr_result()

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
                        self.id = j * self.col + i
                        print(self.character + 'detected')
                        
                        # ocr识别与结果返回并刷新主面板
                        self.artifact[self.id] = ocr.tesseract_ocr(self.x_grab, self.y_grab, self.w_grab, self.h_grab)
                        self.fresh_ocr_result()
                        break
                break

    # 根据鼠标左键选择的圣遗物刷新主窗口圣遗物副属性和评分
    def left_click_artifact(self, x, y):
        for i in range(self.col):
            if x >= self.xarray[i][0] and x <= self.xarray[i][1]:
                for j in range(self.row):
                    if y >= self.yarray[j][0] and y <= self.yarray[j][1]:
                        id_temp = j * self.col + i
                        if self.pastes[id_temp].isVisible() == True:
                            self.id = id_temp
                            self.fresh_ocr_result()
                            break
                break
    
    # 刷新圣遗物识别结果面板
    def fresh_ocr_result(self):
        # 刷新圣遗物id提示
        self.title.setText('圣遗物' + str(self.id + 1))

        # 计算评分（计算很快就不另外储存了）
        self.score_result = score.cal_score(self.artifact[self.id], self.character)

        # 贴图更新总评分
        self.pastes[self.id].label.setText(str(self.score_result[1]))
        self.pastes[self.id].show()

        # 主窗口更新详细评分
        self.score5.setText(str(self.score_result[1]))
        for i in range(4):
            if i < len(self.artifact[self.id]):
                if list(self.artifact[self.id].keys())[i] in score.coefficient.keys():
                    self.name[i].setCurrentText(list(self.artifact[self.id].keys())[i])
                    self.digit[i].setText(str(list(self.artifact[self.id].values())[i]))
                    self.score[i].setText(str(self.score_result[0][i]))
                else:
                    self.name[i].setCurrentText('识别错误')
                    self.digit[i].setText(list(self.artifact[self.id].keys())[i])
                    self.score[i].setText('')
            else:
                self.name[i].setCurrentText('无')
                self.digit[i].setText('')
                self.score[i].setText('')
    
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
    myappid = 'v0.4.1'

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