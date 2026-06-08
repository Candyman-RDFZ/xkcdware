@echo off
pyinstaller -w --add-data "assets;assets" --name="xkcdware" --icon=icon.ico main.py