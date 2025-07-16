'''参数设置页面'''

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFormLayout, QLineEdit
from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator
from doc import coefficient_path
import json, score

class SettingsPage(QWidget):
    go_back = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.form_layout = QFormLayout()

        # 创建表单控件
        self.line_edits = {}
        for key, value in score.coefficient.items():
            label = QLabel(key)
            line_edit = QLineEdit(str(value))
            line_edit.setValidator(QDoubleValidator())  # 限制输入为浮点数
            self.line_edits[key] = line_edit
            self.form_layout.addRow(label, line_edit)

        # 添加保存按钮
        save_button = QPushButton("保存设置")
        save_button.clicked.connect(self.save_settings)
        self.form_layout.addRow(save_button)

        self.setLayout(self.form_layout)
    
    def save_settings(self):
        # 从表单中读取用户输入的值
        new_coefficient = {}
        for key, line_edit in self.line_edits.items():
            try:
                new_coefficient[key] = float(line_edit.text())
            except ValueError:
                new_coefficient[key] = score.coefficient[key]  # 如果输入无效，保留原值

        # 更新变量
        score.coefficient = new_coefficient

        # 更新配置文件
        with open(coefficient_path, "w", encoding = 'utf-8') as f:
            json.dump(new_coefficient, f, ensure_ascii = False)

        # 关闭设置页面
        self.go_back.emit()