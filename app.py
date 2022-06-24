import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QAction

from qt.draggable import DraggableMainWindow
from qt.dialogs.program_info import ProgramInfoDialog
from qt.widgets.main_widget import MainUI
from utils.qt_utils import resource_path

'''
build on windows: 
pyinstaller --onefile --noconsole --icon=./icons/thanos.ico --add-data "icons/thanos.ico;./icons" --add-data "icons/thanos.png;./icons" --add-data "icons/guntlet.png;./icons" --add-data "icons/mind_stone.png;./icons" --add-data "icons/power_stone.png;./icons" --add-data "icons/reality_stone.png;./icons" --add-data "icons/space_stone.png;./icons" --add-data "icons/time_stone.png;./icons" -n Thanos app.py
build on mac: 
pyinstaller --windowed --noconfirm --hiddenimport=PyQt6.sip --icon=./icons/thanos.ico --add-data "icons/thanos.ico:./icons" --add-data "icons/thanos.png:./icons" --add-data "icons/guntlet.png:./icons" --add-data "icons/mind_stone.png:./icons" --add-data "icons/power_stone.png:./icons" --add-data "icons/reality_stone.png:./icons" --add-data "icons/space_stone.png:./icons" --add-data "icons/time_stone.png:./icons" -n Thanos app.py 
'''

class FileApp(DraggableMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.title = '파일 중복 제거'
        self.icon = QIcon(resource_path(relative_path='icons/thanos.ico'))
        self.info_icon = QIcon(resource_path(relative_path='icons/time_stone.png'))
        self.exit_icon = QIcon(resource_path(relative_path='icons/power_stone.png'))

        self._init_ui()
    
    def _init_ui(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)

        main_wigdet = MainUI()
        self.setCentralWidget(main_wigdet)

        action_info = QAction(self.info_icon, '정보', self)
        action_info.triggered.connect(self._on_info_modal)
        action_exit = QAction(self.exit_icon, '종료', self)
        action_exit.triggered.connect(QApplication.exit)

        menu = self.menuBar()

        exec_menu = menu.addMenu('실행')
        exec_menu.addAction(action_info)
        exec_menu.addSeparator()
        exec_menu.addAction(action_exit)

        self.show()

    def _on_info_modal(self):
        ProgramInfoDialog().exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileApp()
    sys.exit(app.exec())