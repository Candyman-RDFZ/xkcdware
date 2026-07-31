from PySide6.QtCore import QEvent, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QLabel, QToolTip

class XKCDwareTitle(QLabel):
	def event(self, event):
		if event.type() == QEvent.ToolTip:
			x = event.pos().x()
			if x < self.width() * 175 // 326:
				text = 'A webcomic of romance, sarcasm, math, and language.'
			else:
				text = 'And a fast and reliable way to view it right on your desktop.'
			QToolTip.showText(event.globalPos(), text, self)
			return True
		return super().event(event)

	def mousePressEvent(self, event):
		x = event.pos().x()
		if x < self.width() * 175 // 326:
			QDesktopServices.openUrl(QUrl('https://xkcd.com'))
		else:
			QDesktopServices.openUrl(QUrl('https://github.com/Candyman-RDFZ/xkcdware'))
		return super().mousePressEvent(event)
