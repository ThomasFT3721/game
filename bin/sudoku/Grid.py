from .Cell import Cell


class Grid:
    def __init__(self, size: int, default_values: list[list[int]]):
        self.cells = [[Cell(x, y, default_values[x][y]) for y in range(size)] for x in range(size)]
        self.size = size
