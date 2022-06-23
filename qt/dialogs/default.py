import sys
from PyQt6.QtWidgets import QGridLayout 
from PyQt6.QtWidgets import QLabel 
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from qt.draggable import DraggablesDialog 
from utils.qt_utils import resource_path

class DefaultDialog(DraggablesDialog):
    def __init__(self, msg:str, btn:tuple=None):
        super().__init__()

        self.title = '알림'
        self.main_msg = msg
        self.btn = btn
        self.icon = QIcon(resource_path(relative_path='icons/delete.png'))

        self.answer: bool = False

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setMinimumWidth(200)

        lbl_main_msg = QLabel(self.main_msg, self)
        lbl_main_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_main_msg.setMinimumHeight(30)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(lbl_main_msg)

        if not self.btn:
            return

        self.btn_yes= QPushButton(f'{self.btn[0]}(y)', self)
        self.btn_yes.setMinimumHeight(30)
        self.btn_yes.clicked.connect(self.on_btn_yes)
        self.btn_yes.setShortcut('Y')
        layout.addWidget(self.btn_yes)

        if len(self.btn) > 1:
            self.btn_no= QPushButton(f'{self.btn[1]}(n)', self)
            self.btn_no.setMinimumHeight(30)
            self.btn_no.clicked.connect(self.on_btn_no)
            self.btn_no.setShortcut('N')
            layout.addWidget(self.btn_no)

    def on_btn_yes(self):  # sourcery skip: class-extract-method
        self.answer = True
        self.close()

    def on_btn_no(self):
        self.answer = False
        self.close()

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    DefaultDialog('',('','')).exec()
    sys.exit(app.exec())