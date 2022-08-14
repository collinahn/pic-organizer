
import sys
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


class ProgressWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.WindowType.Widget)

        self.title = '진행률 알림'

        self.init_widget()

    def init_widget(self):
        self.setWindowTitle(self.title)
        self.box_layout = QBoxLayout(
            QBoxLayout.Direction.TopToBottom, parent=self)
        self.setLayout(self.box_layout)

        self.progress_hint = QLabel()
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.box_layout.addWidget(self.progress_hint)
        self.box_layout.addWidget(self.progress_bar)

    def update_progress(self, val: int):
        self.progress_bar.setValue(val)

    def update_hint(self, hint: str):
        self.progress_hint.setText(hint)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    bar = ProgressWidget()
    bar.show()

    bar.update_progress(10)
    exit(app.exec())
