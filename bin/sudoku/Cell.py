from enum import Enum

from bin.sudoku.Coordinate import Coordinate
from bin.tools.Console import BackgroundColor


class Cell:

    def __init__(self, row: int, col: int):
        self.value = 0
        self.coordinate = Coordinate(row, col)
        self.state = CellState.VALID
        self.background = BackgroundColor.DEFAULT
        self.given = False


class CellState(Enum):
    INVALID = -1
    VALID = 1
