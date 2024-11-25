import os
from source.config import *
from source.players import *
from source.viewer import Viewer

class ConnectFour():
    def __init__(self):
        self.game_over = False
        self.player_turn = True
        self.player = Player()
        self.computer = Computer(self.player)

    def add_new_token_in_board(self, move, disc):
        Viewer.drop_disc_animation(move, disc)

    def check_winner(self, token):
        if BOARD.check_winner(token):
            Viewer.display()
            if token is self.player.token:
                print(f"Agh\U0001F494.. I mean.. \U0001F389Congratulations {self.player.name}\U0001F389 you won!\U0001F3C6")
            else: # computer won
                print("muahaha\U0001F929 I won - I love this game!\U0001F973")       
            self.game_over = True

    def check_for_draw(self):
        if not self.game_over and not BOARD.get_valid_columns():
            Viewer.display()
            print("It's a draw!")
            self.game_over = True

    def play(self):
        Viewer.display()
        token = EmptyToken
        while not self.game_over:
            if self.player_turn:
                move = self.player.next_move()
                if move == -1: continue
                token = self.player.token
                self.player_turn = False
            else:
                move = self.computer.next_move()
                token = self.computer.token
                self.player_turn = True

            self.add_new_token_in_board(move, token)
            self.check_winner(token)
            self.check_for_draw()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    game = ConnectFour()
    game.play()
    
