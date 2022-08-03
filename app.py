import sys, os
import win32con, win32api, win32gui, win32print
from pynput import mouse, keyboard
import img_process

from PySide6.QtCore import Qt, Signal, QObject, QSortFilterProxyModel, QUrl
from PySide6.QtGui import QKeySequence, QShortcut, QIcon, QPixmap, QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QComboBox,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QCompleter
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
        self.combobox.addItem('温迪-攻爆流')
        self.combobox.addItem('温迪-精通流')
        self.combobox.addItem('琴')
        self.combobox.addItem('魈')
        self.combobox.addItem('早柚')
        self.combobox.addItem('砂糖')

        # 火
        self.combobox.addItem('托马')
        self.combobox.addItem('胡桃')
        self.combobox.addItem('宵宫')
        self.combobox.addItem('可莉-纯火流')
        self.combobox.addItem('可莉-反应流')
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
        self.combobox.addItem('甘雨-永冻流')
        self.combobox.addItem('甘雨-反应流')
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
        for i in range(56):
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
        # 贴图坐标组
        position = [(x_initial, y_initial), (x_initial + x_offset, y_initial), (x_initial + 2 * x_offset, y_initial), (x_initial + 3 * x_offset, y_initial), (x_initial + 4 * x_offset, y_initial), (x_initial + 5 * x_offset, y_initial), (x_initial + 6 * x_offset, y_initial), (x_initial + 7 * x_offset, y_initial),
                    (x_initial, y_initial + y_offset), (x_initial + x_offset, y_initial + y_offset), (x_initial + 2 * x_offset, y_initial + y_offset), (x_initial + 3 * x_offset, y_initial + y_offset), (x_initial + 4 * x_offset, y_initial + y_offset), (x_initial + 5 * x_offset, y_initial + y_offset), (x_initial + 6 * x_offset, y_initial + y_offset), (x_initial + 7 * x_offset, y_initial + y_offset),
                    (x_initial, y_initial + 2 * y_offset), (x_initial + x_offset, y_initial + 2 * y_offset), (x_initial + 2 * x_offset, y_initial + 2 * y_offset), (x_initial + 3 * x_offset, y_initial + 2 * y_offset), (x_initial + 4 * x_offset, y_initial + 2 * y_offset), (x_initial + 5 * x_offset, y_initial + 2 * y_offset), (x_initial + 6 * x_offset, y_initial + 2 * y_offset), (x_initial + 7 * x_offset, y_initial + 2 * y_offset),
                    (x_initial, y_initial + 3 * y_offset), (x_initial + x_offset, y_initial + 3 * y_offset), (x_initial + 2 * x_offset, y_initial + 3 * y_offset), (x_initial + 3 * x_offset, y_initial + 3 * y_offset), (x_initial + 4 * x_offset, y_initial + 3 * y_offset), (x_initial + 5 * x_offset, y_initial + 3 * y_offset), (x_initial + 6 * x_offset, y_initial + 3 * y_offset), (x_initial + 7 * x_offset, y_initial + 3 * y_offset),
                    (x_initial, y_initial + 4 * y_offset), (x_initial + x_offset, y_initial + 4 * y_offset), (x_initial + 2 * x_offset, y_initial + 4 * y_offset), (x_initial + 3 * x_offset, y_initial + 4 * y_offset), (x_initial + 4 * x_offset, y_initial + 4 * y_offset), (x_initial + 5 * x_offset, y_initial + 4 * y_offset), (x_initial + 6 * x_offset, y_initial + 4 * y_offset), (x_initial + 7 * x_offset, y_initial + 4 * y_offset),
                    (x_initial, y_initial + 5 * y_offset), (x_initial + x_offset, y_initial + 5 * y_offset), (x_initial + 2 * x_offset, y_initial + 5 * y_offset), (x_initial + 3 * x_offset, y_initial + 5 * y_offset), (x_initial + 4 * x_offset, y_initial + 5 * y_offset), (x_initial + 5 * x_offset, y_initial + 5 * y_offset), (x_initial + 6 * x_offset, y_initial + 5 * y_offset), (x_initial + 7 * x_offset, y_initial + 5 * y_offset),
                    (x_initial, y_initial + 6 * y_offset), (x_initial + x_offset, y_initial + 6 * y_offset), (x_initial + 2 * x_offset, y_initial + 6 * y_offset), (x_initial + 3 * x_offset, y_initial + 6 * y_offset), (x_initial + 4 * x_offset, y_initial + 6 * y_offset), (x_initial + 5 * x_offset, y_initial + 6 * y_offset), (x_initial + 6 * x_offset, y_initial + 6 * y_offset), (x_initial + 7 * x_offset, y_initial + 6 * y_offset)]
        # 鼠标事件有效坐标区间
        xarray = [(x_left, x_right), (x_left + x_offset, x_right + x_offset), (x_left + 2 * x_offset, x_right + 2 * x_offset), (x_left + 3 * x_offset, x_right + 3 * x_offset), (x_left + 4 * x_offset, x_right + 4 * x_offset), (x_left + 5 * x_offset, x_right + 5 * x_offset), (x_left + 6 * x_offset, x_right + 6 * x_offset), (x_left + 7 * x_offset, x_right + 7 * x_offset)]
        yarray = [(y_top, y_bottom), (y_top + y_offset, y_bottom + y_offset), (y_top + 2 * y_offset, y_bottom + 2 * y_offset), (y_top + 3 * y_offset, y_bottom + 3 * y_offset), (y_top + 4 * y_offset, y_bottom + 4 * y_offset), (y_top + 5 * y_offset, y_bottom + 5 * y_offset), (y_top + 6 * y_offset, y_bottom + 6 * y_offset), (y_top + 7 * y_offset, y_bottom + 7 * y_offset)]

        # 根据鼠标事件定位贴图，i列j行
        for i in range(8):
            for j in range(7):
                if x >= xarray[i][0] and x <= xarray[i][1] and y >= yarray[j][0] and y <= yarray[j][1]:
                    id = j * 8 + i
                    # 判断贴图是否存在，存在则不更新，不在则更新
                    if self.pastes[id].isVisible():
                        break
                    else:
                        print('detected')
                        try:
                            score = img_process.main(self.character, x_grab, y_grab, w_grab, h_grab)
                            self.pastes[id].label.setText(str(score))
                        except:
                            print('图像识别有误！')
                        self.pastes[id].show()
                        self.pastes[id].move(position[id][0] // SCALE, position[id][1] // SCALE)
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

# 增强选择框
class ExtendedComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ExtendedComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.ClickFocus)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)

        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox 
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)

    # on model change, update the models of the filter and completer as well 
    def setModel(self, model):
        super(ExtendedComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(ExtendedComboBox, self).setModelColumn(column)

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
        font.setPointSize(14 // SCALE)
        self.label.setFont(font)
        self.label.setFixedSize(36 // SCALE, 36 // SCALE)
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
    global x_initial, y_initial, x_offset, y_offset # 第一个贴图坐标及偏移
    global x_left, x_right, y_top, y_bottom # 第一个圣遗物坐标
    global x_grab, y_grab, w_grab, h_grab # 截图w, y, w, h
    # 2560*1600
    if width_r == 2560 and height_r == 1600:
        x_initial, y_initial, x_offset, y_offset = (490, 320, 156, 188)
        x_left, x_right, y_top, y_bottom = (382, 512, 182, 346)
        x_grab, y_grab, w_grab, h_grab = (1684, 560, 350, 168)
    # 1920*1080
    elif width_r == 1920 and height_r == 1080:
        x_initial, y_initial, x_offset, y_offset = (310, 242, 128, 152)
        x_left, x_right, y_top, y_bottom = (223, 333, 132, 267)
        x_grab, y_grab, w_grab, h_grab = (1283, 437, 308, 141)
    else:
        print('暂不支持该分辨率，请联系作者。')

    # 任务栏图标问题
    try:
        from ctypes import windll  # Only exists on Windows.
        myappid = 'skeathy.keqing.v0.1.0'
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