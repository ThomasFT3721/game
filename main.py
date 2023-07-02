from bin.sudoku.Cell import Cell
from bin.sudoku.Sudoku import Sudoku
from bin.tools.Console import Console, StyledText, Color, Style

# starter
grid_starter = [
    [9, 1, 7, 2, 5, 4, 0, 0, 0],  # 1
    [4, 0, 2, 0, 8, 7, 9, 0, 0],  # 2
    [6, 5, 0, 0, 0, 3, 4, 2, 0],  # 3
    [0, 0, 3, 0, 9, 1, 2, 5, 6],  # 4
    [5, 0, 1, 7, 2, 0, 3, 0, 9],  # 5
    [2, 0, 0, 0, 4, 5, 0, 7, 1],  # 6
    [0, 2, 0, 5, 3, 0, 7, 6, 0],  # 7
    [3, 7, 0, 1, 6, 0, 0, 9, 8],  # 8
    [0, 0, 5, 0, 0, 0, 1, 3, 0]  # 9
]
# easy
grid_easy = [
    [0, 2, 0, 0, 0, 0, 0, 0, 0],  # 1
    [1, 5, 8, 0, 0, 0, 0, 3, 0],  # 2
    [3, 4, 0, 1, 6, 0, 9, 0, 2],  # 3
    [0, 0, 9, 2, 0, 8, 1, 7, 5],  # 4
    [0, 0, 0, 0, 4, 0, 0, 0, 0],  # 5
    [0, 3, 5, 6, 0, 1, 0, 0, 0],  # 6
    [0, 0, 0, 3, 0, 0, 5, 9, 4],  # 7
    [5, 1, 3, 4, 8, 0, 0, 0, 7],  # 8
    [6, 9, 0, 7, 5, 2, 0, 0, 3]  # 9
]
# medium
grid_medium = [
    [0, 6, 0, 0, 3, 9, 0, 0, 0],  # 1
    [3, 0, 2, 0, 0, 0, 9, 0, 5],  # 2
    [1, 9, 0, 0, 0, 0, 6, 0, 0],  # 3
    [0, 8, 0, 7, 0, 4, 1, 3, 2],  # 4
    [0, 0, 0, 0, 0, 0, 5, 9, 0],  # 5
    [0, 1, 0, 0, 0, 0, 7, 0, 0],  # 6
    [9, 2, 0, 4, 0, 3, 0, 7, 0],  # 7
    [4, 0, 3, 0, 0, 0, 0, 5, 0],  # 8
    [0, 0, 0, 0, 6, 0, 3, 0, 0]  # 9
]
# hard
grid_hard = [
    [0, 0, 1, 0, 0, 4, 0, 7, 0],  # 1
    [6, 4, 0, 2, 0, 0, 0, 0, 0],  # 2
    [8, 0, 0, 0, 1, 0, 5, 0, 9],  # 3
    [4, 0, 0, 0, 0, 2, 0, 0, 0],  # 4
    [0, 0, 0, 1, 9, 0, 0, 8, 0],  # 5
    [0, 0, 0, 7, 0, 0, 3, 0, 0],  # 6
    [3, 0, 0, 5, 0, 0, 0, 0, 0],  # 7
    [0, 0, 0, 0, 0, 0, 7, 6, 0],  # 8
    [9, 0, 0, 0, 7, 8, 4, 0, 0]  # 9
]
# expert
grid_expert = [
    [1, 3, 0, 0, 0, 5, 0, 0, 0],  # 1
    [5, 0, 0, 7, 0, 0, 0, 0, 2],  # 2
    [0, 0, 0, 2, 0, 9, 0, 0, 0],  # 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
    [9, 1, 0, 0, 0, 0, 0, 8, 7],  # 5
    [0, 0, 7, 0, 6, 0, 0, 1, 0],  # 6
    [0, 5, 0, 4, 0, 0, 0, 0, 0],  # 7
    [3, 4, 0, 0, 0, 0, 0, 0, 0],  # 8
    [8, 0, 0, 0, 0, 6, 3, 0, 5]  # 9
]

grids = [grid_expert]

solved = False


def loop(sudoku: Sudoku):
    global solved

    print()
    print()

    solved = sudoku.solve()
    sudoku.verify()

    Console.println(StyledText("Solved: " + str(sudoku.number_steps), Style(Color.GREEN)))

    if False:
        if False:
            for i in range(0, 9):
                Cell.number = i + 1
                sudoku.print()
                sudoku.print_information()

        Cell.number = -1
        sudoku.print()
        sudoku.print_information()
        Cell.number = None
        sudoku.print()
        sudoku.print_information()

    sudoku.print_xl()
    exit()

    if not solved:
        response = input("Press enter to continue...")
        if response != "":
            exit()
        else:
            loop(sudoku)


for grid in grids:
    sudoku = Sudoku(grid)
    loop(sudoku)
    solved = False
