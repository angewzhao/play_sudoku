"""
This creates a cell class for every single one of the 81 cells in a sudoku board. This is so that when playing the
game, each cell has its own and different properties that make playing easier.

Each cell has these attributes: whether or not it can be changed, its row, its column, the board_width, the board_height,
its permanent value, its temporary value, whether or not it was selected, and its line thickness for the highlighted
rectangle that goes around the border when it is selected.

Inspiration was taken from TechWithTim.
"""
import pygame
from sudoku import make_puzzle_board, valid_move, solve_board_possible
from config import NUM_CELLS


class Cell:
    """
    This function initiates all of the properites of the Cell class.
    """

    def __init__(self, row, col, width, height, value):
        # Whether or not the player can change the value
        self.changeable = False
        self.set_changeable(value)
        self.row = row
        self.col = col
        self.board_width = width
        self.board_height = height
        self.value = value
        self.temp = 0
        self.selected = False
        self.line_thickness = 2

    """
    This function sets whether or not the cell's value can be changed. Changeable values are those that were not set
    in stone for the original board problem given to the user.   
    """
    def set_changeable(self, val):
        if val == 0:
            self.changeable = True

    """
    This function draws the cell when the player wants the program to solve the board.
    
    First, there is a blank white rectangle that covers up all of the old numbers. Then, choose the color of the 
    rectangle that highlights the cell: green if the value is correct/is a value that is being tried, and red if the 
    value has found to be incorrect. Draw the highlighted rectangle. Finally, draw on the value currently stored in the 
    cell.  
       
    """
    def draw_solve_gui_cell(self, window, value_correct=True):
        cell_width = self.board_width / 9
        cell_height = cell_width

        x = self.col * cell_width
        y = self.row * cell_height

        # Cover up any old/wrong numbers with a white rectangle.
        # Changes to x, y were made just to cover the middle bits and leave the border black.
        pygame.draw.rect(window, (255, 255, 255), (x + 5, y + 5, cell_width - 10, cell_width - 10))

        color = (0, 255, 0)
        if not value_correct:
            color = (255, 0, 0)

        pygame.draw.rect(window, color, (x + 5, y + 5, cell_width - 10, cell_width - 10), self.line_thickness)

        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(str(self.value), True, (0, 0, 0))

        x += (cell_width - text.get_width()) / 2
        y += (cell_height - text.get_height()) / 2
        window.blit(text, (x, y))

    """
    This function draws the cell, normally, when the player is playing the Sudoku game. First, draw in the temporary
    value if there is no value set yet. It appears as a small grey number in the upper left hand bit of the cell. Then, 
    draw in the value if it exists. This is black and centered in the cell. Finally, if the cell has been selected by
    being clicked on, then draw a green square around the highlighted bit of board. 
    """
    def draw_cell(self, window):
        font = pygame.font.SysFont('comicsans', 40)

        # width and height, here, are board widths
        cell_width = self.board_width / 9
        cell_height = cell_width

        x = self.col * cell_width
        y = self.row * cell_height

        #Draw temp
        if self.temp != 0 and self.value == 0:
            # the 128s code for the color, True for words to have smooth edges
            temp_text = font.render(str(self.temp), True, (128,128,128))

            # Puts the text on the screen at certain coordinates
            window.blit(temp_text, (x + self.line_thickness, y + self.line_thickness))

        # Draw value
        elif self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            x += (cell_width - text.get_width()) / 2
            y += (cell_height - text.get_height()) / 2
            window.blit(text, (x, y))

        # If selected, then draw the green square around the highlighted board
        if self.selected and self.changeable:
            if self.value != 0:
                x -= 25
                y -= 15
            # Surface, color, left, top, width, height, thickness
            pygame.draw.rect(window, (0, 255, 0), (x, y, cell_width, cell_height), self.line_thickness)