from PySide6.QtCore import QStandardPaths, QSettings
from PySide6.QtWidgets import QFileDialog
from io import BytesIO
from PIL import Image
from pathlib import Path

from core.config import DATA_FORMATS, IMG_FORMATS

def downloadData(res, currentComicData, useNativeDialog):
	dataText = str(currentComicData)

	settings = QSettings()
	lastDir = settings.value('data_last_save_dir', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
	if not useNativeDialog:
		filename, _ = QFileDialog.getSaveFileName(None, 'Save xkcd comic #' + res + ' data', lastDir + '/xkcd_' + res + '.json', ';;'.join(DATA_FORMATS.keys()), options=QFileDialog.DontUseNativeDialog)
	else:
		filename, _ = QFileDialog.getSaveFileName(None, 'Save xkcd comic #' + res + ' data', lastDir + '/xkcd_' + res + '.json', ';;'.join(DATA_FORMATS.keys()))
	if filename:
		settings.setValue('data_last_save_dir', str(Path(filename).parent))
		with open(filename, 'w', encoding='utf-8') as file:
			file.write(dataText + '\n')
	
def downloadImage(res, imgData, useNativeDialog):
	tmp = Image.open(BytesIO(imgData))

	settings = QSettings()
	lastDir = settings.value('img_last_save_dir', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation))
	if not useNativeDialog:
		filename, fmt = QFileDialog.getSaveFileName(None, 'Save xkcd comic #' + res + ' image', lastDir + '/xkcd_' + res + '.jpeg', ';;'.join(IMG_FORMATS.keys()), options=QFileDialog.DontUseNativeDialog)
	else:
		filename, fmt = QFileDialog.getSaveFileName(None, 'Save xkcd comic #' + res + ' image', lastDir + '/xkcd_' + res + '.jpeg', ';;'.join(IMG_FORMATS.keys()))
	if filename:
		ext = IMG_FORMATS[fmt]
		settings.setValue('img_last_save_dir', str(Path(filename).parent))
		tmp.save(filename, format=ext)
