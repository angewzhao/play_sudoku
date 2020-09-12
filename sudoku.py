"""
This is a script that both creates a Sudoku board to be solved and is also capable of solving the board.

Method of solving the board: backtracking. If a cell is empty, try putting in a valid number. If the board is solvable
with that number, then return True. Otherwise, remove that number and continue trying all numbers. If you've gone through
all numbers for that particular cell and you still can't solve the board, then the board is unsolvable. Return false.
Otherwise, if you've gone through all of the board and have discovered there are no empty cells, this must be a filled board
and therefore is a solvable board. Return true.

Method of creating the board:
Seed the board with one value per row, randomly with all 9 values being 1-9. Then, solve the board. Afterwards,
remove one value from the board from a random position and check if the resulting board still only has one solution.
Continue doing so until desired number of clues corresponding to level is reached.

The idea of seeding the board: https://www.sudokuwiki.org/Sudoku_Creation_and_Grading.pdf.

"""

import random, copy
from config import NUM_CELLS

"""
This function checks whether or not a number can be placed in a certain cell in a certain board so that the number
doesn't violate the sudoku rule that there can only be one number from 1-9 in each row and column. 

Parameters: row number, col number, the number tested, and the board, which is a list of 9 lists for each row on the 
Sudoku board. 

Returns: boolean
"""


def check_row_col(row, col, num, board):
    for i in range(9):
        if col != i and board[row][i] == num:
            return False
    for i in range(9):
        if row != i and board[i][col] == num:
            return False
    return True


"""
This returns the start and end index of both columns and rows of the 3x3 block boundary on each Sudoku board. 

Parameter: the row or column index of the cell, and the desired start or end for the boundary

Returns: either the start or end index for both columns and rows of the 3x3 block boundary on each Sudoku board.
"""


def get_block_boundary(index, boundary):
    if index <= 2:
        if boundary == "start":
            return 0
        elif boundary == "end":
            return 2
    elif 3 <= index <= 5:
        if boundary == "start":
            return 3
        elif boundary == "end":
            return 5
    elif 6 <= index <= 8:
        if boundary == "start":
            return 6
        elif boundary == "end":
            return 8


"""
This function checks whether or not the number being tested is valid within the 3x3 block it resides. The number is 
valid when the number is the only one of its kind within the 3x3 block. 

Parameters: row number, col number, the number tested, and the board, which is a list of 9 lists for each row on the 
Sudoku board. 

Returns: boolean
"""


def check_block(row, col, num, board):
    for r in range(get_block_boundary(row, "start"), get_block_boundary(row, "end") + 1):
        for c in range(get_block_boundary(col, "start"), get_block_boundary(col, "end") + 1):
            if r != row and c != col and board[r][c] == num:
                return False
    return True


"""
This function checks whether or not the number being tested is valid and can be placed in the row and column given 
Sudoku rules. 

Parameters: row number, col number, the number tested, and the board, which is a list of 9 lists for each row on the 
Sudoku board. 

Returns: boolean
"""


def valid_move(row, col, num, board):
    return check_row_col(row, col, num, board) and check_block(row, col, num, board)


"""
This function checks whether or not the filled Sudoku board created is a valid Sudoku board. 

Parameters: board, which is a list of 9 lists for each row on the 
Sudoku board. 

Returns: boolean
"""


def is_valid_board(board):
    for r in range(9):
        for c in range(9):
            if not valid_move(r, c, board[r][c], board) or board[r][c] == 0:
                return False
    return True


"""
This solves the Sudoku board given. The logic, in pseudocode:
for all r in row:
    for all c in colums: 
        if the cell is empty:
            for all numbers in 1-9:
                Test out whether or not the resulting board can be solved if the number is placed into the empty cell.
                if so, then return true. 
                Otherwise, replace the number with 0 and try the next number. 
            All of the numbers have been tried and there is no solution. Return False. 
The board is complete, so it must be solvable. Return True. 

Parameters: board, which is a list of 9 lists for each row on the Sudoku board. 

Returns: boolean
"""


def solve_board_possible(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if valid_move(row, col, num, board):
                        board[row][col] = num
                        if solve_board_possible(board):
                            return True
                        board[row][col] = 0
                return False
    return True


"""
This creates a bare-bones template for the creation of a filled Sudoku board. This method of starting a board is inspired
by AC Stuart's paper on Sudoku creation. 9 cells are chosen and given 1 number from 1-9; 1-9 appear once through all 9
cells. This is not guaranteed to make a valid or solvable board. 

Parameters: board, which is a list of 9 lists for each row on the Sudoku board. 

Returns: board, which is a list of 9 lists for each row on the Sudoku board. 
"""


def seed_board(board):
    nums_left = list(range(1, 10))

    for row in range(9):
        col = random.randint(0, 8)
        nums_left_index = random.randint(0, len(nums_left) - 1)

        seed_num = nums_left.pop(nums_left_index)

        board[row][col] = seed_num

    return board


"""
This creates a possible Sudoku solution. It creates an empty board, seeds the board, and returns a solved board. 

Paramters: none

Returns: board, which is a list of 9 lists for each row on the Sudoku board. 
"""


def make_possible_sudoku_solution():
    # Creates an empty board
    board = []
    for i in range(9):
        board.append([0] * 9)

    # Seed 9 cells randomly with numbers 1-9
    board = seed_board(board)

    # if cannot solve the board, then re-seed
    while not solve_board_possible(board):
        board = seed_board(board)

    # The reason why this is possible is because lists are passed by reference in Python. So the solve_board_possible
    # method automatically changes the board as needed and when the method finishes, board is solved and filled.
    return board


"""
This ensures that the Sudoku board, solved and filled, is a valid board. 

Parameters: none

Returns: board, which is a list of 9 lists for each row on the Sudoku board. 
"""


def sudoku_solution():
    board = make_possible_sudoku_solution()

    while not is_valid_board(board):
        board = make_possible_sudoku_solution()

    return board


"""
This function counts the number of solutions a Sudoku board has. No longer used because too slow. The logic:

The board given is a half-empty board that needs to be filled. So, go through and try to find all of the possible
solutions to this board. Once solve_board_possible runs, save the board and put it into a list of solutions in order
to differentiate different solutions. 

This can be rather redundant and can be improved. 

Parameters: board, which is a list of 9 lists for each row on the Sudoku board. 

Returns: number of solutions
"""


# def num_solutions(board):
#     count = 0
#
#     solutions = []
#
#     for row in range(9):
#         for col in range(9):
#             if board[row][col] == 0:
#                 for num in range(1, 10):
#                     if valid_move(row, col, num, board):
#                         # Create a complete copy of the given board for solve_board_possible to change.
#                         copy_board = copy.deepcopy(board)
#                         copy_board[row][col] = num
#
#                         if solve_board_possible(copy_board):
#                             solved_board = copy_board
#
#                             if solved_board not in solutions:
#                                 count += 1
#                                 solutions += [solved_board]
#
#     # if the board is filled:
#     if count == 0:
#         count += 1
#
#     return count

"""
This function solves the board by going backwards. It does solve_board_possible, but backwards. 

Parameters: board, which is a list of 9 lists for each row on the Sudoku board. 

Returns: whether or not solving the board is possible. 
"""


def solve_board_backwards(board):
    for row in reversed(range(9)):
        for col in reversed(range(9)):
            if board[row][col] == 0:
                for num in reversed(range(1, 10)):
                    if valid_move(row, col, num, board):
                        board[row][col] = num
                        if solve_board_backwards(board):
                            return True
                        board[row][col] = 0
                return False
    return True

"""
This function checks if the solutions of solving the board backwards and forwards is equivalent. If yes, then only 1
unique solution. If not, multiple solutions possible. 

Here, although the solve_board_x return booleans, since the boards themselves are passed in by reference, by checking
whether or not the boards are solvable, the boards themselves are solved. 

Parameters: board, which is a list of 9 lists for each row on the Sudoku board. 

Returns: whether or not the board has a unique solution
"""


def unique_solution(board):
    copy_f = copy.deepcopy(board)
    copy_b = copy.deepcopy(board)
    solve_board_possible(copy_f)

    solve_board_backwards(copy_b)

    return copy_f == copy_b

"""
Choose the number of clues according to the level given. Here, 39 is the upper limit for the number of clues a minimal
puzzle can have. To be clear, this does not create minimal puzzles, but in the case of a minimal puzzle, cap the 
number of clues at 39. The lower limit number of clues for each puzzle to have only 1 solution is 17.

The standards here are general guidelines given for Sudoku. 

Parameters: a string for easy, medium, or hard. 

Returns: a random integer in a range of numbers for each level. 
"""


def choose_num_clues(level):
    if level == "easy":
        return random.randint(36, 39)
    elif level == "medium":
        return random.randint(27, 35)
    elif level == "hard":
        return random.randint(19, 26)

"""
This function generates a random list of all of the cell indexes for the make_puzzle_board function to try to remove 
from a filled Sudoku board. A cell: [row index, col index].

Paramters: none

Returns: a list of all of the cell indexes, shuffled, for the board. 
"""


def gen_cell_indexes():
    cells = []

    for row in range(9):
        for col in range(9):
            cells.append([row, col])

    random.shuffle(cells)

    return cells


"""
This determines whether or not the board has reached the number of clues it needs for a certain level. Clues are cells
that are left in. 

Paramters: number of empty cells and the level of those cells

Returns: boolean
"""


def reached_target_level(num_empty_cells, level):
    num_clues = NUM_CELLS - num_empty_cells
    return (level == "easy" and 36 <= num_clues <= 39) \
           or (level == "medium" and 27 <= num_clues <= 35) \
           or (level == "hard" and 19 <= num_clues <= 26)

"""
This removes cells in a random order to try and create a Sudoku puzzle according to the desired level, which is graded 
by the number of clues (or remaining cells) wished to be included in the finished puzzle. 

This function tries to remove a cell. If the cell is removable and the resulting board produces a board that has a 
unique solution, then leave the cell empty. Otherwise, move on to the next cell. Keep a running list of the cells that
have been removed. Keep trying to remove cells until the target number of clues has been reached. If the target number
of clues is unreachable, then try again with a new board and reset the function. 

Parameters: board, which is a list of 9 lists for each row on the Sudoku board, 
and a level (easy, medium, hard). 

Returns: board, which is a list of 9 lists for each row on the Sudoku board. 
"""


def make_puzzle_board(level):
    board = sudoku_solution()
    count_empty_cells = 0
    cells_to_empty = gen_cell_indexes()
    target_empty_cells = NUM_CELLS - choose_num_clues(level)
    emptied_cells = []

    while len(cells_to_empty) != 0:
        cells_to_empty_len = len(cells_to_empty)
        for cell in cells_to_empty:
            if cell not in emptied_cells:
                row = cell[0]
                col = cell[1]

                copy_board = copy.deepcopy(board)
                copy_board[row][col] = 0

                #if num_solutions(copy_board) == 1: Too slow
                if unique_solution(copy_board):
                    count_empty_cells += 1
                    board[row][col] = 0
                    emptied_cells += [cell]

                if count_empty_cells == target_empty_cells:
                    return board

                # If within target level, then return the board
                if level == "hard":
                    if reached_target_level(count_empty_cells, level):
                        return board

        # If it is impossible to reach the desired number of empty cells:
        if len(cells_to_empty) == cells_to_empty_len:
            if reached_target_level(count_empty_cells, level):
                return board
            # Otherwise, try a new board and reset the function.
            board = sudoku_solution()
            count_empty_cells = 0
            cells_to_empty = gen_cell_indexes()
            target_empty_cells = NUM_CELLS - choose_num_clues(level)
            emptied_cells = []


def main():
    x = make_puzzle_board("easy")

    for line in x:
        print(line)

# When executed directly, then condition is true. If executed indirectly, like it's imported, then the if statement
# evaluates to false.
if __name__ == "__main__":
    main()
