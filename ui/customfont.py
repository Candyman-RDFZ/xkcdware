from PySide6.QtGui import QFont

class XKCDfont(QFont):
    def __init__(self):
        super().__init__('Arial')
        self.setPixelSize(16)
        self.setCapitalization(QFont.Capitalization.SmallCaps)