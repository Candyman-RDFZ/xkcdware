from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

class XKCDware(QMainWindow):
    def __init__(self):
        super().__init__()

app = QApplication()

xkcdware = XKCDware()
xkcdware.show()

app.exec()