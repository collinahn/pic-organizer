from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSizePolicy


class ExpandingQPushButton(QPushButton):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)


class MaxQPushButton(QPushButton):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setSizePolicy(QSizePolicy.Policy.Maximum,
                           QSizePolicy.Policy.Maximum)
