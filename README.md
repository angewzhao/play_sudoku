# Play Sudoku!

This module allows players to play an interactive version of Sudoku. 

This version allows the player to choose one of three levels: easy, medium or hard. The game then creates a board depending on the level chosen. It may take a while, so
wait, at most, a minute if the level chosen was "hard". 

Want to watch the board being solved? Watch the backtracking algorithm visualized by clicking the solve button. 

Features also include: a timer to see how long players have been playing, an automatic checker that lets them know if they can put a value there or not, and three levels to play! Each board created is seeded randomly and different each time. 

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


