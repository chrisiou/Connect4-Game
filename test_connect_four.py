import unittest
from source.config import *

"""
Testing is not currently working, but here is how it would be. 
To enable it, I would extend the functionality of the ConnectFour object
for testing, allowing changes to board dimensions, manual input of 
player names and difficulty levels, and the ability to preset board 
values.
"""
class TestConnectFour(unittest.TestCase):
    print("Testing is not currently working, but here is how it would be. To enable it, I would extend the functionality of the ConnectFour object for testing, allowing changes to board dimensions, manual input of player names and difficulty levels, and the ability to preset board values.")
    
    def test_check_winner_horizontal(self):
        # simulate a horizontal win
        BOARD[5] = [1, 1, 1, 1, 0, 0, 0]
        game = ConnectFour("Player", 1)
        self.assertTrue(game.check_winner(PlayerToken))

    def test_check_winner_vertical(self):
        # simulate a vertical win
        BOARD = np.zeros((ROWS_NUM, COLUMNS_NUM), dtype=int)
        BOARD[5][3] = BOARD[4][3] = BOARD[3][3] = BOARD[2][3] = 1
        game = ConnectFour("Player", 1)
        self.assertTrue(game.check_winner(PlayerToken))

    def test_get_valid_columns(self):
        # Test for valid columns
        BOARD[5] = [1, 1, 1, 1, 0, 0, 0]
        game = ConnectFour("Player", 1)
        self.assertEqual(game.get_valid_columns(), [4, 5, 6])

    def test_is_valid_move(self):
        # Test invalid move (column full)
        BOARD[5][3] = 1
        game = ConnectFour("Player", 1)
        self.assertFalse(game.is_valid_move(3))

if __name__ == "__main__":
    unittest.main()
