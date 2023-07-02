from bin.sudoku.Grid import Grid
from bin.tools.Console import Style, Console, StyledText, Color


class Printer:

    @staticmethod
    def print(grid: Grid):
        if grid.size == 9:
            Printer.__print_9x9(grid)

    @staticmethod
    def __print_9x9(grid: Grid):
        Console.println(StyledText("╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗", Style(Color.GREY)))
        for y in range(grid.size):
            Console.print(StyledText("║", Style(Color.GREY)))
            for x in range(grid.size):
                cell = grid.cells[y][x]

                Console.print(" " + StyledText(cell.get_value_for_print(), cell.get_style_for_print()).__str__() + " ")

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

    @staticmethod
    def print_xl(grid: Grid):
        if grid.size == 9:
            Printer.__print_9x9_xl(grid)

    @staticmethod
    def __print_9x9_xl(grid: Grid):
        Console.println(StyledText("╔═══════╤═══════╤═══════╦═══════╤═══════╤═══════╦═══════╤═══════╤═══════╗", Style(Color.GREY)))
        for y in range(grid.size):
            for i in range(1, 4):
                Console.print(StyledText("║", Style(Color.GREY)))
                for x in range(grid.size):
                    cell = grid.cells[y][x]
                    Console.print(" ")
                    Console.print(StyledText(cell.get_value_for_print_xl(i * 3 - 2), cell.get_style_for_print_xl(i * 3 - 2)))
                    Console.print(" ")
                    Console.print(StyledText(cell.get_value_for_print_xl(i * 3 - 1), cell.get_style_for_print_xl(i * 3 - 1)))
                    Console.print(" ")
                    Console.print(StyledText(cell.get_value_for_print_xl(i * 3), cell.get_style_for_print_xl(i * 3)))
                    Console.print(" ")
                    if x % 3 == 2:
                        Console.print(StyledText("║", Style(Color.GREY)))
                    else:
                        Console.print(StyledText("│", Style(Color.GREY)))
                Console.println()
            if y % 3 == 2:
                if y != grid.size - 1:
                    Console.println(StyledText("╠═══════╪═══════╪═══════╬═══════╪═══════╪═══════╬═══════╪═══════╪═══════╣", Style(Color.GREY)))
            else:
                Console.println(StyledText("╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢", Style(Color.GREY)))

        Console.println(StyledText("╚═══════╧═══════╧═══════╩═══════╧═══════╧═══════╩═══════╧═══════╧═══════╝", Style(Color.GREY)))
