from platform import system
from pathlib import Path
import sys

APPNAME = 'xkcdware'
APPVERSION = '1.0.0'
APPID = 'Candyman.xkcdware'

PLATFORM = system()
ASEXE = getattr(sys, 'frozen', False)
if ASEXE:
    ROOTDIR = Path(sys.executable).parent
else:
    ROOTDIR = Path(__file__).parent.parent

ICON = str(ROOTDIR / 'assets/icon.png')

TITLEIMG = str(ROOTDIR / 'assets/xkcd.png')
BROWSERIMG = str(ROOTDIR / 'assets/browser.png')
BROWSERHIMG = str(ROOTDIR / 'assets/browserh.png')
DOWNLOADIMG = str(ROOTDIR / 'assets/download.png')
DOWNLOADHIMG = str(ROOTDIR / 'assets/downloadh.png')