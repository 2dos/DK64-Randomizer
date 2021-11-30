from enum import IntEnum, auto


class SearchMode(IntEnum):
    GetReachable = auto()
    GeneratePlaythrough = auto()
    CheckBeatable = auto()
