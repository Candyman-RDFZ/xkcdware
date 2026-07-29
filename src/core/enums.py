from enum import Enum, auto

class Status(Enum):
	OK = auto()
	RETRY = auto()
	FAIL = auto()

class Operation(Enum):
	OPEN_IN_BROWSER = auto()
	OPEN_EXPLANATION = auto()
	DOWNLOAD_DATA = auto()
	DOWNLOAD_IMAGE = auto()
