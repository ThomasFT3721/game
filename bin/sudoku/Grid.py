from .Cell import Cell


class Grid:
    def __init__(self, size: int):
        self.cells = [[Cell(x, y) for x in range(size)] for y in range(size)]
        self.size = size
