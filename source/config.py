import numpy as np

ROWS_NUM = 6
COLUMNS_NUM = 7
ANIMATION_DELAY = 0.1  # in secs

class Token():
    def __init__(self, name, disc_symbol, value_in_board):
        self.name = name            # EMPTY, PLAYER, COMPUTER
        self.symbol = disc_symbol   # " ", "X", "O"
        self.value = value_in_board # 0, 1, 2

EmptyToken = Token("EMPTY", " ", 0)
PlayerToken =  Token("PLAYER", "X", 1)
ComputerToken =  Token("COMPUTER", "0", 2)

def get_token(value):
    if value == PlayerToken.value:
        return PlayerToken
    elif value == ComputerToken.value:
        return ComputerToken
    return EmptyToken


class Board():
    def __init__(self):
        self.rows = ROWS_NUM
        self.columns = COLUMNS_NUM
        self.data = np.zeros((self.rows,self.columns), dtype=int)

    def copy(self):
        new_instance = Board()
        new_instance.data = self.data.copy()
        return new_instance
        
    def __getitem__(self, row_index):
        return self.data[row_index]
    
    # check if column is already full
    def is_valid_move(self, column):
        return self.data[0][column] == int(EmptyToken.value)

    def get_valid_columns(self):
        return [c for c in range(COLUMNS_NUM) if self.is_valid_move(c)]

    def check_winner(self, token):
        # check horizontal
        for r in range(ROWS_NUM):
            for c in range(COLUMNS_NUM - 3):
                if all(self.data[r][c + i] == token.value for i in range(4)):
                    return True

        # check vertical
        for r in range(ROWS_NUM - 3):
            for c in range(COLUMNS_NUM):
                if all(self.data[r + i][c] == token.value for i in range(4)):
                    return True

        # check bottom-left diagonal
        for r in range(ROWS_NUM - 3):
            for c in range(COLUMNS_NUM - 3):
                if all(self.data[r + i][c + i] == token.value for i in range(4)):
                    return True

        # check bottom-right diagonal
        for r in range(3, ROWS_NUM):
            for c in range(COLUMNS_NUM - 3):
                if all(self.data[r - i][c + i] == token.value for i in range(4)):
                    return True

        return False

BOARD = Board()
