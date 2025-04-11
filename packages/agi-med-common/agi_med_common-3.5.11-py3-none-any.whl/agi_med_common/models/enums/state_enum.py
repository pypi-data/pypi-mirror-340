from enum import StrEnum, auto


class StateEnum(StrEnum):
    EMPTY = auto()
    ASK_FILE_AGAIN = auto()
    COLLECTION = auto()
    READINESS = auto()
    FINAL = auto()
    ERROR = auto()
