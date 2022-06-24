from PyQt6.QtCore import (
    Qt,
    QObject
)
from PyQt6.QtWidgets import (
    QDialog, 
    QMainWindow, 
    QWidget
)


class DraggableMainWindow(QMainWindow):
    def mousePressEvent(self, event) :
        if event.button() == Qt.MouseButton.LeftButton :
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) :
        try:
            if self.offset is not None and event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.pos() - self.offset)
            else:
                super().mouseMoveEvent(event)
        except Exception:
            ...

    def mouseReleaseEvent(self, event) :
        self.offset = None
        super().mouseReleaseEvent(event)


class DraggableWidget(QWidget):
    def mousePressEvent(self, event) :
        if event.button() == Qt.MouseButton.LeftButton :
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) :
        try:
            if self.offset is not None and event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.pos() - self.offset)
            else:
                super().mouseMoveEvent(event)
        except Exception:
            ...

    def mouseReleaseEvent(self, event) :
        self.offset = None
        super().mouseReleaseEvent(event)


class DraggableDialog(QDialog):
    def mousePressEvent(self, event) :
        if event.button() == Qt.MouseButton.LeftButton :
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) :
        try:
            if self.offset is not None and event.buttons() == Qt.MouseButton.LeftButton:
                self.move(self.pos() + event.pos() - self.offset)
            else:
                super().mouseMoveEvent(event)
        except Exception:
            ...

    def mouseReleaseEvent(self, event) :
        self.offset = None
        super().mouseReleaseEvent(event)