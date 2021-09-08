from enum import Enum


class GameState(Enum):
    CREATED = 0
    STARTED = 1
    FINISHED = 2


class Formation(Enum):
    STANDARD = 0
    BELGIAN_DAISY = 1
    GERMAN_DAISY = 2
