from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl
import json

class ComicDataManager:
    def __init__(self, parent):
        self.manager = QNetworkAccessManager(parent)

    def getLatestComicData(self, callback, key):
        rep = self.manager.get(QNetworkRequest(QUrl('https://xkcd.com/info.0.json')))
        rep.finished.connect(lambda: self._getLatestComicData(rep, callback, key))

    def _getLatestComicData(self, reply, callback, key):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            replyd = reply.readAll()
            replyStr = bytes(replyd).decode('utf-8')
            callback(json.loads(replyStr)[key])
        else:
            print(reply.error())
        reply.deleteLater()