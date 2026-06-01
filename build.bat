@echo off
pyinstaller -w --add-data "icon.png;." --add-data "xkcd.png;." --name="xkcdware" --icon=icon.ico main.py