class Coordinate:

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __str__(self):
        return f'(row={self.row}, col={self.col})'
