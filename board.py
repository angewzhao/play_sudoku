"""
This creates a board class for the entire sudoku board. There are 81 cells in each board.

Each board has these attributes: width, height, level given, num_rows, num_cols, the puzzle itself, the surface on which
all of its attributes are blitted/drawn, which cell is selected, a comment at the bottom left corner, and a button's
dimensions. The button is the solve button.

Inspiration was taken from TechWithTim.
"""

from sudoku import make_puzzle_board, valid_move, solve_board_possible
from cell import Cell
from config import NUM_CELLS
import pygame


class Board:

    """
    This initiates the board.
    """

    def __init__(self, width, height, level, win):
        self.width = width
        self.height = height
        self.level = level
        self.num_rows = 9
        self.num_cols = 9
        self.puzzle = make_puzzle_board(level)
        self.puzzle = [[Cell(r, c, width, height, self.puzzle[r][c]) for c in range(self.num_cols)] \
                       for r in range(self.num_rows)]
        self.win = win
        self.selected_cell = None
        self.comment = "Let's play!"

        self.button_x = None
        self.button_y = None
        self.button_width = None
        self.button_height = None

    """
    This function determines whether or not a value the player places in a certain cell is a valid value. To be valid, 
    the cell must be changeable and it must be a valid move. 
    """

    def value_correct(self, val):
        row, col = self.selected_cell
        if self.puzzle[row][col].value == 0:
            self.puzzle[row][col].value = val
            test_puzzle = [[self.puzzle[i][j].value for j in range(self.num_cols)] for i in range(self.num_rows)]

            if valid_move(row, col, val, test_puzzle) and self.puzzle[row][col].changeable:
                return True

            self.puzzle[row][col].value = 0
            self.puzzle[row][col].temp = 0

        return False


    """
    This function draws the comment given to the bottom left corner of the board. 
    """
    def add_comment(self, font, window):
        text = font.render(self.comment, True, (0, 0, 0))
        width, height = pygame.display.get_surface().get_size()
        window.blit(text, (0, height - text.get_height()))

    """
    This function draws the solve button in the bottom center of the board. 
    """
    def draw_solve_button(self, font, window):
        text = font.render("Solve", True, (0, 0, 0))
        width, height = pygame.display.get_surface().get_size()
        x = ((width - text.get_width()) / 2) - 10
        y = height - text.get_height() - 10

        pygame.draw.rect(window, (52, 216, 235), (x, y, text.get_width() + 20, text.get_height() + 30))
        window.blit(text, (x, y))

        self.button_x = x
        self.button_y = y
        self.button_width = text.get_width() + 20
        self.button_height = text.get_height() + 30

    """
    This function checks whether or not the player has clicked on the "Solve" button. 
    """
    def clicked_on_button(self, coord):
        x, y = coord

        return self.button_x <= x <= self.button_x + self.button_width \
               and self.button_y <= y <= self.button_y + self.button_height

    """
    This function draws the board. It creates both thick and thin lines, then draws in the cells, the comment at the
    bottom, and then the solve button. 
    """
    def draw(self, window):
        gap = self.width / 9
        for i in range(self.num_rows + 1):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(window, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(window, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw the cells.
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.puzzle[i][j].draw_cell(window)

        # draw in the comment
        font = pygame.font.SysFont("comicsans", 40)
        self.add_comment(font, window)

        # Draw in the "Solve" button
        self.draw_solve_button(font, window)

    """
    This function sets the specificed cell at row, col to be selected and all other cells to be not selected. 
    """
    def select(self, row, col):
        # Reset all other
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.puzzle[i][j].selected = False

        self.puzzle[row][col].selected = True
        self.selected_cell = (row, col)

    """
    This function sets both the temp and value of the cell to 0. 
    """
    def remove_value_temp(self):
        row, col = self.selected_cell
        if self.puzzle[row][col].changeable:
            self.puzzle[row][col].value = 0
            self.puzzle[row][col].temp = 0

    """
    Get the position of the selected cell. The x and y are flipped due to how the board is represented and how pixels
    work in images(0,0) is the top left corner.
    """
    def get_selected_cell_position(self, coord):
        if 0 < coord[0] < self.width and 0 < coord[1] < self.height:
            cell_width = self.width / 9

            # FLip the x and y b/c the way pixels work normally and board are flipped
            return int(coord[1] // cell_width), int(coord[0] // cell_width)

        return None

    """
    This function checks whether or not the board is complete.  
    """
    def is_finished(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.puzzle[row][col].value == 0:
                    return False
        return True

    """
    This function visualizes the backtracking algorithm on the board itself. 
    """
    def solve_board_gui(self, test_puzzle):
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col].value == 0:
                    for num in range(1, 10):
                        test_puzzle = [[self.puzzle[i][j].value for j in range(self.num_cols)] for i in
                                       range(self.num_rows)]
                        if valid_move(row, col, num, test_puzzle):
                            test_puzzle[row][col] = num
                            self.puzzle[row][col].value = num
                            self.puzzle[row][col].draw_solve_gui_cell(self.win, True)
                            pygame.display.update()
                            pygame.time.delay(150)

                            if self.solve_board_gui(test_puzzle):
                                return True

                            self.puzzle[row][col].value = 0
                            self.puzzle[row][col].draw_solve_gui_cell(self.win, False)
                            pygame.display.update()
                            pygame.time.delay(150)
                    return False
        return True

    """
    This function resets the board to what is originally used to be. It sets all changeable values to 0, all temp values
    to 0, and covers up all changeable value cells with a white rectangle. 
    """
    def reset_board(self, window):
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col].changeable:
                    self.puzzle[row][col].value = 0
                    self.puzzle[row][col].temp = 0

                    cell_width = self.width / 9
                    cell_height = cell_width

                    x = col * cell_width
                    y = row * cell_height

                    # Cover up any old/wrong numbers with a white rectangle.
                    # Changes to x, y were made just to cover the middle bits and leave the border black
                    pygame.draw.rect(window, (255, 255, 255), (x + 5, y + 5, cell_width - 10, cell_width - 10))