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

ICON = str(ROOTDIR / 'icon.ico')