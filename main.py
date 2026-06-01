from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import *

from core.config import APPID, PLATFORM
from core.config import ICON, TITLEIMG

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
        self.WIDTH = self.HEIGHT = SCREENSIZE.height() * 8 // 9
        self.setGeometry((SCREENSIZE.width() - self.WIDTH) // 2 + SCREENSIZE.x(), (SCREENSIZE.height() - self.HEIGHT) // 2 + SCREENSIZE.y(), self.WIDTH, self.HEIGHT)

        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(self.p)

        self.mainLayout = QVBoxLayout()

        ## Start Title Section
        self.titleImagePixmap = QPixmap(TITLEIMG)
        self.titleImagePixmap = self.titleImagePixmap.scaledToHeight(self.HEIGHT // 12)
        self.titleImageLabel = QLabel()
        self.titleImageLabel.setPixmap(self.titleImagePixmap)
        # self.titleImageLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.mainLayout.addWidget(self.titleImageLabel, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        ## End Title Section

        ## Start First Horizontal Separator

        self.separator1 = QFrame()
        self.separator1.setFrameShape(QFrame.HLine)

        self.mainLayout.addWidget(self.separator1, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(10)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

app = QApplication()
app.setWindowIcon(QIcon(ICON))

xkcdware = XKCDware()
xkcdware.show()

app.exec()