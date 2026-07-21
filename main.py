from PySide6.QtCore import Qt, QUrl, QSettings, QStandardPaths
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices
from PySide6.QtWidgets import *
from pathlib import Path
import json

from core.config import APPID, PLATFORM, APPORG, APPNAME
from core.config import ICON, TITLEIMG, BROWSERIMG, BROWSERHIMG, DOWNLOADIMG, DOWNLOADHIMG
from core.status import Status

from core.comic.matcher import match_comic
from core.comic.data import ComicDataManager

from ui.customfont import XKCDfont
from ui.custombutton import XKCDbutton

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
		self.WIDTH = self.HEIGHT = SCREENSIZE.height() * 7 // 8
		self.setGeometry((SCREENSIZE.width() - self.WIDTH) // 2 + SCREENSIZE.x(), (SCREENSIZE.height() - self.HEIGHT) // 2 + SCREENSIZE.y(), self.WIDTH, self.HEIGHT)

		self.comicDataManager = ComicDataManager(self)
		self.currentComicData = ''
		self.latestComicData = self.comicDataManager.getComicData('https://xkcd.com/info.0.json')
		
		while self.latestComicData is None:
			dialog = QMessageBox(self)
			dialog.setWindowTitle('Error')
			dialog.setText('Error while connecting to xkcd.com to retrieve latest comic data.')
			dialog.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok)
			choice = dialog.exec()
			if choice == QMessageBox.Retry:
				self.latestComicData = self.comicDataManager.getComicData('https://xkcd.com/info.0.json')
			else:
				sys.exit()
		self.latestComicData = json.loads(self.latestComicData.decode('utf-8'))

		self.p = self.palette()
		self.p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(self.p)

		self.mainLayout = QVBoxLayout()

		## Start Title Section
		self.titleImagePixmap = QPixmap(TITLEIMG)
		self.titleImagePixmap = self.titleImagePixmap.scaledToHeight(self.HEIGHT // 15)
		self.titleImageLabel = QLabel(self)
		self.titleImageLabel.setPixmap(self.titleImagePixmap)
		self.titleImageLabel.setCursor(Qt.CursorShape.PointingHandCursor)
		self.titleImageLabel.mousePressEvent = self.pressTitle

		self.mainLayout.addWidget(self.titleImageLabel, alignment=Qt.AlignmentFlag.AlignHCenter)
		## End Title Section

		## Start First Horizontal Separator

		self.separator1 = QFrame()
		self.separator1.setFrameShape(QFrame.HLine)

		self.mainLayout.addWidget(self.separator1)
		## End First Horizontal Separator

		## Start Navigation Menu

		self.navLayout = QVBoxLayout()
		self.navLayout.setSpacing(5)

		# Start Jump Area
		self.jumpLayout = QHBoxLayout()

		# Entry
		self.jumpEntry = QLineEdit(self, placeholderText='Enter comic id or URL:')
		self.jumpEntry.setFont(XKCDfont())
		self.jumpLayout.addWidget(self.jumpEntry)

		# Jump button
		self.jumpButton = XKCDbutton('Jump', 'Jump to this comic in xkcdware')
		self.jumpLayout.addWidget(self.jumpButton)

		# Open in browser button
		self.openBrowserButton = XKCDbutton('', 'Open this comic in the web browser', BROWSERHIMG, BROWSERIMG)
		self.openBrowserButton.setIcon(QIcon(BROWSERIMG))
		self.openBrowserButton.clicked.connect(lambda: self.openComicInBrowser(self.jumpEntry.text()))
		self.jumpLayout.addWidget(self.openBrowserButton)
		self.jumpLayout.setContentsMargins(0, 1, 0, 1)

		self.jumpWidget = QWidget()
		self.jumpWidget.setLayout(self.jumpLayout)
		self.jumpWidget.setFixedWidth(self.WIDTH * 2 // 3)
		self.navLayout.addWidget(self.jumpWidget, alignment=Qt.AlignmentFlag.AlignHCenter)

		# End Jump Area

		# Start xkcd Navigation Menu

		self.xkcdLayout = QHBoxLayout()

		# |<
		self.toLeastButton = XKCDbutton('|<', 'Jump to the first comic')
		self.xkcdLayout.addWidget(self.toLeastButton)

		# < Prev
		self.previousButton = XKCDbutton('< Prev', 'Jump to the previous comic')
		self.xkcdLayout.addWidget(self.previousButton)

		# Random
		self.randomButton = XKCDbutton('Random', 'Jump to a random comic')
		self.xkcdLayout.addWidget(self.randomButton)

		# Next >
		self.nextButton = XKCDbutton('Next >', 'Jump to the next comic')
		self.xkcdLayout.addWidget(self.nextButton)

		# >|
		self.toLatestButton = XKCDbutton('>|', 'Jump to the latest comic')
		self.xkcdLayout.addWidget(self.toLatestButton)

		self.xkcdLayout.setContentsMargins(0, 1, 0, 1)
		self.xkcdWidget = QWidget()
		self.xkcdWidget.setLayout(self.xkcdLayout)
		self.xkcdWidget.setFixedWidth(self.WIDTH * 1 // 2)
		self.navLayout.addWidget(self.xkcdWidget, alignment=Qt.AlignmentFlag.AlignHCenter)

		# End xkcd Navigation Menu

		# Start Advanced Menu

		self.advancedLayout = QHBoxLayout()

		# Data download

		self.dataDownloadButton = XKCDbutton('Data', 'Download the data of the current comic', DOWNLOADHIMG, DOWNLOADIMG)
		self.dataDownloadButton.clicked.connect(lambda: self.dataDownload(self.jumpEntry.text()))
		self.advancedLayout.addWidget(self.dataDownloadButton)

		# Explanation

		self.explanationButton = XKCDbutton('Explanation', 'Open the explanation in explainxkcd')
		self.explanationButton.clicked.connect(lambda: self.openExplanation(self.jumpEntry.text()))
		self.advancedLayout.addWidget(self.explanationButton)

		# Image download

		self.imageDownloadButton = XKCDbutton('Image', 'Download the image of the current comic', DOWNLOADHIMG, DOWNLOADIMG)
		self.advancedLayout.addWidget(self.imageDownloadButton)

		self.advancedLayout.setContentsMargins(0, 1, 0, 1)
		self.advancedWidget = QWidget()
		self.advancedWidget.setLayout(self.advancedLayout)
		self.advancedWidget.setFixedWidth(self.WIDTH * 2 // 5)
		self.navLayout.addWidget(self.advancedWidget, alignment=Qt.AlignmentFlag.AlignHCenter)

		## End Navigation Menu

		self.mainLayout.addLayout(self.navLayout)

		self.mainLayout.setContentsMargins(0, 0, 0, 0)
		self.mainLayout.setSpacing(5)
		self.mainLayout.addStretch()
		self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.mainWidget = QWidget()
		self.mainWidget.setLayout(self.mainLayout)
		self.setCentralWidget(self.mainWidget)

	def pressTitle(self, event):
		if event.button() == Qt.LeftButton:
			x = event.position().x()
			if x < self.titleImageLabel.width() // 2:
				QDesktopServices.openUrl(QUrl('https://xkcd.com'))
			else:
				QDesktopServices.openUrl(QUrl('https://github.com/Candyman-RDFZ/xkcdware'))

	def checkComicValidity(self, text):
		res = match_comic(text)
		if res is None:
			dialog = QMessageBox(self)
			dialog.setWindowTitle('Error')
			dialog.setText('Please enter a valid comic number or URL.')
			dialog.setStandardButtons(QMessageBox.Ok)
			dialog.setIcon(QMessageBox.Critical)
			dialog.exec()
			return Status.FAIL
		
		if self.currentComicData == '':
			self.currentComicData = self.comicDataManager.getComicData('https://xkcd.com/' + str(res) + '/info.0.json')
			while self.currentComicData is None:
				dialog = QMessageBox(self)
				dialog.setWindowTitle('Error')
				dialog.setText('Error while connecting to xkcd.com to retrieve current comic data.')
				dialog.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok)
				choice = dialog.exec()
				if choice == QMessageBox.Retry:
					self.currentComicData = self.comicDataManager.getComicData('https://xkcd.com/info.0.json')
				else:
				  sys.exit()
			if isinstance(self.currentComicData, bytes):
				self.currentComicData = self.currentComicData.decode('utf-8')
		else:
			currentComicNum = int(json.loads(self.currentComicData)['num'])
			if currentComicNum != int(res):
				self.currentComicData = self.comicDataManager.getComicData('https://xkcd.com/' + str(res) + '/info.0.json')
				while self.currentComicData is None:
					dialog = QMessageBox(self)
					dialog.setWindowTitle('Error')
					dialog.setText('Error while connecting to xkcd.com to retrieve current comic data.')
					dialog.setStandardButtons(QMessageBox.Retry | QMessageBox.Ok)
					choice = dialog.exec()
					if choice == QMessageBox.Retry:
						self.currentComicData = self.comicDataManager.getComicData('https://xkcd.com/info.0.json')
					else:
						 sys.exit()
			if isinstance(self.currentComicData, bytes):
				self.currentComicData = self.currentComicData.decode('utf-8')

		latestComicIndex = int(self.latestComicData['num'])
		if res < 1 or res > latestComicIndex:
			dialog = QMessageBox(self)
			dialog.setWindowTitle('Error')
			dialog.setText('Please enter a valid comic number or URL.')
			dialog.setStandardButtons(QMessageBox.Ok)
			dialog.setIcon(QMessageBox.Critical)
			dialog.exec()
			return Status.FAIL
		return str(res)
	
	def openComicInBrowser(self, text):
		while True:
			res = self.checkComicValidity(text)
			if res == Status.FAIL:
				self.jumpEntry.setText('')
				return
			elif res == Status.RETRY:
				continue
			else:
				QDesktopServices.openUrl(QUrl('https://xkcd.com/' + res))
				return

	def openExplanation(self, text):
		while True:
			res = self.checkComicValidity(text)
			if res == Status.FAIL:
				self.jumpEntry.setText('')
				return
			elif res == Status.RETRY:
				continue
			else:
				QDesktopServices.openUrl(QUrl('https://explainxkcd.com/' + res))
				return

	def dataDownload(self, text):
		res = ''
		while True:
			res = self.checkComicValidity(text)
			if res == Status.FAIL:
				self.jumpEntry.setText('')
				return
			elif res == Status.RETRY:
				continue
			else:
				break
		
		dataText = self.currentComicData

		settings = QSettings()
		lastDir = settings.value('last_save_dir', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
		filename, _ = QFileDialog.getSaveFileName(self, 'Save xkcd comic #' + res + ' data', lastDir + '/xkcd_' + res + '.json', 'JSON Files (*.json);;Text Files (*.txt)')
		if filename:
			settings.setValue('last_save_dir', str(Path(filename).parent))
			with open(filename, 'w', encoding='utf-8') as file:
				file.write(dataText + '\n')


app = QApplication()
app.setOrganizationName(APPORG)
app.setApplicationName(APPNAME)
app.setWindowIcon(QIcon(ICON))

xkcdware = XKCDware()
xkcdware.show()

app.exec()
