import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QProgressBar

from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt

class ProgressBarTimer(QWidget):
    def __init__(self, shared_mem: list, Parent=None):
        super(ProgressBarTimer, self).__init__(Parent)

        self.title = '진행 위젯'
        self.label = '폴더 탐색 중'

        self.shared_mem = shared_mem
        self.total_count = self._setup_numbers()

        self._setup_UI()

        self.timer = QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self._update)
        self.timer.start()

    def _setup_numbers(self):
        try:
            return sum(( store.count for store in self.shared_mem ))
        except AttributeError:
            return -1

    def _current_status(self):
        try:
            return sum(( store.status for store in self.shared_mem ))            
        except AttributeError:
            return -1
    
    def _setup_UI(self):
        self.setWindowTitle(self.title)

        self.comment = QLabel(self.label)
        self.comment.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.pbar = QProgressBar(self)
        self.pbar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.comment, 0, 0)
        layout.addWidget(self.pbar, 1, 0)


    def _update(self):
        progress = int(self._current_status() / self.total_count)
        print(self._current_status(), self.total_count)
        if progress == self.pbar.value():
            return

        self.pbar.setValue(progress)
        print(f'value set to {self.pbar.value()}')
        

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    pdlg = ProgressBarTimer('test')
    pdlg.show()