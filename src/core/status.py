from enum import Enum, auto

class Status(Enum):
	OK = auto()
	RETRY = auto()
	FAIL = auto()
