import random
import time
from source.config import *
from source.viewer import Viewer

class Move:
    # return a tmp board with the hypothetical new token at this column 
    def simulate_move(self, board, column, token):
        tmp_board = board.copy()
        for row in range(ROWS_NUM - 1, -1, -1):  # start from the bottom row
            if tmp_board[row][column] == 0:
                tmp_board[row][column] = token.value
                break
        return tmp_board
    
    def is_possible_move(self, row, column):
        if BOARD.is_valid_move(column): # is column already full?
            return False
        if BOARD[row][column] != EmptyToken.value: # is available position?
            return False
        if row < ROWS_NUM-2:
            if BOARD[row + 1][column] == EmptyToken.value: # is there below another token?
                return False
        return True


class Player():
    token = PlayerToken

    def __init__(self):
       self.name = self.set_player_name()

    def set_player_name(self):
        print("Greetings, Human! What's your name?")
        name = input("  name: ")
        print(f"Ah, {name}, a name fit for a Connect 4 champion (or so you hope\U0001F60B)!\n")
        return name
    
    def next_move(self):
        try:
            move = int(input("Your turn (1-7): ")) - 1
            if move == -1:
                exit()
            if move not in range(COLUMNS_NUM):
                print("Invalid column. Please choose between 1 and 7.")
                return -1
            if not BOARD.is_valid_move(move):
                print("Column is full. Choose a different column.")
                return -1
            return move
        except ValueError:
            print("Please enter a valid column number or 0 to exit.")
            return -1
        
class Computer(Move):
    token =  ComputerToken

    def __init__(self, opponent):
        self.level = self.set_difficulty()
        self.opponent = opponent
        self.reactions = [
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
    
    def set_difficulty(self):
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
                    print("Let the fun begin! You play first!")
                    time.sleep(0.8)
                break
            except ValueError:
                print("Please enter an integer number or 0 to exit.")
        return level


    # check if there is possibility to strike 4
    def check_for_3_consecutive_pieces(self, token):
        for row in range(ROWS_NUM):
            for col in range(COLUMNS_NUM):
                # check horizontal
                if col <= COLUMNS_NUM - 4:
                    opponent_tokens = 0
                    for i in range(4):
                        if BOARD[row][col + i] == token.value:
                            opponent_tokens += 1
                        else:
                            next_move = col + i
                    if opponent_tokens == 3 and self.is_possible_move(row, next_move):
                        return next_move

                # check vertical
                if row <= ROWS_NUM - 4:
                    opponent_tokens = 0
                    for i in range(4):
                        if BOARD[row + i][col] == token.value:
                            opponent_tokens += 1
                        else:
                            next_move = row + i
                    if opponent_tokens == 3 and self.is_possible_move(next_move, col):
                        return col

                # check right-bottom diagonal direction
                if row <= ROWS_NUM - 4 and col <= COLUMNS_NUM - 4:
                    opponent_tokens = 0
                    for i in range(4):
                        if BOARD[row + i][col + i] == token.value:
                            opponent_tokens += 1
                        else:
                            next_move =  i
                    if opponent_tokens == 3 and self.is_possible_move(row + next_move, col + next_move):
                        return col + next_move

                # check left-bottom diagonal direction
                if row <= ROWS_NUM - 4 and col >=3:
                    opponent_tokens = 0
                    for i in range(4):
                        if BOARD[row + i][col - i] == token.value:
                            opponent_tokens += 1
                        else:
                            next_move =  i
                    if opponent_tokens == 3 and self.is_possible_move(row + next_move, col - next_move):
                        return col - next_move
        return None
    
    def detect_double_threat(self, column):
        # detect if placing a piece in this column allows the opponent to create two potential winning moves.
        tmp_board = self.simulate_move(BOARD, column, self.opponent.token)
        winning_moves = 0
        for test_col in range(COLUMNS_NUM):
            # check if placing in test_col leads to a win for the opponent
            if tmp_board[0, test_col] == 0:  # only test valid columns
                simulated_board = self.simulate_move(tmp_board, test_col, self.opponent.token)
                if Board.check_winner(simulated_board, self.opponent.token):
                    winning_moves += 1
        return winning_moves >= 2 

    # returns the winning column, otherwise None
    def can_win(self):
        return self.check_for_3_consecutive_pieces(self.token)

    def next_move(self):
        print(random.choice(self.reactions))
        time.sleep(0.8)
        
        valid_columns = BOARD.get_valid_columns()
        if self.level == 1: # easy mode (random position)
            return random.choice(valid_columns)
        
        win = self.can_win()
        if win is not None:
            return win
        
        prevent_opponent_win = self.check_for_3_consecutive_pieces(self.opponent.token)
        if prevent_opponent_win is not None:
            return prevent_opponent_win
        
        # hard mode
        if self.level == 3:
            for c in range(COLUMNS_NUM):
                if self.detect_double_threat(c):
                    return c

        # prevent opponent to monopolize the area at the middle
        if BOARD.is_valid_move(COLUMNS_NUM//2):
            return COLUMNS_NUM//2 + random.choice([-1,0,1])
        return random.choice(valid_columns)
