from PySide6.QtCore import QStandardPaths, QSettings
from PySide6.QtWidgets import QFileDialog
from io import BytesIO
from PIL import Image
import re
from pathlib import Path

def downloadData(res, currentComicData, useNativeDialog):
	dataText = str(currentComicData)

	settings = QSettings()
	lastDir = settings.value('data_last_save_dir', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation))
	if not useNativeDialog:
		filename, _ = QFileDialog.getSaveFileName(None, 'Save xkcd comic #' + res + ' data', lastDir + '/xkcd_' + res + '.json', 'JSON Files (*.json);;Text Files (*.txt)', options=QFileDialog.DontUseNativeDialog)
	else:
		filename, _ = QFileDialog.getSaveFileName(None, 'Save xkcd comic #' + res + ' data', lastDir + '/xkcd_' + res + '.json', 'JSON Files (*.json);;Text Files (*.txt)')
	if filename:
		settings.setValue('data_last_save_dir', str(Path(filename).parent))
		with open(filename, 'w', encoding='utf-8') as file:
			file.write(dataText + '\n')
	
def downloadImage(res, imgData, useNativeDialog):
	tmp = Image.open(BytesIO(imgData))

	settings = QSettings()
	lastDir = settings.value('img_last_save_dir', QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation))
	if not useNativeDialog:
		filename, fmt = QFileDialog.getSaveFileName(None, 'Save xkcd comic #' + res + ' image', lastDir + '/xkcd_' + res + '.jpeg', 'JPEG Images (*.jpg  *.jpeg);;PNG Images (*.png);;GIF Images (*.gif);;BMP Images (*.bmp);;WebP Images (*.webp);;TIF Images (*.tif  *.tiff)', 'JPEG Images (*.jpg, *.jpeg)', options=QFileDialog.DontUseNativeDialog)
	else:
		filename, fmt = QFileDialog.getSaveFileName(None, 'Save xkcd comic #' + res + ' image', lastDir + '/xkcd_' + res + '.jpeg', 'JPEG Images (*.jpg  *.jpeg);;PNG Images (*.png);;GIF Images (*.gif);;BMP Images (*.bmp);;WebP Images (*.webp);;TIF Images (*.tif  *.tiff)', 'JPEG Images (*.jpg, *.jpeg)')
	if filename:
		exts = re.findall(r'\*\.([A-Za-z0-9]+)', fmt)
		ext = exts[1] if len(exts) == 2 else exts[0]
		ext = ext.upper()
		if ext == 'JPG': ext = 'JPEG'
		if ext == 'TIF': ext = 'TIFF'
		settings.setValue('img_last_save_dir', str(Path(filename).parent))
		tmp.save(filename, format=ext)
