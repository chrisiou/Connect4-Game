import numpy as np
import random
import os
import time

ROW_COUNT = 6
COLUMN_COUNT = 7
EMPTY = 0
PLAYER_DISC = 1
COMPUTER_DISC = 2
ANIMATION_DELAY = 0.1  # in secs

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


class ConnectFour:
    def __init__(self, name):
        self.board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
        self.player_name = name
        self.game_over = False
        self.player_turn = True

    def clear_terminal_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_board(self):
        self.clear_terminal_screen()
        print("\n  " + "   ".join(map(str, range(1, COLUMN_COUNT + 1))))
        print("+" + "---+" * COLUMN_COUNT)
        for row in self.board:
            print("|" + "|".join(f" {self.get_disc_symbol(cell)} " for cell in row) + "|")
            print("+" + "---+" * COLUMN_COUNT)
        print()

    @staticmethod
    def get_disc_symbol(disc):
        if disc == PLAYER_DISC:
            return "X"
        elif disc == COMPUTER_DISC:
            return "O"
        else:
            return " "  # empty cell

    def is_valid_move(self, column):
        return self.board[0][column] == EMPTY

    def drop_disc_animated(self, column, disc):
        for row in range(ROW_COUNT):
            if row > 0:
                self.board[row - 1][column] = EMPTY  # clear the previous animation position
            self.board[row][column] = disc  # Set the current animation position
            self.print_board()
            time.sleep(ANIMATION_DELAY)

            # Stop at the first occupied cell below or at the bottom
            if row == ROW_COUNT - 1 or self.board[row + 1][column] != EMPTY:
                return row, column

    def check_winner(self, disc):
        # check horizontal
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                if all(self.board[r][c + i] == disc for i in range(4)):
                    return True

        # check vertical
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT):
                if all(self.board[r + i][c] == disc for i in range(4)):
                    return True

        # check bottom-left diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                if all(self.board[r + i][c + i] == disc for i in range(4)):
                    return True

        # check bottom-right diagonal
        for r in range(3, ROW_COUNT):
            for c in range(COLUMN_COUNT - 3):
                if all(self.board[r - i][c + i] == disc for i in range(4)):
                    return True

        return False

    def get_valid_columns(self):
        return [c for c in range(COLUMN_COUNT) if self.is_valid_move(c)]

    def computer_move(self):
        valid_columns = self.get_valid_columns()
        return random.choice(valid_columns)

    def play(self):
        self.print_board()

        while not self.game_over:
            if self.player_turn:
                try:
                    move = int(input("Your turn (1-7): ")) - 1
                    if move is -1:
                        exit()
                    if move not in range(COLUMN_COUNT):
                        print("Invalid column. Please choose between 1 and 7.")
                        continue
                    if not self.is_valid_move(move):
                        print("Column is full. Choose a different column.")
                        continue

                    row, col = self.drop_disc_animated(move, PLAYER_DISC)
                    if self.check_winner(PLAYER_DISC):
                        self.print_board()
                        print(f"Agh\U0001F494.. I mean.. \U0001F389Congratulations {self.player_name}\U0001F389 you won!\U0001F3C6")
                        self.game_over = True
                    self.player_turn = False
                except ValueError:
                    print("Please enter a valid column number or 0 to exit.")
            else:
                print(random.choice(reactions))
                time.sleep(0.8)
                move = self.computer_move()
                row, col = self.drop_disc_animated(move, COMPUTER_DISC)
                if self.check_winner(COMPUTER_DISC):
                    self.print_board()
                    print("muahaha\U0001F929 I won - I love this game!\U0001F973")
                    self.game_over = True
                self.player_turn = True

            # check for draw
            if not self.get_valid_columns() and not self.game_over:
                self.print_board()
                print("It's a draw!")
                self.game_over = True


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Greetings, Human! What's your name?")
    name = input()
    print(f"Ah, {name}, a name fit for a Connect 4 champion (or so you hope\U0001F60B)!\n")
    time.sleep(0.8)

    game = ConnectFour(name)
    game.play()
    
