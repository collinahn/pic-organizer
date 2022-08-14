from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QDialog

from utils.qt_utils import resource_path
from utils.constants import VERSION


class ProgramInfoDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.title = 'Thanos 정보'
        self.icon_path = resource_path('icons/reality_stone.png')
        self.pixmap_path = resource_path('icons/thanos.png')

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon_path))

        lbl_Icon = QLabel()
        lbl_Icon.setPixmap(QPixmap(self.pixmap_path).scaled(120, 120))
        lbl_Icon.setMinimumWidth(120)
        lbl_version = QLabel('버전:')
        lbl_version_info = QLabel(f'{VERSION}')
        lbl_dev = QLabel('개발자:')
        lbl_dev_info = QLabel('안태영(Collin Ahn)')
        lbl_source = QLabel('소스코드:')
        lbl_source_url = QLabel(
            '<a href="https://github.com/collinahn/pic-organizer">https://github.com/collinahn/pic-organizer</a>')
        lbl_source_url.setOpenExternalLinks(True)
        lbl_contact = QLabel('연락처:')
        lbl_contact_info = QLabel('collinahn@hufs.ac.kr')
        lbl_license = QLabel('License:')
        lbl_license_info = QLabel(
            'MIT License \nCopyright (c) 2022 Collin Ahn')

        self.btn_exit = QPushButton('확인')
        self.btn_exit.clicked.connect(self.on_click_out)

        lbl_version.setAlignment(Qt.AlignmentFlag.AlignTop)
        lbl_dev.setAlignment(Qt.AlignmentFlag.AlignTop)
        lbl_source.setAlignment(Qt.AlignmentFlag.AlignTop)
        lbl_contact.setAlignment(Qt.AlignmentFlag.AlignTop)
        lbl_license.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(lbl_Icon, 0, 0, 6, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(lbl_version, 0, 1)
        layout.addWidget(lbl_version_info, 0, 2)
        layout.addWidget(lbl_dev, 1, 1)
        layout.addWidget(lbl_dev_info, 1, 2)
        layout.addWidget(lbl_source, 2, 1)
        layout.addWidget(lbl_source_url, 2, 2)
        layout.addWidget(lbl_contact, 3, 1)
        layout.addWidget(lbl_contact_info, 3, 2)
        layout.addWidget(lbl_license, 5, 1)
        layout.addWidget(lbl_license_info, 5, 2)
        layout.addWidget(self.btn_exit, 5, 3)

    def on_click_out(self):
        self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    i = ProgramInfoDialog()
    i.exec()
