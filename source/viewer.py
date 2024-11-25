from source.config import *
from source.players import *
import os
import time

class GameViewer():
    def clear_terminal_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display(self):
        self.clear_terminal_screen()
        print("\n  " + "   ".join(map(str, range(1, COLUMNS_NUM + 1))))
        print("+" + "---+" * COLUMNS_NUM)
        for row in BOARD.data:
            print("|" + "|".join(f" {get_token(cell).symbol} " for cell in row) + "|")
            print("+" + "---+" * COLUMNS_NUM)
        print()
        
    def drop_disc_animation(self, column, token):
        for row in range(ROWS_NUM):
            if row > 0:
                BOARD[row - 1][column] = EmptyToken.value  # clear the previous animation position
            BOARD[row][column] = token.value  # set the current animation position
            self.display()
            time.sleep(ANIMATION_DELAY)

            # stop at the first occupied cell below or at the bottom
            if row == ROWS_NUM - 1 or BOARD[row + 1][column] != EmptyToken.value:
                return row, column
    
Viewer = GameViewer()