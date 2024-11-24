import numpy as np
import random
import os
import time
from enum import Enum

ROWS_NUM = 6
COLUMNS_NUM = 7
ANIMATION_DELAY = 0.1  # in secs

BOARD = np.zeros((ROWS_NUM,COLUMNS_NUM), dtype=int)


reactions = [
    "\U0001F914", 
    "Give me a sec, please..",
    "It's my turn.. \U0001F914",
    "Haa.. That's easy!",
    "Let me think... \U0001F914",
    "I got this! \U0001F91D", 
    "Hmm, how about this move? \U0001F914",
    "I've got a plan... \U0001F91D",
    "Calculating... \U0001F4C8", 
    "You won't beat me that easily! \U0001F608", 
    "Haha, I'm on fire! \U0001F525", 
    "Oh, that was too easy! \U0001F60E", 
    "Nice try! \U0001F609",  
    "Let's see how you handle this... \U0001F4A1", 
    "Hmm... this is interesting... \U0001F914", 
    "Are you sure you want to do that? \U0001F928"
]

class Disc(Enum):
    EMPTY = 0
    PLAYER = 1
    COMPUTER = 2

class GameViewer:
    def clear_terminal_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display(self):
        self.clear_terminal_screen()
        print("\n  " + "   ".join(map(str, range(1, COLUMNS_NUM + 1))))
        print("+" + "---+" * COLUMNS_NUM)
        for row in BOARD:
            print("|" + "|".join(f" {self.get_disc_symbol(cell)} " for cell in row) + "|")
            print("+" + "---+" * COLUMNS_NUM)
        print()
        
    def drop_disc_animation(self, column, disc):
        for row in range(ROWS_NUM):
            if row > 0:
                BOARD[row - 1][column] = Disc.EMPTY.value  # clear the previous animation position
            BOARD[row][column] = disc  # set the current animation position
            self.display()
            time.sleep(ANIMATION_DELAY)

            # Stop at the first occupied cell below or at the bottom
            if row == ROWS_NUM - 1 or BOARD[row + 1][column] != Disc.EMPTY.value:
                return row, column
    
    @staticmethod
    def get_disc_symbol(disc):
        if disc == Disc.PLAYER.value:
            return "X"
        elif disc == Disc.COMPUTER.value:
            return "O"
        else:
            return " "  # empty cell
        
class ComputerMove:
    def __init__(self, level):
        self.level = level

    def is_valid_move(self, row, column):
        return BOARD[row][column] == int(Disc.EMPTY.value)

    def get_valid_columns(self):
        return [c for c in range(COLUMNS_NUM) if self.is_valid_move(0,c)]
    
    def check_winner(self, board, disc):
        # check horizontal
        for r in range(ROWS_NUM):
            for c in range(COLUMNS_NUM - 3):
                if all(board[r][c + i] == disc for i in range(4)):
                    return True

        # check vertical
        for r in range(ROWS_NUM - 3):
            for c in range(COLUMNS_NUM):
                if all(board[r + i][c] == disc for i in range(4)):
                    return True

        # check bottom-left diagonal
        for r in range(ROWS_NUM - 3):
            for c in range(COLUMNS_NUM - 3):
                if all(board[r + i][c + i] == disc for i in range(4)):
                    return True

        # check bottom-right diagonal
        for r in range(3, ROWS_NUM):
            for c in range(COLUMNS_NUM - 3):
                if all(board[r - i][c + i] == disc for i in range(4)):
                    return True

        return False
    
    
    def check_for_3_consecutive_pieces(self): # returns the next position in order to prevent the opponent to strike 4
        for row in range(ROWS_NUM):
            for col in range(COLUMNS_NUM):
                # check horizontal
                if col <= COLUMNS_NUM - 4:
                    if all(BOARD[row][col + i] == Disc.PLAYER.value for i in range(3)) and self.is_valid_move(row, col + 3):
                        return col + 3

                # check vertical
                if row <= ROWS_NUM - 4:
                    if all(BOARD[row + i][col] == Disc.PLAYER.value for i in range(3)) and self.is_valid_move(row + 3, col):
                        return col

                # check bottom-right diagonal
                if row <= ROWS_NUM - 4 and col <= COLUMNS_NUM - 4:
                    if all(BOARD[row + i][col + i] == Disc.PLAYER.value for i in range(3)) and self.is_valid_move(row + 3, col + 3):
                        return col + 3

                # Check bottom-left diagonal direction
                if row >= 3 and col <= COLUMNS_NUM - 4:
                    if all(BOARD[row - i][col + i] == Disc.PLAYER.value for i in range(3)) and self.is_valid_move(row - 3, col + 3):
                        return col + 3
        return None
    
    def simulate_move(self, board, column, disc): # return a tmp board with the hypothetical computer's move
        tmp_board = board.copy()
        for row in range(ROWS_NUM - 1, -1, -1):  # start from the bottom row
            if tmp_board[row, column] == 0:
                tmp_board[row, column] = disc.value
                break
        return tmp_board
    
    def detect_double_threat(self, column):
        # detect if placing a piece in this column allows the opponent to create two potential winning moves.
        tmp_board = self.simulate_move(BOARD, column, Disc.COMPUTER)
        winning_moves = 0
        for test_col in range(COLUMNS_NUM):
            # check if placing in test_col leads to a win for the opponent
            if tmp_board[0, test_col] == 0:  # only test valid columns
                simulated_board = self.simulate_move(tmp_board, test_col, Disc.PLAYER)
                if self.check_winner(simulated_board, Disc.PLAYER):
                    winning_moves += 1
        return winning_moves >= 2    

    def next_move(self):
        valid_columns = self.get_valid_columns()
        if self.level == 1: # easy mode (random position)
            return random.choice(valid_columns)
        
        save_the_game = self.check_for_3_consecutive_pieces() # TODO: debug this one
        if save_the_game is not None:
            return save_the_game

        # hard mode
        if self.level == 3:
            for c in range(COLUMNS_NUM):
                if self.detect_double_threat(c):
                    return c

        # prevent the opponent to monopolize the middle column
        if self.is_valid_move(0,3):
            return 3
        return random.choice(valid_columns)


        

class ConnectFour:
    def __init__(self, name, level):
        self.player_name = name
        self.level = level
        self.game_over = False
        self.player_turn = True
        self.viewer = GameViewer()
        self.computer = ComputerMove(level)

    def is_valid_move(self, column):
        return BOARD[0][column] == int(Disc.EMPTY.value)

    def check_winner(self, disc):
        # check horizontal
        for r in range(ROWS_NUM):
            for c in range(COLUMNS_NUM - 3):
                if all(BOARD[r][c + i] == disc for i in range(4)):
                    return True

        # check vertical
        for r in range(ROWS_NUM - 3):
            for c in range(COLUMNS_NUM):
                if all(BOARD[r + i][c] == disc for i in range(4)):
                    return True

        # check bottom-left diagonal
        for r in range(ROWS_NUM - 3):
            for c in range(COLUMNS_NUM - 3):
                if all(BOARD[r + i][c + i] == disc for i in range(4)):
                    return True

        # check bottom-right diagonal
        for r in range(3, ROWS_NUM):
            for c in range(COLUMNS_NUM - 3):
                if all(BOARD[r - i][c + i] == disc for i in range(4)):
                    return True

        return False
    
    def computer_move(self):
        return self.computer.next_move()

    def get_valid_columns(self):
        return [c for c in range(COLUMNS_NUM) if self.is_valid_move(c)]

    def play(self):
        self.viewer.display()
        while not self.game_over:
            if self.player_turn:
                try:
                    move = int(input("Your turn (1-7): ")) - 1
                    if move is -1:
                        exit()
                    if move not in range(COLUMNS_NUM):
                        print("Invalid column. Please choose between 1 and 7.")
                        continue
                    if not self.is_valid_move(move):
                        print("Column is full. Choose a different column.")
                        continue

                    row, col = self.viewer.drop_disc_animation(move, Disc.PLAYER.value)
                    if self.check_winner(Disc.PLAYER.value):
                        self.viewer.display()
                        print(f"Agh\U0001F494.. I mean.. \U0001F389Congratulations {self.player_name}\U0001F389 you won!\U0001F3C6")
                        self.game_over = True
                    self.player_turn = False
                except ValueError:
                    print("Please enter a valid column number or 0 to exit.")
            else:
                print(random.choice(reactions))
                time.sleep(0.8)
                move = self.computer_move()
                row, col = self.viewer.drop_disc_animation(move, Disc.COMPUTER.value)
                if self.check_winner(Disc.COMPUTER.value):
                    self.viewer.display()
                    print("muahaha\U0001F929 I won - I love this game!\U0001F973")
                    self.game_over = True
                self.player_turn = True

            # check for draw
            if not self.get_valid_columns() and not self.game_over:
                self.viewer.display()
                print("It's a draw!")
                self.game_over = True


def set_difficulty():
    print("Prepare for battle! Choose your difficulty level:")
    while(True):
        try:
            level = int(input("1 - Easy (a walk in the park), 2 - Medium (things get spicy), 3 - Difficult (brace yourself!), 0 - Exit: "))
            if level == 0:
                exit()
            if level not in range(4):
                print("\nHmm... that's not an option. I'll put you on Easy mode. You're welcome!")
                time.sleep(1.5)
            else:
                print("Let the fun begin!")
                time.sleep(0.8)
            break
        except ValueError:
            print("Please enter an integer number or 0 to exit.")
    return level


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Greetings, Human! What's your name?")
    
    name = input("  name: ")
    print(f"Ah, {name}, a name fit for a Connect 4 champion (or so you hope\U0001F60B)!\n")
    level = set_difficulty()
    game = ConnectFour(name, level)
    game.play()
    
