from PySide6.QtGui import QFont

class XKCDfont(QFont):
    def __init__(self, fontsize=16):
        super().__init__('Arial')
        self.setPixelSize(fontsize)
        self.setCapitalization(QFont.Capitalization.SmallCaps)
