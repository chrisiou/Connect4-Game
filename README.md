# Connect Four Game - Python Implementation

A try-to-be fun, interactive implementation of the classic **Connect Four** game in Python. This game features a human player battling against a computer with three difficulty levels: Easy, Medium, and Difficult. The computer uses some strategies (mostly defensive tactics) to make its moves, especially in the Difficult mode.

```
Connect 4 Game

  1   2   3   4   5   6   7
+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+
|   |   |   |   | X |   |   |
+---+---+---+---+---+---+---+
|   |   |   |   | O |   |   |
+---+---+---+---+---+---+---+
| X |   |   | X | O |   |   |
+---+---+---+---+---+---+---+

Your turn (1-7): 4
Calculating... 📈
Hmm, how about this move? 🤔

```

## Features
1. **Player vs Computer** gameplay on a 6x7 grid.
2. **Difficulty levels**:
   - **Easy:** Random moves by the computer.
   - **Medium:** Basic defensive strategy to block winning moves by detecting threats like "three-in-a-row.
   - **Difficult:** Advanced defensive strategy to look ahead for Two-in-a-Row threats. Check for positions where the Player can create two potential winning moves in the next turn. It prevents the Player from setting up these "double threats" by blocking this position.

## How It Works
### **Game Components**
- **Game Board:** A 6x7 grid represented by a NumPy array. The rows and columns of the board are indexed from `0`.
- **Tokens:** The player's discs are represented by `X`, and the computer's discs are represented by `O`.
- **Modules:**
  - `GameViewer`: Handles displaying the game board and animating moves.
  - `Computer`: Contains the logic for the computer's move selection.
  - `ConnectFour`: Manages the game loop, alternates turns, and checks for winners.

### **Gameplay Flow**
1. The game begins with the player choosing a difficulty level (Easy, Medium, Difficult).
2. The player and computer alternate turns:
   - **Player Turn:** The player chooses a column to drop their disc.
   - **Computer Turn:** The computer calculates the best move based on the selected difficulty level.
3. After each move, the program checks for a winner or a draw.
4. The game ends when a player forms a vertical, horizontal, or diagonal line of 4 discs, or if the board is full.


## How to Play

### **Prerequisites**
- Python 3.6 or higher.
- Install NumPy if it’s not already installed:
  ```bash
  pip install numpy
  ```

### **Run the Game**
1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Run this script
  ```bash
  python connect_four.py
  ```
4. Follow the prompts to play the game.


## Testing the Code

- Run the test suite
```bash
    pytest test_connect_four.py
```
**Testing is not currently functional*, **but** [here](https://github.com/chrisiou/Connect4-Game/blob/main/test_connect_four.py)’s how it would work if it were implemented.
To enable testing, I would extend the functionality of the `ConnectFour` object to allow changing board's dimensions, manual input of player names and difficulty levels, and the ability to preset board values.


Enjoy the game and may the best strategist win! 🎉
