import os

os.system('rm -rf build')
os.system('rm -rf dist')
os.system('pyinstaller xkcdware.spec')
