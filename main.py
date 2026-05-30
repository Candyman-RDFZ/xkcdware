from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *

from core.config import APPID, PLATFORM
from core.config import ICON

if PLATFORM == 'Windows':
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(APPID)
    except: pass

class XKCDware(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('xkcdware') # Window Title
        SCREENSIZE = QApplication.instance().primaryScreen().geometry()
        WIDTH = HEIGHT = SCREENSIZE.height() * 8 // 9
        self.setGeometry((SCREENSIZE.width() - WIDTH) // 2 + SCREENSIZE.x(), (SCREENSIZE.height() - HEIGHT) // 2 + SCREENSIZE.y(), WIDTH, HEIGHT)


app = QApplication()
app.setWindowIcon(QIcon(ICON))

xkcdware = XKCDware()
xkcdware.show()

app.exec()