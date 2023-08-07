from bin.sudoku.Cell import Cell


class PairCell:

    def __init__(self, cell1: Cell, cell2: Cell, possible_values: tuple[int, int]):
        self.cell1 = cell1
        self.cell2 = cell2
        self.possible_values = possible_values
