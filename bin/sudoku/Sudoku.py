from .Cell import CellState, Cell
from .Coordinate import Coordinate
from .Grid import Grid
from .tools.Printer import Printer
from .types.PairCell import PairCell
from ..tools.Console import Console, StyledText, Color, Style


class Sudoku:
    def __init__(self, start_grid: list[list[int]]):
        self.number_steps = 0
        self.number_loop = 0
        self.banned_pairs = []
        self.numbers = [[0, x] for x in range(1, 10)]
        if len(start_grid) != 9:
            raise Exception("Grid size does not match")
        for y in range(9):
            if len(start_grid[y]) != 9:
                raise Exception("Grid size does not match")
        self.grid = Grid(9, start_grid)

        if not self.verify():
            self.print()
            raise Exception("Invalid start grid")

    def print(self, grid: Grid = None):
        if grid is None:
            grid = self.grid
        Printer.print(grid)

    def print_xl(self, grid: Grid = None):
        if grid is None:
            grid = self.grid
        Printer.print_xl(grid)

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

    def set_cell(self, coordinate: Coordinate, value: int):
        if coordinate.row < 0 or coordinate.row >= 9:
            raise Exception("Row out of bounds")
        if coordinate.col < 0 or coordinate.col >= 9:
            raise Exception("Column out of bounds")
        self.grid.cells[coordinate.row][coordinate.col].set_value(value)
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
        for x in range(row - row % 3, row - row % 3 + 3):
            for y in range(col - col % 3, col - col % 3 + 3):
                if (x != row or y != col) and self.grid.cells[x][y].value == self.grid.cells[row][col].value:
                    return self.grid.cells[row][col].state.INVALID
        return self.grid.cells[row][col].state.VALID

    def is_done(self) -> bool:
        for row in range(9):
            for col in range(9):
                if self.grid.cells[row][col].value == 0:
                    return False
        return True

    @staticmethod
    def __get_boxs() -> list[tuple[list[int], list[int]]]:
        mlist = []
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                rows, cols = Sudoku.__get_rows_and_cols_in_box(row, col)
                mlist.append((rows, cols))
        return mlist

    @staticmethod
    def __get_rows_and_cols_in_box(row: int, col: int) -> tuple[list[int], list[int]]:
        rows = []
        cols = []
        for i in range(row - row % 3, row - row % 3 + 3):
            rows.append(i)
        for j in range(col - col % 3, col - col % 3 + 3):
            cols.append(j)
        return rows, cols

    @staticmethod
    def __get_boxs_aligned_with_box(row: int, col: int) -> list[tuple[list[int], list[int]]]:
        rows, cols = Sudoku.__get_rows_and_cols_in_box(row, col)
        mlist = []
        r = 0
        while r < 9:
            if r not in rows:
                rows1, cols1 = Sudoku.__get_rows_and_cols_in_box(r, col)
                mlist.append((rows1, cols))
                r += 3
            else:
                r += 1
        c = 0
        while c < 9:
            if c not in cols:
                rows1, cols1 = Sudoku.__get_rows_and_cols_in_box(row, c)
                mlist.append((rows, cols1))
                c += 3
            else:
                c += 1
        return mlist

    def __get_cells_in_box(self, row: int, col: int) -> list[Cell]:
        rows, cols = self.__get_rows_and_cols_in_box(row, col)
        cells = []
        for r in rows:
            for c in cols:
                cells.append(self.grid.cells[r][c])
        return cells

    def __get_available_cells_in_box(self, row: int, col: int) -> list[Cell]:
        cells = self.__get_cells_in_box(row, col)
        available_cells = []
        for cell in cells:
            if cell.value == 0:
                available_cells.append(cell)
        return available_cells

    def __get_available_cells_in_box_where_number_is_possible(self, row: int, col: int, number: int) -> list[Cell]:
        cells = self.__get_available_cells_in_box(row, col)
        available_cells = []
        for cell in cells:
            if cell.is_possible_value(number):
                available_cells.append(cell)
        return available_cells

    def __number_is_in_row(self, row: int, number: int) -> bool:
        for col in range(9):
            if self.grid.cells[row][col].value == number:
                return True
        return False

    def __number_is_in_col(self, col: int, number: int) -> bool:
        for row in range(9):
            if self.grid.cells[row][col].value == number:
                return True
        return False

    def __number_is_in_box(self, row: int, col: int, number: int) -> bool:
        rows, cols = self.__get_rows_and_cols_in_box(row, col)
        for r in rows:
            for c in cols:
                if self.grid.cells[r][c].value == number:
                    return True
        return False

    def __count_number_of_possible_values_in_row(self, row: int, number: int) -> int:
        count = 0
        for col in range(9):
            if self.grid.cells[row][col].value == 0 and self.grid.cells[row][col].is_possible_value(number):
                count += 1
        return count

    def __count_number_of_possible_values_in_col(self, col: int, number: int) -> int:
        count = 0
        for row in range(9):
            if self.grid.cells[row][col].value == 0 and self.grid.cells[row][col].is_possible_value(number):
                count += 1
        return count

    def __count_number_of_possible_values_in_box(self, row: int, col: int, number: int) -> int:
        count = 0
        rows, cols = self.__get_rows_and_cols_in_box(row, col)
        for r in rows:
            for c in cols:
                if self.grid.cells[r][c].value == 0 and self.grid.cells[r][c].is_possible_value(number):
                    count += 1
        return count

    def __all_possible_values_are_in_same_row_in_box(self, row: int, col: int, number: int) -> int:
        cells = self.__get_available_cells_in_box_where_number_is_possible(row, col, number)
        if len(cells) == 0:
            return -1
        r = cells[0].coordinate.row
        for cell in cells:
            if cell.coordinate.row != r:
                return -1
        return r

    def __all_possible_values_are_in_same_col_in_box(self, row: int, col: int, number: int) -> int:
        cells = self.__get_available_cells_in_box_where_number_is_possible(row, col, number)
        if len(cells) == 0:
            return -1
        c = cells[0].coordinate.col
        for cell in cells:
            if cell.coordinate.col != c:
                return -1
        return c

    def __count_number_of_pair_appears_in_box(self, row: int, col: int, pair: tuple[int, int]) -> int:
        cells = self.__get_available_cells_in_box(row, col)
        count = 0
        for cell in cells:
            pairs = cell.get_possible_values_as_pairs()
            if pair in pairs:
                count += 1
        return count

    def __find_hidden_pairs_in_box(self, rows: list[int], cols: list[int]) -> list[PairCell]:
        cells = self.__get_available_cells_in_box(rows[0], cols[0])
        cells_as_pairs = []
        for cell in cells:
            for cell2 in cells:
                if cell != cell2:
                    if (cell, cell2) not in cells_as_pairs and (cell2, cell) not in cells_as_pairs:
                        cells_as_pairs.append((cell, cell2))

        tempo_pairs = []
        for pair in cells_as_pairs:
            cell = pair[0]
            cell_possible_values = cell.get_possible_values()
            if len(cell_possible_values) == 1:
                continue
            cell_possible_values_as_pairs = cell.get_possible_values_as_pairs()
            cell2 = pair[1]
            cell2_possible_values = cell2.get_possible_values()
            if len(cell2_possible_values) == 1:
                continue
            cell2_possible_values_as_pairs = cell2.get_possible_values_as_pairs()

            pairs_occurrences = []
            for p in cell_possible_values_as_pairs:
                count_appears = self.__count_number_of_pair_appears_in_box(rows[0], cols[0], p)
                if count_appears == 2:
                    pairs_occurrences.append((p, count_appears))
            for p in cell2_possible_values_as_pairs:
                count_appears = self.__count_number_of_pair_appears_in_box(rows[0], cols[0], p)
                if count_appears == 2:
                    pairs_occurrences.append((p, count_appears))

            pairs_same = []
            pairs_banned = []
            # Filter pairs that one of the values is in the other pair
            for pairs_occurrence in pairs_occurrences:
                can_add = True
                for pairs_occurrence2 in pairs_occurrences:
                    if pairs_occurrence != pairs_occurrence2:
                        if pairs_occurrence[0][0] in pairs_occurrence2[0] or pairs_occurrence[0][1] in pairs_occurrence2[0]:
                            can_add = False
                            break
                if can_add:
                    if pairs_occurrence not in pairs_same and pairs_occurrence not in pairs_banned:
                        pairs_same.append(pairs_occurrence)
                else:
                    if pairs_occurrence not in pairs_banned:
                        pairs_banned.append(pairs_occurrence)
                    if pairs_occurrence in pairs_same:
                        pairs_same.remove(pairs_occurrence)

            if len(pairs_same) == 1:
                p = pairs_same[0][0]
                if p in cell_possible_values_as_pairs and p in cell2_possible_values_as_pairs:
                    tempo_pairs.append(PairCell(cell, cell2, pairs_same[0][0]))
        pairs = []
        for pair in tempo_pairs:
            can_add = True
            for pair2 in self.banned_pairs:
                if pair.cell1 == pair2.cell1 and pair.cell2 == pair2.cell2 and pair.possible_values == pair2.possible_values:
                    can_add = False
                    break
            if can_add:
                pairs.append(pair)
        return pairs

    def __find_pairs_in_box(self, rows: list[int], cols: list[int]) -> list[PairCell]:
        cells = self.__get_available_cells_in_box(rows[0], cols[0])
        cells_as_pairs = []
        for cell in cells:
            for cell2 in cells:
                if cell != cell2:
                    if (cell, cell2) not in cells_as_pairs and (cell2, cell) not in cells_as_pairs:
                        cells_as_pairs.append((cell, cell2))

        pairs = []
        for pair in cells_as_pairs:
            cell = pair[0]
            cell_possible_values = cell.get_possible_values()
            if len(cell_possible_values) == 1:
                continue
            cell_possible_values_as_pairs = cell.get_possible_values_as_pairs()
            cell2 = pair[1]
            cell2_possible_values = cell2.get_possible_values()
            if len(cell2_possible_values) == 1:
                continue
            cell2_possible_values_as_pairs = cell2.get_possible_values_as_pairs()

            pairs_occurrences = []
            for p in cell_possible_values_as_pairs:
                count_appears = self.__count_number_of_pair_appears_in_box(rows[0], cols[0], p)
                if count_appears == 2:
                    pairs_occurrences.append((p, count_appears))
            for p in cell2_possible_values_as_pairs:
                count_appears = self.__count_number_of_pair_appears_in_box(rows[0], cols[0], p)
                if count_appears == 2:
                    pairs_occurrences.append((p, count_appears))

            if len(cell_possible_values_as_pairs) == 1 and cell_possible_values_as_pairs == cell2_possible_values_as_pairs:
                pairs.append(PairCell(cell, cell2, cell_possible_values_as_pairs[0]))


            # TODO banned pairs
            pairs_same = []
            pairs_banned = []
            # Filter pairs that one of the values is in the other pair
            for pairs_occurrence in pairs_occurrences:
                can_add = True
                for pairs_occurrence2 in pairs_occurrences:
                    if pairs_occurrence != pairs_occurrence2:
                        if pairs_occurrence[0][0] in pairs_occurrence2[0] or pairs_occurrence[0][1] in pairs_occurrence2[0]:
                            can_add = False
                            break
                if can_add:
                    if pairs_occurrence not in pairs_same and pairs_occurrence not in pairs_banned:
                        pairs_same.append(pairs_occurrence)
                else:
                    if pairs_occurrence not in pairs_banned:
                        pairs_banned.append(pairs_occurrence)
                    if pairs_occurrence in pairs_same:
                        pairs_same.remove(pairs_occurrence)


        return pairs

    def __set_possible_values(self, number: int) -> bool:
        changed = False
        for row in range(9):
            for col in range(9):
                cell = self.grid.cells[row][col]
                if cell.value == 0:
                    if (self.__number_is_in_row(row, number) or self.__number_is_in_col(col, number) or self.__number_is_in_box(row, col, number)) and cell.is_possible_value(number):
                        cell.remove_possible_value(number)
                        changed = True

        for box in self.__get_boxs():
            rows, cols = box
            current_row = self.__all_possible_values_are_in_same_row_in_box(rows[0], cols[0], number)
            if current_row > -1:
                for col in range(9):
                    cell = self.grid.cells[current_row][col]
                    if cell.value == 0 and cell.is_possible_value(number) and cell.coordinate.col not in cols:
                        cell.remove_possible_value(number)
                        changed = True
            current_col = self.__all_possible_values_are_in_same_col_in_box(rows[0], cols[0], number)
            if current_col > -1:
                for row in range(9):
                    cell = self.grid.cells[row][current_col]
                    if cell.value == 0 and cell.is_possible_value(number) and cell.coordinate.row not in rows:
                        cell.remove_possible_value(number)
                        changed = True

            if self.number_loop > 1:
                hidden_pairs = self.__find_hidden_pairs_in_box(box[0], box[1]) + self.__find_pairs_in_box(box[0], box[1])
                for pair in hidden_pairs:
                    for possible_values in pair.cell1.get_possible_values():
                        if possible_values not in pair.possible_values:
                            pair.cell1.remove_possible_value(possible_values)
                            changed = True
                    for possible_values in pair.cell2.get_possible_values():
                        if possible_values not in pair.possible_values:
                            pair.cell2.remove_possible_value(possible_values)
                            changed = True
                    self.banned_pairs.append(pair)
        return changed

    def __set_values_for_number(self, number: int):
        for row in range(9):
            for col in range(9):
                cell = self.grid.cells[row][col]
                if cell.value == 0 and cell.is_possible_value(number):
                    if self.__count_number_of_possible_values_in_row(row, number) == 1:
                        self.set_cell(cell.coordinate, number)
                        continue
                    if self.__count_number_of_possible_values_in_col(col, number) == 1:
                        self.set_cell(cell.coordinate, number)
                        continue
                    if self.__count_number_of_possible_values_in_box(row, col, number) == 1:
                        self.set_cell(cell.coordinate, number)

    def __set_values(self):
        for row in range(9):
            for col in range(9):
                cell = self.grid.cells[row][col]
                if cell.value == 0 and cell.len_possible_values() == 1:
                    self.set_cell(cell.coordinate, cell.get_possible_values()[0])

    def solve(self) -> bool:
        self.number_loop += 1
        for i in self.numbers:
            if i[0] == 9:
                continue
            num = i[1]
            print("//////" * 20)
            print(f'Loop: {self.number_loop}, number: {num}')
            while self.__set_possible_values(num):
                pass
            self.__set_values_for_number(num)
            self.__set_values()
            self.print_xl()
            self.verify()
        return self.is_done()
