from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl, QEventLoop

class ComicDataManager:
	def __init__(self, parent):
		self.manager = QNetworkAccessManager(parent)

	def getComicData(self, url):
		"""
		Fetch the contents of the URL specified.
		
		Returns:
			bytes: the responce body.
			if unsuccessful, returns None
		"""
		request = QNetworkRequest(QUrl(url))
		reply = self.manager.get(request)
		loop = QEventLoop()
		reply.finished.connect(loop.quit)
		loop.exec()

		if reply.error() != QNetworkReply.NoError:
			reply.deleteLater()
			return None

		data = bytes(reply.readAll())
		reply.deleteLater()
		return data
