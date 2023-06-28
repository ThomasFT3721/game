from bin.sudoku.Sudoku import Sudoku
from bin.tools.Console import Console, StyledText, Color, Style

# starter
grid_starter = [
    [0, 3, 0, 0, 9, 1, 0, 0, 0],  # 1
    [7, 0, 0, 5, 0, 0, 0, 1, 3],  # 2
    [0, 0, 2, 0, 0, 8, 6, 0, 0],  # 3
    [9, 0, 0, 2, 7, 0, 1, 0, 0],  # 4
    [4, 5, 0, 0, 0, 0, 0, 2, 7],  # 5
    [0, 0, 7, 0, 4, 3, 0, 0, 6],  # 6
    [0, 0, 5, 6, 0, 0, 2, 0, 0],  # 7
    [6, 9, 0, 0, 0, 2, 0, 0, 8],  # 8
    [0, 0, 0, 9, 8, 0, 0, 6, 0]  # 9
]
# medium
grid_medium = [
    [0, 3, 0, 0, 0, 6, 4, 0, 9],  # 1
    [6, 0, 0, 3, 0, 0, 0, 5, 2],  # 2
    [0, 0, 7, 0, 0, 0, 0, 0, 0],  # 3
    [0, 0, 8, 9, 0, 0, 0, 0, 7],  # 4
    [0, 9, 0, 0, 0, 1, 2, 3, 8],  # 5
    [7, 5, 3, 0, 0, 2, 6, 0, 0],  # 6
    [0, 7, 0, 2, 8, 0, 0, 0, 5],  # 7
    [1, 8, 0, 0, 0, 0, 0, 0, 0],  # 8
    [0, 0, 0, 0, 5, 0, 8, 0, 0]  # 9
]
# hard
grid_hard = [
    [0, 0, 9, 1, 3, 0, 0, 0, 0],  # 1
    [0, 0, 0, 7, 0, 4, 1, 0, 0],  # 2
    [1, 0, 0, 5, 0, 8, 0, 7, 0],  # 3
    [3, 4, 0, 0, 0, 0, 0, 0, 0],  # 4
    [0, 0, 0, 2, 5, 0, 0, 0, 3],  # 5
    [7, 2, 6, 0, 0, 9, 0, 0, 1],  # 6
    [0, 0, 0, 0, 0, 0, 0, 5, 0],  # 7
    [6, 8, 0, 0, 0, 0, 4, 0, 0],  # 8
    [0, 5, 0, 0, 0, 3, 0, 1, 7]  # 9
]

grids = [grid_starter, grid_medium, grid_hard]

for grid in grids:
    sudoku = Sudoku(grid)

    sudoku.solve()

    Console.println(StyledText("Solved: " + str(sudoku.number_steps), Style(Color.GREEN)))

    sudoku.print()
    sudoku.print_information()
