from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QSizePolicy

from ui.customfont import XKCDfont

class XKCDbutton(QPushButton):
    def __init__(self, text, tooltip, hoverIcon=None, normalIcon=None):
        super().__init__()
        self.setText(text)
        self.setToolTip(tooltip)
        if hoverIcon is not None:
            self.normalIcon = QIcon(normalIcon)
            self.hoverIcon = QIcon(hoverIcon)
            self.setIcon(self.normalIcon)
            self.setIconSize(QSize(18, 18))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet('''
            XKCDbutton {
                background-color: #6E7B91;
                color: #FFF;
                border: 1.5px solid #333;
                border-radius: 3px;
                padding: 0.5px 8px;
                font-weight: 600;
            }
            XKCDbutton:hover {
                background-color: #FFF;
                color: #6E7B91;
            }
        ''')
        self.setFont(XKCDfont())
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    def enterEvent(self, event):
        try:
            self.setIcon(self.hoverIcon)
        except: pass
        return super().enterEvent(event)
    def leaveEvent(self, event):
        try:
            self.setIcon(self.normalIcon)
        except: pass
        return super().leaveEvent(event)