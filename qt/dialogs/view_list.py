import sys
from PyQt6.QtWidgets import QGridLayout 
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QGroupBox
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtGui import QIcon

from folder_utils.browse import Browser
from qt.stylesheets import flat_push_button
from utils.qt_utils import resource_path

class ViewListDialog(QDialog):
    def __init__(self, file_list, file_valid):
        super().__init__()

        self.title: str = '파일 확인하기'
        self.icon = QIcon(resource_path(relative_path='icons/thanos.png'))
        self.data: list[tuple[str]] = file_list
        self.meta_data: list[bool] = file_valid
        self.current_file: str = ''

        self._init_ui()


    def _init_ui(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setMinimumWidth(1200)
        self.setMinimumHeight(400)

        dialog_layout = QGridLayout()
        self.setLayout(dialog_layout)

        lbl_explain = QLabel('파일명을 클릭하면 사진을 확인할 수 있습니다. 미리보기를 더블 클릭하면 해당 폴더로 이동합니다.')
        
        #스크롤 바 영역
        widget_file_list = QWidget()
        layout_file_list = QVBoxLayout()
        widget_file_list.setLayout(layout_file_list)
        layout_file_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        for idx_group, overlapped in enumerate(self.data):
            #중복 파일을 그룹으로 묶어서 위젯에 추가한다
            group_overlapped = QGroupBox()
            layout_overlapped = QGridLayout()
            group_overlapped.setLayout(layout_overlapped)

            chkbox_flag = QCheckBox(f'{idx_group+1}')
            if self.meta_data[idx_group]: chkbox_flag.setChecked(True)
            chkbox_flag.toggled.connect(self.on_chkbox_toggle)
            layout_overlapped.addWidget(chkbox_flag, 0, 0, 100, 1, alignment=Qt.AlignmentFlag.AlignVCenter)

            for idx_fname, file in enumerate(overlapped):
                btn_filename = QPushButton(f'{file}', flat=True)
                btn_filename.setStyleSheet(flat_push_button)
                btn_filename.clicked.connect(self.on_btn_filename)
                layout_overlapped.addWidget(btn_filename, idx_fname, 1, 1, 100, alignment=Qt.AlignmentFlag.AlignLeft)
                layout_overlapped.setSpacing(0)

            layout_overlapped.setAlignment(Qt.AlignmentFlag.AlignTop)
            layout_file_list.addWidget(group_overlapped)

        self.scroll_files_view = QScrollArea()
        self.scroll_files_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_files_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_files_view.setWidgetResizable(True)
        self.scroll_files_view.setMaximumHeight(500)
        self.scroll_files_view.setMinimumWidth(600)
        self.scroll_files_view.setWidget(widget_file_list)
        #스크롤 바 영역
        
        self.pixmap_preview = QLabel('미리보기 영역입니다.')
        self.pixmap_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pixmap_preview.setFixedSize(self.scroll_files_view.width(), self.scroll_files_view.height())
        self.pixmap_preview.mouseDoubleClickEvent = self.on_doubleclick_pixmap

        btn_exit = QPushButton('나가기')
        btn_exit.setMaximumWidth(70)
        btn_exit.clicked.connect(self.close)
        btn_exit.setDefault(True)

        dialog_layout.addWidget(lbl_explain, 0, 0, 1, 2)
        dialog_layout.addWidget(self.scroll_files_view, 1, 0)
        dialog_layout.addWidget(self.pixmap_preview, 1, 1)
        dialog_layout.addWidget(btn_exit, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)
        

    def on_btn_filename(self):
        try:
            file_name = self.sender().text()
            self.current_file = file_name # 상태 저장
        except AttributeError as e:
            print(e)
            return
        
        ref_size = (self.scroll_files_view.width(), self.scroll_files_view.height())
        self.pixmap_preview.setMaximumSize(*ref_size)
        self.pixmap_preview.setPixmap(QPixmap(self.current_file).scaled(*ref_size, Qt.AspectRatioMode.KeepAspectRatio))
        if self.pixmap_preview.pixmap().isNull():
            self.pixmap_preview.setText('지원하지 않는 파일 형식입니다.\n이 영역을 더블 클릭하면 해당 폴더로 이동합니다.')
                

    def on_doubleclick_pixmap(self, event: QMouseEvent):
        if self.current_file:
            Browser.open_folder(path=self.current_file)

    def on_chkbox_toggle(self):
        chkbox: QCheckBox = self.sender()

        try:
            idx = int(chkbox.text())
        except AttributeError as e:
            print(e)
            return

        self.meta_data[idx-1] = bool(chkbox.isChecked())





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ViewListDialog([('123','1234'),('123456','12343535','123424123424123424123424123424123424123424123424123424123424123424123424123424123424123424123424123424123424','12313213'),], [True, True]).exec()
    sys.exit(app.exec())