from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

def openComicInBrowser(text):
	QDesktopServices.openUrl(QUrl('https://xkcd.com/' + text))

def openExplanation(text):
	QDesktopServices.openUrl(QUrl('https://explainxkcd.com/' + text))
