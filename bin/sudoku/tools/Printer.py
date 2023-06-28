from bin.sudoku.Cell import CellState
from bin.sudoku.Grid import Grid
from bin.tools.Console import Style, Console, StyledText, Color


class Printer:

    @staticmethod
    def print(grid: Grid):
        if grid.size == 9:
            Printer.print_9x9(grid)

    @staticmethod
    def print_9x9(grid: Grid):
        Console.println(StyledText("╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗", Style(Color.GREY)))
        for y in range(grid.size):
            Console.print(StyledText("║", Style(Color.GREY)))
            for x in range(grid.size):
                cell = grid.cells[y][x]
                value = str(cell.value)
                if cell.value == 0:
                    value = " "

                style = Style(Color.CYAN, cell.background)

                if cell.given:
                    style.color = Color.WHITE
                else:
                    style.bold = True

                if cell.state == CellState.INVALID:
                    style.color = Color.ORANGE
                    if not cell.given:
                        style.color = Color.RED

                Console.print(" " + StyledText(value, style).__str__() + " ")

                if x % 3 == 2:
                    Console.print(StyledText("║", Style(Color.GREY)))
                else:
                    Console.print(StyledText("│", Style(Color.GREY)))
            Console.println()
            if y % 3 == 2:
                if y != grid.size - 1:
                    Console.println(StyledText("╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣", Style(Color.GREY)))
            else:
                Console.println(StyledText("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢", Style(Color.GREY)))

        Console.println(StyledText("╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝", Style(Color.GREY)))
