import sys, os, requests, json
import qdarktheme
from pynput import keyboard

import doc, location, ocr, score, mona
from extention import OutsideMouseManager, ExtendedComboBox
from paste_window import PasteWindow

from PySide6.QtCore import Qt, QUrl, QTimer
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

        # 默认坐标信息-角色B
        self.position = location.position_B
        self.row, self.col = location.row_B, location.col_B
        self.xarray, self.yarray = location.xarray_B, location.yarray_B
        self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.x_grab_B, location.y_grab_B, location.w_grab_B, location.h_grab_B
        self.SCALE = location.SCALE

        # 预先设定好贴图窗口组&每一个窗口的圣遗物数据
        self.pastes = []
        self.id = -1
        # 当前屏幕中圣遗物坐标及副词条dict，{'0': {'暴击率': 2.0}, '2': {'暴击伤害': 4.0}}
        self.artifact = {}
        self.score_result = [[0, 0, 0, 0], 0]
        for i in range(self.row * self.col):
            window = PasteWindow()
            self.pastes.append(window)
            self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)

        # 背包/角色面板选择（Radio）
        self.radiobtn1 = QRadioButton('角色')
        self.radiobtn1.setChecked(True)
        self.radiobtn2 = QRadioButton('背包')
        self.type = '角色'

        # 默认角色及配置
        self.character = '默认攻击双爆'
        self.config = {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0,
                       '元素充能效率': 0}
        # 角色选择框
        self.combobox = ExtendedComboBox()
        # 添加角色
        with open(doc.character_path, 'r', encoding='utf-8') as f:
            self.characters = json.load(f)
        for key in self.characters:
            self.combobox.addItem(key)

        # 识别结果显示，初始配置
        self.title = QLabel('请选择圣遗物，然后点击右键')
        self.name = []
        self.digit = []
        self.strengthen = []
        self.score = []
        for i in range(4):
            self.name.append(QComboBox())
            text = QLineEdit("0")
            # text.setFixedWidth(50)
            text.setAlignment(Qt.AlignRight)
            self.digit.append(text)
            self.score.append(QLabel("0"))
            self.strengthen.append(QLabel("+0"))
            self.name[i].addItem('副属性词条' + str(i + 1))
            self.name[i].addItems(score.coefficient.keys())
            self.name[i].addItem('识别错误')
        self.button = QPushButton('确认修改')

        self.entries = QLabel('有效词条：0')
        self.total = QLabel('总分')
        self.score_total = QLabel('0')

        # 评分方案本地保存，选择框、保存确认按钮
        self.archive = ExtendedComboBox()
        self.archive.setEditable(True)
        self.archive.addItem('----保存此屏结果请输入名称----')
        with open(doc.archive_path, 'r', encoding='utf-8') as fp:
            self.artifacts = json.load(fp)
        for name in self.artifacts[self.type]:
            self.archive.addItem(name)
        self.save = QPushButton('保存')

        # GitHub图标与项目链接
        # 更新提示
        self.upgrade = QLabel()
        try:
            response = requests.get(
                'https://api.github.com/repos/SkeathyTomas/genshin_artifact_auxiliary/releases/latest')
            tag = response.json()['tag_name']
            if myappid != tag:
                self.upgrade.setText('有新版本，点击右侧图标前往下载~')
            else:
                self.upgrade.setText(myappid)
        except:
            pass
        # 图标与release下载链接
        self.github = QLabel()
        self.github.setFixedSize(20, 20)
        pixmap = QPixmap('src/GitHub.png')
        pixmap = pixmap.scaled(16, 16)
        self.github.setPixmap(pixmap)

        # layout
        self.layout = QGridLayout()
        # 面板选择
        self.layout.addWidget(self.radiobtn1, 0, 0)
        self.layout.addWidget(self.radiobtn2, 0, 1)
        # 角色选择
        self.layout.addWidget(self.combobox, 1, 0, 1, 4)
        # 识别结果展示
        self.layout.addWidget(self.title, 2, 0, 1, 4)
        for i in range(4):
            self.layout.addWidget(self.name[i], i + 3, 0)
            self.layout.addWidget(self.digit[i], i + 3, 1)
            self.layout.addWidget(self.strengthen[i], i + 3, 2, Qt.AlignRight)
            self.layout.addWidget(self.score[i], i + 3, 3, Qt.AlignRight)
        # 总分计算结果
        self.layout.addWidget(self.button, 7, 0)
        self.layout.addWidget(self.entries, 7, 1, Qt.AlignRight)
        self.layout.addWidget(self.total, 7, 2, Qt.AlignRight)
        self.layout.addWidget(self.score_total, 7, 3, Qt.AlignRight)
        # 保存/读取方案
        self.layout.addWidget(self.archive, 8, 0, 1, 3)
        self.layout.addWidget(self.save, 8, 3)
        # 更新与项目链接
        self.layout.addWidget(self.upgrade, 9, 0, 1, 2, Qt.AlignLeft | Qt.AlignBottom)
        self.layout.addWidget(self.github, 9, 3, Qt.AlignRight | Qt.AlignBottom)
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
        # 识别结果修改
        self.button.clicked.connect(self.button_clicked)
        # 本地方案选择
        self.archive.currentIndexChanged.connect(self.archive_index_changed)
        # 方案保存按钮
        self.save.clicked.connect(self.button_save)
        # 图标外部链接
        self.github.setCursor(Qt.PointingHandCursor)
        self.github.mousePressEvent = self.open_github
        # 外部鼠标事件启动识别和贴图弹窗
        self.manager = OutsideMouseManager()
        self.manager.right_click.connect(self.open_new_window)
        self.manager.left_click.connect(self.left_click_artifact)
        # 全局热键
        self.hotkey()
        # 数据插入模式
        self.insert = False
        self.insert_mode()

    # 单选框面板选择事件
    def radiobtn_state(self, btn):
        if btn.text() == '背包':
            if btn.isChecked() == True:
                self.type = '背包'
                self.reset_archive()
                # 重置坐标信息
                # import location
                self.position = location.position_A
                self.row, self.col = location.row_A, location.col_A
                self.xarray, self.yarray = location.xarray_A, location.yarray_A
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.x_grab_A, location.y_grab_A, location.w_grab_A, location.h_grab_A
                self.reset()

        if btn.text() == '角色':
            if btn.isChecked() == True:
                self.type = '角色'
                self.reset_archive()
                # 重置坐标信息
                # import location
                self.position = location.position_B
                self.row, self.col = location.row_B, location.col_B
                self.xarray, self.yarray = location.xarray_B, location.yarray_B
                self.x_grab, self.y_grab, self.w_grab, self.h_grab = location.x_grab_B, location.y_grab_B, location.w_grab_B, location.h_grab_B
                self.reset()

    # 重置保存结果选择框
    def reset_archive(self):
        self.archive.clear()
        self.archive.addItem('----保存此屏结果请输入名称----')
        for name in self.artifacts[self.type]:
            self.archive.addItem(name)

    # 选择框选择角色事件
    def current_index_changed(self, index):
        self.character = self.combobox.currentText()
        try:
            self.config = self.characters[self.character]
            if self.config == {}:
                self.config = {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0,
                               '元素充能效率': 0}
        except:
            self.config = {'生命值': 0, '攻击力': 0.75, '防御力': 0, '暴击率': 1, '暴击伤害': 1, '元素精通': 0,
                           '元素充能效率': 0}
        # 更新评分贴图
        for i in range(len(self.pastes)):
            if self.pastes[i].isVisible() == True:
                self.score_result = score.cal_score(self.artifact[str(i)][1], self.config)
                self.pastes[i].label.setText(str(self.score_result[1]))

        # 更新主程序评分详情
        if self.artifact != {}:
            self.fresh_main_window()

    # 修改识别结果按钮
    def button_clicked(self):
        self.artifact[str(self.id)][1] = {}
        for i in range(4):
            try:
                self.artifact[str(self.id)][1][self.name[i].currentText()] = float(self.digit[i].text())
            except:
                pass
        print(self.artifact[str(self.id)])
        if self.id != -1:
            self.fresh_main_window()
            self.fresh_paste_window()
        else:
            self.fresh_main_window()

    # 方案选择框事件
    def archive_index_changed(self, index):
        self.reset()

        currentText = self.archive.currentText()
        if currentText in self.artifacts[self.type]:
            self.artifact = self.artifacts[self.type][self.archive.currentText()].copy()
            print(self.artifact)
            for key in self.artifact:
                self.id = eval(key)
                if self.id != -1:
                    self.fresh_main_window()
                    self.fresh_paste_window()
                else:
                    self.fresh_main_window()

    # 保存方案按钮
    def button_save(self):
        new_archive = self.archive.currentText()
        if new_archive == '----保存此屏结果请输入名称----' or new_archive == '':
            hint_txt = '请输入名称~'
        elif self.artifact != {}:
            if new_archive not in self.artifacts[self.type].keys():
                self.archive.addItem(new_archive)
                hint_txt = '保存成功！'
            else:
                hint_txt = '更新成功！'
            self.artifacts[self.type].update({new_archive: self.artifact})
            dic_sorted = sorted(self.artifacts[self.type].items())
            self.artifacts[self.type] = {k: v for k, v in dic_sorted}
            with open(doc.archive_path, 'w', encoding='utf-8') as fp:
                json.dump(self.artifacts, fp, ensure_ascii=False)
            mona.update() #保存一次更新一次mona格式的导出
        else:
            hint_txt = '未识别圣遗物，无结果保存~'

        # 保存按钮结果提示
        self.upgrade.setText(hint_txt)
        self.timer = QTimer()
        self.timer.timeout.connect(self.reset_myappid)
        self.timer.start(2000)

    # 恢复版本号信息
    def reset_myappid(self):
        self.upgrade.setText(myappid)

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
                        print(self.character + 'detected')
                        # 插入模式后移数据
                        self.id = j * self.col + i
                        if self.insert:
                            self.insert_data()
                        # ocr识别与结果返回并刷新主面板、贴图
                        self.id = j * self.col + i
                        self.artifact[str(self.id)] = ocr.rapidocr(self.x_grab, self.y_grab, self.w_grab, self.h_grab)
                        self.fresh_main_window()
                        self.fresh_paste_window()
                        break
                break

    # 插入模式后移数据
    def insert_data(self):
        old = {}
        for key in self.artifact:
            if eval(key) >= self.id:
                new = self.artifact[key]
                self.artifact[key] = old
                old = new
        self.artifact[str(len(self.artifact))] = old
        print(self.artifact)
        # 贴图需要刷新
        for key in self.artifact:
            if eval(key) > self.id:
                self.id = eval(key)
                self.score_result = score.cal_score(self.artifact[str(self.id)][1], self.config)
                self.fresh_paste_window()

    # 根据鼠标左键选择的圣遗物刷新主窗口圣遗物副属性和评分
    def left_click_artifact(self, x, y):
        for i in range(self.col):
            if x >= self.xarray[i][0] and x <= self.xarray[i][1]:
                for j in range(self.row):
                    if y >= self.yarray[j][0] and y <= self.yarray[j][1]:
                        id_temp = j * self.col + i
                        if self.pastes[id_temp].isVisible() == True:
                            self.id = id_temp
                            self.fresh_main_window()
                            break
                break

    # 刷新主程序（识别、选择、切换角色、修改后确认、加载本地数据）
    def fresh_main_window(self):
        # 刷新圣遗物基本信息
        self.title.setText('-'.join(self.artifact[str(self.id)][0]))

        # 计算评分（计算很快就不另外储存了）
        self.score_result = score.cal_score(self.artifact[str(self.id)][1], self.config)

        # 主窗口更新详细评分
        self.score_total.setText(str(self.score_result[1]))
        self.entries.setText('有效词条：' + str(self.score_result[3]))
        for i in range(4):
            if i < len(self.artifact[str(self.id)][1]):
                if list(self.artifact[str(self.id)][1].keys())[i] in score.coefficient.keys():
                    self.name[i].setCurrentText(list(self.artifact[str(self.id)][1].keys())[i])
                    self.digit[i].setText(str(list(self.artifact[str(self.id)][1].values())[i]))
                    self.score[i].setText(str(self.score_result[0][i]))
                    self.strengthen[i].setText("+" + str(self.score_result[2][i]))
                else:
                    self.name[i].setCurrentText('识别错误')
                    self.digit[i].setText(list(self.artifact[str(self.id)][1].keys())[i])
                    self.score[i].setText('0')
                    self.strengthen[i].setText("+0")
            else:
                self.name[i].setCurrentText('识别错误')
                self.digit[i].setText('0')
                self.score[i].setText('0')
                self.strengthen[i].setText("+0")

    # 刷新圣遗物贴图（识别、修改后确认、加载本地数据,后于主面板更新）
    def fresh_paste_window(self):
        self.pastes[self.id].label.setText(str(self.score_result[1]))
        self.pastes[self.id].show()

    # 重置圣遗物数据&贴图窗口&主程序窗口
    def reset(self):
        # 主程序重置
        self.id = -1
        self.title.setText('请选择圣遗物，然后点击右键')
        for i in range(4):
            self.name[i].setCurrentText('副属性词条' + str(i + 1))
            self.digit[i].setText('0')
            self.score[i].setText('0')
            self.strengthen[i].setText("+0")
        self.score_total.setText('0')
        self.entries.setText('有效词条：0')

        # 数据重置
        self.pastes = []
        self.artifact = {}
        for i in range(self.row * self.col):
            window = PasteWindow()
            self.pastes.append(window)
            self.pastes[i].move(self.position[i][0] / self.SCALE, self.position[i][1] / self.SCALE)

    # 主窗口关闭则所有贴图窗口也关闭
    def closeEvent(self, event):
        for item in self.pastes:
            item.close()

    # 全局快捷键Ctrl+Shift+Z重置贴图窗口
    def hotkey(self):
        def on_activate():
            print('reset!')
            # self.reset() # 为啥这里调用就闪退
            self.id = -1
            self.artifact = {}
            self.title.setText('请选择圣遗物，然后点击右键')
            for i in range(4):
                self.name[i].setCurrentText('副属性词条' + str(i + 1))
                # self.digit[i].setText('0')  # 不明原因引起闪退，reset()里也是因为这个
                self.score[i].setText('0')
                self.strengthen[i].setText("+0")
            self.score_total.setText('0')
            self.entries.setText('有效词条：0')
            for item in self.pastes:
                item.hide()

        h = keyboard.GlobalHotKeys({'<ctrl>+<shift>+z': on_activate})
        h.start()

    # 左Alt键插入新数据模式，之后的圣遗物后移一位
    def insert_mode(self):
        def on_press(key):
            if not self.insert and key == keyboard.Key.alt_l:
                print('insert start!')
                self.insert = True
                self.upgrade.setText('插入模式')

        def on_release(key):
            if key == keyboard.Key.alt_l:
                print('insert end!')
                self.insert = False
                self.upgrade.setText(myappid)

        l = keyboard.Listener(on_press=on_press, on_release=on_release)
        l.start()


def main():
    global myappid
    myappid = 'v0.8.1'

    # 任务栏图标问题
    try:
        from ctypes import windll  # Only exists on Windows.
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass

    app = QApplication(sys.argv)
    # qdarktheme.setup_theme('light')
    app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()