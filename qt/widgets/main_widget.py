import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
from PyQt6.QtCore import QObject
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QFileDialog 
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QApplication 

from folder_utils.base_folder import BaseFolder
from folder_utils.base_folder import GlobalBaseFolder
from folder_utils.file_list import FileList
from file_utils.compare import CompareFile
from file_utils.delete import DeleteFileStrategy
from qt.dialogs.default import DefaultDialog
from qt.dialogs.view_list import ViewListDialog
from qt.widgets.progress import ProgressWidget
from qt.stylesheets import main_wigdet_stylesheet
from utils.qt_utils import resource_path

class MainUI(QWidget):
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.guntlet_icon = QIcon(resource_path(relative_path='icons/guntlet.png'))

        self._init_ui()


        self._base = BaseFolder('')
        self.final_res: list[tuple[str]] = []
        self.del_flag: list[bool] = []

    def _init_ui(self):
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.setStyleSheet(main_wigdet_stylesheet)

        #경로 설정
        self.btn_set_dir = QPushButton('여기를 눌러 폴더를 지정해주세요')
        self.btn_set_dir.clicked.connect(self.on_btn_set_dir)
        self.btn_set_dir.setMinimumHeight(40)
        self.btn_set_dir.setMinimumWidth(340)

        #분석시작 버튼
        self.btn_start_diagnose = QPushButton('분석하기')
        self.btn_start_diagnose.clicked.connect(self.on_btn_start_diagnose)
        self.btn_start_diagnose.setMinimumHeight(40)
        self.btn_start_diagnose.setEnabled(False)

        #분석결과 요약
        self.lbl_result_short = QLabel('')
        self.lbl_result_short.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #분석결과 상세
        self.btn_result_detail = QPushButton('목록 보기')
        self.btn_result_detail.setMinimumHeight(40)
        self.btn_result_detail.setEnabled(False)
        self.btn_result_detail.clicked.connect(self.on_btn_view_list)

        #완료 버튼 설명(분석 완료시 등장)
        self.lbl_explain_final_btn = QLabel('')
        self.lbl_explain_final_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_delete_overlapped = QPushButton('정리하기')
        self.btn_delete_overlapped.setMinimumHeight(50)
        self.btn_delete_overlapped.setEnabled(False)
        self.btn_delete_overlapped.clicked.connect(self.delete_all)

        self.main_layout.addWidget(self.btn_set_dir, 0, 0)
        self.main_layout.addWidget(self.btn_start_diagnose, 0, 1)
        self.main_layout.addWidget(self.lbl_result_short, 1, 0)
        self.main_layout.addWidget(self.btn_result_detail, 1, 1)
        self.main_layout.addWidget(self.lbl_explain_final_btn, 2, 0)
        self.main_layout.addWidget(self.btn_delete_overlapped, 2, 1)
        
        self.progress_update_widget = ProgressWidget()
        self.progress_delete_widget = ProgressWidget()

    def on_btn_set_dir(self):

        self._base = BaseFolder(str(QFileDialog.getExistingDirectory(self, "기준 폴더를 선택하세요") or self._base.path))
        # print(f'{self._base} selected')

        if self._base.path:
            self.btn_set_dir.setText(self._base.path)
            self.btn_start_diagnose.setText('분석하기')
            self.btn_start_diagnose.setEnabled(True)
            self.btn_result_detail.setEnabled(False)
            self.btn_delete_overlapped.setText('정리하기')
            self.btn_delete_overlapped.setIconSize(QSize(0,0))
            self.btn_delete_overlapped.setEnabled(False)
            self.lbl_explain_final_btn.setText('')
            self.lbl_result_short.setText('')

    def on_btn_start_diagnose(self):
        if not self._base.path:
            return

        file_list = FileList(self._base.path)
        cmp_file = CompareFile(file_obj=file_list)
        self._replace_widget_fm_main_layout(
            useless=self.lbl_result_short,
            useable=self.progress_update_widget,
            coord=(1, 0)
        )

        self.search_thread = QThread()
        self.search_worker = DiagnoseWorker()
        self.search_worker.moveToThread(self.search_thread)
        self.search_thread.started.connect( lambda: GlobalBaseFolder(self._base.path) )
        self.search_thread.started.connect( lambda: self.btn_start_diagnose.setText('분석 중,,') )
        self.search_thread.started.connect( lambda: self.btn_start_diagnose.setEnabled(False) )
        self.search_thread.started.connect( lambda: self.search_worker.run(file_list, cmp_file) )
        self.search_worker.progress_hint.connect(self.progress_update_widget.update_hint)
        self.search_worker.progress_int.connect(self.progress_update_widget.update_progress)

        self.search_thread.start()


        self.search_thread.finished.connect(
            lambda: self._search_result(cmp_file)
        )
        self.search_thread.finished.connect(
            lambda: self.btn_start_diagnose.setText('분석 완료')
        )
        self.search_thread.finished.connect(
            lambda: self.btn_start_diagnose.setEnabled(False)
        )
        self.search_thread.finished.connect(
            lambda: self.btn_result_detail.setEnabled(True)
        )
        self.search_thread.finished.connect(
            lambda: self.btn_delete_overlapped.setEnabled(True)
        )
        self.search_thread.finished.connect(
            lambda: self._replace_widget_fm_main_layout(
                useless=self.progress_update_widget,
                useable=self.lbl_result_short,
                coord=(1, 0)
            )
        )
        self.search_thread.finished.connect(
            lambda: self.lbl_result_short.setText(f'{file_list.count}개의 파일 중 {len(cmp_file.result)}건의 중복을 찾았습니다.')
        )
        self.search_worker.finished.connect(self.search_thread.quit)
        self.search_worker.finished.connect(self.search_thread.deleteLater)
        self.search_thread.finished.connect(self.search_worker.deleteLater)

    def _replace_widget_fm_main_layout(self, *, useless, useable, coord):
        self.main_layout.removeWidget(useless)
        useless.hide()
        self.main_layout.addWidget(useable, *coord)
        useable.show()
        self.main_layout.update()

    def _search_result(self, cmp_object: CompareFile):
        self.final_res: list[tuple[str]] = cmp_object.result
        self.del_flag: list[bool] = [ True for _ in cmp_object.result ]
        # print(f'total overlap: {len(cmp_object.result)}')
        # for res in cmp_object.result:
        #     print(f'{len(res)} files overlapped: {res}')
    
    def on_btn_view_list(self):
        dlg = ViewListDialog(self.final_res, self.del_flag)
        dlg.exec()
        self.final_res, self.del_flag = dlg.data, dlg.meta_data
        self.lbl_explain_final_btn.setText(f'선택된 {self.del_flag.count(True)}개의 중복을 정리합니다.')

    def delete_all(self):
        if not self.final_res:
            DefaultDialog('중복된 파일이 없습니다.', ('확인', )).exec()
            return

        dlg_ask = DefaultDialog('삭제를 시작합니다.', ('네', '아니오'))
        dlg_ask.exec()

        if dlg_ask.answer:
            self._replace_widget_fm_main_layout(
                useless=self.lbl_explain_final_btn,
                useable=self.progress_delete_widget,
                coord=(2, 0)
            )

            self.delete_thread = QThread()
            self.delete_worker = DeleteWorker(self.final_res, self.del_flag)
            self.delete_worker.moveToThread(self.delete_thread)
            self.delete_thread.started.connect(self.delete_worker.run)
            self.delete_worker.finished.connect(self.delete_thread.quit)
            self.delete_worker.finished.connect(self.delete_thread.deleteLater)
            self.delete_thread.finished.connect(self.delete_worker.deleteLater)
            self.delete_worker.progress_int.connect(self.progress_delete_widget.update_progress)
            self.delete_worker.progress_hint.connect(self.progress_delete_widget.update_hint)
            self.delete_thread.started.connect(
                lambda: self.btn_delete_overlapped.setText('')
            )
            self.delete_thread.started.connect(
                lambda: self.btn_delete_overlapped.setIcon(self.guntlet_icon)
            )
            self.delete_thread.started.connect(
                lambda: self.btn_delete_overlapped.setIconSize(QSize(49,49))
            )
            self.delete_thread.start()

            self.delete_thread.finished.connect(
                lambda: DefaultDialog('처리를 완료하였습니다.', ('네', )).exec()
            )
            self.delete_thread.finished.connect(
                lambda: self.lbl_explain_final_btn.setText('')
            )
            self.delete_thread.finished.connect(
                lambda: self.lbl_result_short.setText('')
            )
            self.delete_thread.finished.connect(
                lambda: self._replace_widget_fm_main_layout(
                    useless=self.progress_delete_widget,
                    useable=self.lbl_explain_final_btn,
                    coord=(2, 0)
                )
            )


class DiagnoseWorker(QObject):
    finished = pyqtSignal()
    progress_hint = pyqtSignal(str)
    progress_int = pyqtSignal(int)

    def run(self, file_object:FileList, cmp_object: CompareFile):
        self.progress_hint.emit('초기화 중...')
        QTest.qWait(100)
        file_object.lazy_init()
        QTest.qWait(100)
        cmp_object.lazy_init(self.progress_hint, self.progress_int)
        QTest.qWait(100)

        self.finished.emit()

class DeleteWorker(QObject):
    finished = pyqtSignal()
    progress_hint = pyqtSignal(str)
    progress_int = pyqtSignal(int)

    def __init__(self, target_files, delete_flag, parent=None) -> None:
        super().__init__(parent)

        self.target = target_files
        self.del_flag = delete_flag
        self.progress_hint.emit('파일 삭제 중')
        QTest.qWait(100)

    def run(self):
        delete_file = DeleteFileStrategy(self.target, self.del_flag)
        delete_file.delete.run(self.progress_int)

        self.finished.emit()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainUI()
    ex.show()
    sys.exit(app.exec())
    
