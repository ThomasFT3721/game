from .Cell import CellState, Cell
from .Coordinate import Coordinate
from .Grid import Grid
from .tools.Printer import Printer
from ..tools.Console import Console, StyledText, Color, Style, BackgroundColor


class Sudoku:
    def __init__(self, start_grid: list[list[int]]):
        self.number_steps = 0
        self.number_loop = 0
        self.numbers = [[0, x] for x in range(1, 10)]
        self.grid = Grid(9)
        if len(start_grid) != 9:
            raise Exception("Grid size does not match")
        for y in range(9):
            if len(start_grid[y]) != 9:
                raise Exception("Grid size does not match")
            for x in range(9):
                self.grid.cells[y][x].value = start_grid[y][x]
                self.grid.cells[y][x].given = start_grid[y][x] != 0

        if not self.verify():
            self.print()
            raise Exception("Invalid start grid")

    def print(self, grid: Grid = None):
        if grid is None:
            grid = self.grid
        Printer.print(grid)

    def print_information(self):
        Console.println(StyledText("╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗", Style(Color.GREY)))
        for num in self.numbers:
            Console.print(StyledText("║ ", Style(Color.GREY)))
            Console.print(StyledText(str(num[1]), Style(Color.WHITE, bold=True)))
            Console.print(" ")
        Console.println(StyledText("║", Style(Color.GREY)))
        Console.println(StyledText("╟───╫───╫───╫───╫───╫───╫───╫───╫───╢", Style(Color.GREY)))
        for num in self.numbers:
            Console.print(StyledText("║ ", Style(Color.GREY)))
            if num[0] == 9:
                Console.print(StyledText(str(num[0]), Style(Color.WHITE)))
            else:
                Console.print(StyledText(str(num[0]), Style(Color.PURPLE)))
            Console.print(" ")
        Console.println(StyledText("║", Style(Color.GREY)))
        Console.println(StyledText("╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝", Style(Color.GREY)))

    def get_cell(self, row: int, col: int) -> Cell:
        if row < 0 or row >= 9:
            raise Exception("Row out of bounds")
        if col < 0 or col >= 9:
            raise Exception("Column out of bounds")
        return self.grid.cells[row][col]

    def set_cell(self, coordinate: Coordinate, value: int):
        if coordinate.row < 0 or coordinate.row >= 9:
            raise Exception("Row out of bounds")
        if coordinate.col < 0 or coordinate.col >= 9:
            raise Exception("Column out of bounds")
        self.grid.cells[coordinate.row][coordinate.col].value = value
        print("Loop " + str(self.number_loop) + " - Action: set cell (" + str(coordinate.row) + ", " + str(coordinate.col) + ") to " + str(value))
        self.number_steps += 1
        for i in self.numbers:
            if i[1] == value:
                i[0] += 1

    def verify(self) -> bool:
        numbers = [[0, x] for x in range(1, 10)]
        all_done = True
        for row in range(9):
            for col in range(9):
                self.grid.cells[row][col].state = self.__verify_cell(row, col)
                if self.grid.cells[row][col].state == CellState.INVALID:
                    all_done = False
                if self.grid.cells[row][col].value != 0:
                    for i in numbers:
                        if i[1] == self.grid.cells[row][col].value:
                            i[0] += 1
        self.numbers = numbers
        return all_done

    def __verify_cell(self, row: int, col: int) -> CellState:
        if self.grid.cells[row][col].value == 0:
            return self.grid.cells[row][col].state
        for i in range(9):
            if i != col and self.grid.cells[row][i].value == self.grid.cells[row][col].value:
                return self.grid.cells[row][col].state.INVALID
            if i != row and self.grid.cells[i][col].value == self.grid.cells[row][col].value:
                return self.grid.cells[row][col].state.INVALID
        for y in range(row - row % 3, row - row % 3 + 3):
            for x in range(col - col % 3, col - col % 3 + 3):
                if (y != row or x != col) and self.grid.cells[y][x].value == self.grid.cells[row][col].value:
                    return self.grid.cells[row][col].state.INVALID
        return self.grid.cells[row][col].state.VALID

    def is_done(self) -> bool:
        for row in range(9):
            for col in range(9):
                if self.grid.cells[row][col].value == 0:
                    return False
        return True

    def __have_number_in_row(self, row: int, number: int) -> bool:
        for col in range(9):
            if self.grid.cells[row][col].value == number:
                return True
        return False

    def __have_number_in_col(self, col: int, number: int) -> bool:
        for row in range(9):
            if self.grid.cells[row][col].value == number:
                return True
        return False

    def __have_number_in_3x3(self, rows: list[int], cols: list[int], number: int) -> bool:
        for row in rows:
            for col in cols:
                if self.grid.cells[row][col].value == number:
                    return True
        return False

    def number_of_available_cases_in_3x3(self, number: int, rows: list[int], cols: list[int]) -> list[Coordinate]:
        number_of_available_cases = []
        if self.__have_number_in_3x3(rows, cols, number):
            return []
        for row in rows:
            for col in cols:
                if self.grid.cells[row][col].value == number:
                    return []
                if self.grid.cells[row][col].value == 0:
                    if not (self.__have_number_in_row(row, number) or self.__have_number_in_col(col, number)):
                        number_of_available_cases.append(Coordinate(row, col))
        return number_of_available_cases

    def number_of_available_cases_in_3x3_new(self, number: int, rows: list[int], cols: list[int]) -> list[Coordinate]:
        number_of_available_cases = []
        for row in rows:
            for col in cols:
                if self.grid.cells[row][col].value == number:
                    return []
                if self.grid.cells[row][col].value == 0:
                    can_be_placed = not (self.__have_number_in_row(row, number) or self.__have_number_in_col(col, number))

                    if can_be_placed:
                        self.grid.cells[row][col].background = BackgroundColor.GREEN
                        number_of_available_cases.append(Coordinate(row, col))
                    else:
                        self.grid.cells[row][col].background = BackgroundColor.RED

        return number_of_available_cases

    def __all_cases_available_in_3x3_are_in_same_row(self, cases: list[Coordinate]) -> bool:
        row = cases[0].row
        for case in cases:
            if case.row != row:
                return False
        return True

    def __all_cases_available_in_3x3_are_in_same_column(self, cases: list[Coordinate]) -> bool:
        col = cases[0].col
        for case in cases:
            if case.col != col:
                return False
        return True

    def number_of_available_cases_in_9x9(self, i: int) -> list[Coordinate]:
        number_of_available_cases = []
        for row in range(9):
            if self.__have_number_in_row(row, i):
                continue
            for col in range(9):
                if self.__have_number_in_col(col, i):
                    continue
                coordinate = Coordinate(row, col)
                rows, cols = self.__get_rows_and_cols(coordinate)
                coordinates = self.number_of_available_cases_in_3x3(i, rows, cols)
                if coordinates.__len__() > 0:
                    if self.grid.cells[row][col].value == 0:
                        number_of_available_cases.append(coordinate)
        return number_of_available_cases

    def __filter_of_available_cases_in_9x9(self, coordinates: list[Coordinate]) -> list[Coordinate]:
        coordinates_copy = coordinates.copy()
        number_of_available_cases = coordinates.copy()
        coordinates_grouped_by_3x3 = self.__group_coordinates_by_3x3(coordinates_copy)
        for coordinates_in_3x3 in coordinates_grouped_by_3x3:
            if coordinates_in_3x3.__len__() == 0:
                continue
            if self.__all_cases_available_in_3x3_are_in_same_column(coordinates_in_3x3):
                for coo_copy in coordinates_copy:
                    if coo_copy.col == coordinates_in_3x3[0].col:
                        if coo_copy.row not in self.__get_rows_and_cols(coordinates_in_3x3[0])[0]:
                            number_of_available_cases.remove(coo_copy)
        return number_of_available_cases

    def __group_coordinates_by_3x3(self, coordinates: list[Coordinate]) -> list[list[Coordinate]]:
        coordinates_grouped_by_3x3 = [[], [], [], [], [], [], [], [], []]
        for coordinate in coordinates:
            rows, cols = self.__get_rows_and_cols(coordinate)
            coordinates_grouped_by_3x3[rows[0] // 3 * 3 + cols[0] // 3].append(coordinate)
        return coordinates_grouped_by_3x3

    def number_of_available_cases_in_row_for_number(self, row: int, number: int) -> list[Coordinate]:
        if self.__have_number_in_row(row, number):
            return []
        number_of_available_cases = []
        for col in range(9):
            if self.grid.cells[row][col].value == 0:
                if not self.__have_number_in_col(col, number):
                    number_of_available_cases.append(Coordinate(row, col))
        return number_of_available_cases

    def number_of_available_cases_in_col_for_number(self, col: int, number: int) -> list[Coordinate]:
        if self.__have_number_in_col(col, number):
            return []
        number_of_available_cases = []
        for row in range(9):
            if self.grid.cells[row][col].value == 0:
                if not self.__have_number_in_row(row, number):
                    number_of_available_cases.append(Coordinate(row, col))
        return number_of_available_cases

    def __get_rows_and_cols(self, coordinate: Coordinate) -> tuple[list[int], list[int]]:
        if coordinate.row < 3:
            rows = [0, 1, 2]
        elif coordinate.row < 6:
            rows = [3, 4, 5]
        else:
            rows = [6, 7, 8]

        if coordinate.col < 3:
            cols = [0, 1, 2]
        elif coordinate.col < 6:
            cols = [3, 4, 5]
        else:
            cols = [6, 7, 8]

        return rows, cols

    def __get_other_rows_and_cols(self, coordinate: Coordinate) -> tuple[list[int], list[int]]:
        if coordinate.row < 3:
            rows = [3, 4, 5, 6, 7, 8]
        elif coordinate.row < 6:
            rows = [0, 1, 2, 6, 7, 8]
        else:
            rows = [0, 1, 2, 3, 4, 5]

        if coordinate.col < 3:
            cols = [3, 4, 5, 6, 7, 8]
        elif coordinate.col < 6:
            cols = [0, 1, 2, 6, 7, 8]
        else:
            cols = [0, 1, 2, 3, 4, 5]

        return rows, cols

    def __solve_number_of_available_cases_in_3x3(self, number: int, coordinate: Coordinate):
        rows, cols = self.__get_rows_and_cols(coordinate)
        number_of_available_cases_in_3x3 = self.number_of_available_cases_in_3x3(number, rows, cols)
        if len(number_of_available_cases_in_3x3) == 1:
            self.set_cell(number_of_available_cases_in_3x3[0], number)
            self.verify()

    def __solve_number_of_available_cases_in_row(self, number: int, row: int):
        number_of_available_cases_in_row = self.number_of_available_cases_in_row_for_number(row, number)
        if len(number_of_available_cases_in_row) == 1:
            self.set_cell(number_of_available_cases_in_row[0], number)
            self.verify()

    def __solve_number_of_available_cases_in_col(self, number: int, col: int):
        number_of_available_cases_in_col = self.number_of_available_cases_in_col_for_number(col, number)
        if len(number_of_available_cases_in_col) == 1:
            self.set_cell(number_of_available_cases_in_col[0], number)
            self.verify()

    def __solve_number_of_available_cases_in_9x9(self, number: int):
        number_of_available_cases = self.number_of_available_cases_in_9x9(number)
        number_of_available_cases = self.__filter_of_available_cases_in_9x9(number_of_available_cases)
        for group_3x3 in self.__group_coordinates_by_3x3(number_of_available_cases):
            if group_3x3.__len__() == 1:
                self.set_cell(group_3x3[0], number)
                self.verify()

    def solve(self):
        self.number_loop += 1
        if self.number_loop > 10:
            return
        for i in self.numbers:
            num = i[1]
            for row in range(9):
                self.__solve_number_of_available_cases_in_row(num, row)
                self.__solve_number_of_available_cases_in_col(num, row)
                for col in range(9):
                    self.__solve_number_of_available_cases_in_3x3(num, Coordinate(row, col))
            self.__solve_number_of_available_cases_in_9x9(num)
        if self.is_done():
            return
        else:
            self.solve()
