from enum import Enum

from bin.sudoku.Coordinate import Coordinate
from bin.tools.Console import BackgroundColor, Color, Style


class Cell:
    number = 2

    def __init__(self, row: int, col: int, value: int):
        self.value = value
        self.coordinate = Coordinate(row, col)
        self.state = CellState.VALID
        if self.value != 0:
            self.given = True
            self.style = Style(Color.WHITE, BackgroundColor.DEFAULT)
            self.__possible_values = []
        else:
            self.given = False
            self.style = Style(Color.BLUE, BackgroundColor.DEFAULT, True)
            self.__possible_values = [x for x in range(1, 10)]

    def remove_possible_value(self, value: int):
        if value in self.__possible_values:
            if self.coordinate.row == 7 and self.coordinate.col == 3:
                print(f'Cell {self.coordinate} remove {value}')
            self.__possible_values.remove(value)

    def set_value(self, value: int):
        print(f'Cell {self.coordinate} set to {value}')
        self.value = value
        if self.value == 0:
            self.state = CellState.VALID
            self.__possible_values = []
            self.style.bold = True
            self.style.color = Color.RED

    def get_value_for_print(self) -> str:
        if self.value == 0:
            if self.__possible_values.__contains__(Cell.number):
                return f'{Cell.number}'
            if Cell.number is not None:
                return str(self.__possible_values.__len__())
            return ' '
        return str(self.value)

    def get_value_for_print_xl(self, number: int) -> str:
        if self.value == 0:
            if self.__possible_values.__contains__(number):
                return f'{number}'
            return ' '
        return str(self.value)

    def get_style_for_print(self) -> Style:
        if self.state == CellState.INVALID:
            return Style(self.style.color, BackgroundColor.RED)
        if Cell.number == self.value:
            if self.given:
                return Style(Color.GREEN, BackgroundColor.DEFAULT)
            else:
                return Style(Color.RED, BackgroundColor.DEFAULT)
        if self.value == 0:
            if self.__possible_values.__contains__(Cell.number):
                return Style(Color.YELLOW, BackgroundColor.DEFAULT, True)
            else:
                return Style(Color.GREY, BackgroundColor.DEFAULT)
        return self.style

    def get_style_for_print_xl(self, number: int) -> Style:
        if self.state == CellState.INVALID:
            return Style(self.style.color, BackgroundColor.RED)

        if self.value == number:
            return self.style

        if self.value != 0:
            return Style(Color.BLACK, BackgroundColor.DEFAULT)
        else:
            if self.__possible_values.__contains__(number):
                return Style(Color.YELLOW, BackgroundColor.DEFAULT, True)
            else:
                return Style(Color.GREY, BackgroundColor.DEFAULT)
        return self.style

    def is_possible_value(self, value: int) -> bool:
        return value in self.__possible_values

    def get_possible_values(self) -> list:
        return self.__possible_values

    def len_possible_values(self) -> int:
        return self.__possible_values.__len__()


class CellState(Enum):
    INVALID = -1
    VALID = 1
