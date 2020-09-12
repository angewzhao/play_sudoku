"""
This module allows players to play an interactive version of Sudoku. This version allows the player to choose one of
three levels: easy, medium or hard. The game then creates a board depending on the level chosen. It may take a while, so
wait, at most, a minute if the level chosen was "hard". It also allows the players to have a timer to see how long they
have been playing, an option to see the backtracking algorithm in action by clicking the solve button, and an
automatic checker that lets them know if they can put a value there or not.

This game was inspired by TechWithTim.

How to play:
Run py play.py with the files sudoku.py, cell.py, and board.py in the same directory.

Click on the solve button if you want to watch the algorithm in action.

Click on a cell to highlight and confirm that is the cell whose value you want to change. Press a number key; that will
be the temporary value you want to try out. If you've decided you want to place the value there, then hit enter. If the
value can be placed there according to Sudoku rules, it will appear as a black number centered in the cell. If it cannot
be placed there, try another value.

If you don't like the value that you've placed, select the cell by clicking on it and then hit backspace or delete.

The timer in the bottom right corner will tell you how long it took you to solve the puzzle.

"""

import pygame, time, copy
from pygame.locals import *
from sudoku import make_puzzle_board, valid_move, solve_board_possible
from board import Board
from cell import Cell
from config import NUM_CELLS

"""
This function formats the time, given in seconds, as a string. 
"""


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    return str(hour) + ":" + str(minute) + ":" + str(sec)


"""
This function draws the time onto the surface on the lower right corner. 
"""


def draw_time(window, play_time):
    font = pygame.font.SysFont("comicsans", 40)
    text = font.render("Time: " + format_time(play_time), True, (0, 0, 0))

    width, height = pygame.display.get_surface().get_size()
    window.blit(text, (width - text.get_width(), height - text.get_height()))


"""
This function redraws the game to account for changes made. It re-fills the window, draws the timer, and then redraws
the grid and the board. 
"""


def redraw_window(win, board, clock):
    win.fill((255, 255, 255))

    # Draw the timer position
    draw_time(win, clock)

    # Draw grid and board
    board.draw(win)


"""
This is a dictionary that gets and returns the key pressed by the player. Default value is None. 
"""


def get_key(event):
    switcher = {
        K_1: 1,
        K_2: 2,
        K_3: 3,
        K_4: 4,
        K_5: 5,
        K_6: 6,
        K_7: 7,
        K_8: 8,
        K_9: 9
    }

    # Takes the event argument and passes back the key. If no key matches, then passes back None.
    return switcher.get(event, None)

"""
This function gets the level the player wants to play. It will account for capitlization mistakes and check that only the
possible levels told will be selected. 
"""


def get_level():
    level = input("Enter the level(easy, medium, or hard): ")
    level = level.lower()

    while level not in ["easy", "medium", "hard"]:
        print("Please enter either easy, medium, or hard.")
        level = input("Enter the level(easy, medium, or hard): ")
        level = level.lower()
    return level

"""
This function pulls everything together to create a game. It sets up the screen, takes in the level the player wants
to play, continually checks for key input in order to update the game.  
"""

def play():
    pygame.init()

    screen_width = 540
    screen_height = 600

    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Play Sudoku!")

    level = get_level()
    board = Board(screen_width, screen_width, level, win)
    key = None

    start = time.time()

    while True:
        play_time = round(time.time() - start)
        draw_time(win, play_time)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                key = get_key(event.key)

                # If hit enter to turn the temp into value, check whether or not the value can be place there. Show
                # cooresponding comment if value was correct or incorrect.
                if event.key == K_RETURN:
                    row, col = board.selected_cell
                    if board.puzzle[row][col].temp != 0:
                        if board.value_correct(board.puzzle[row][col].temp):
                            board.comment = "Right on!"
                        else:
                            board.comment = "Illegal!"

                # Whether Mac or Windows, remove the temp and the value if no longer wanted
                if event.key == K_DELETE or event.key == K_BACKSPACE:
                    board.remove_value_temp()

            # If hit something, then either cell or the solve button. Either solve the board or update that the cell
            # has been selected.
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_cell = board.get_selected_cell_position(pygame.mouse.get_pos())

                # Currently solve_board_gui not working
                if board.clicked_on_button(pygame.mouse.get_pos()):
                    test_puzzle = [[board.puzzle[i][j].value for j in range(board.num_cols)] for i in
                                   range(board.num_rows)]

                    # If is not possible to solve, then reset board to original position
                    if not solve_board_possible(test_puzzle):
                        board.reset_board(win)
                        board.draw(win)
                        pygame.display.update()
                        pygame.time.delay(100)

                    board.solve_board_gui(board)
                    print("Done.")

                if selected_cell is not None:
                    board.select(selected_cell[0], selected_cell[1])

        # If the board is complete, place appropriate comment.
        if board.is_finished():
            board.comment = "You've finished!"

        # update temp
        if board.selected_cell is not None and key is not None:
            row, col = board.selected_cell
            board.puzzle[row][col].temp = key

        # Redraw the board according the the changes
        redraw_window(win, board, play_time)

        # Update the display
        pygame.display.update()


def main():
    play()


# When executed directly, then condition is true. If executed indirectly, like it's imported, then the if statement
# evaluates to false.
if __name__ == "__main__":
    main()
