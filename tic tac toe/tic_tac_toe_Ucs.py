import tkinter as tk
from tkinter import messagebox
#constains
EMPTY = " "
PLAYER = "X"
COMPUTER = "O"

class TicTacToe:
    def __init__(self):
        # Initializing the game board and current player
        self.board = [EMPTY] * 9
        self.current_player = PLAYER

    def make_move(self, position):
        # Update the game board with the current player's move at a specified position
        self.board[position] = self.current_player

    def get_valid_moves(self):
        # Get a list of valid moves (positions) available on the board
        return [i for i, val in enumerate(self.board) if val == EMPTY]

    def is_winner(self, player):
        # Check if a given player has won based on the winning patterns (rows, columns, and diagonals)
        winning_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for pattern in winning_patterns:
            if all(self.board[i] == player for i in pattern):
                return True
        return False

    def is_game_over(self):
        # Check if the game is over due to a win or tie
        return self.is_winner(PLAYER) or self.is_winner(COMPUTER) or len(self.get_valid_moves()) == 0

    def switch_players(self):
        # Change the current player for the next move
        self.current_player = PLAYER if self.current_player == COMPUTER else COMPUTER

    def ucs(self):
        # Initiates the Uniform Cost Search (UCS) to find the best move
        best_move = self.search()
        return best_move

    def search(self):
        # Perform a search for the best move among the valid moves
        best_score = float("inf")
        best_move = None
        for move in self.get_valid_moves():
            self.make_move(move)
            score = self.uniform_cost_search()
            self.make_move(move)
            if score < best_score:
                best_score = score
                best_move = move
        return best_move

    def uniform_cost_search(self):
        # Implement the Uniform Cost Search algorithm recursively to evaluate the game states and determine the best move
        if self.is_winner(PLAYER):
            return -1
        elif self.is_winner(COMPUTER):
            return 1
        elif len(self.get_valid_moves()) == 0:
            return 0

        best_score = float("-inf")
        for move in self.get_valid_moves():
            self.make_move(move)
            score = self.uniform_cost_search()
            self.make_move(move)
            best_score = max(score, best_score)
        return best_score

class TicTacToeGUI:
    def __init__(self, root):
        # Initialize the graphical user interface for the Tic Tac Toe game using Tkinter
        self.root = root
        self.root.title("Tic Tac Toe")
        self.game = TicTacToe()
        self.buttons = []
        self.create_board()

    def create_board(self):
        # Generate a 3x3 grid of buttons (representing the game board) and bind each button to the make_move method
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=EMPTY, width=10, height=4,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def make_move(self, row, col):
        # Handle the player's move by updating the GUI and checking for game over conditions after the move
        if self.game.board[row * 3 + col] == EMPTY and not self.game.is_game_over():
            self.buttons[row * 3 + col].config(text=PLAYER)
            self.game.make_move(row * 3 + col)
            if self.game.is_game_over():
                self.show_game_result()
            else:
                self.computer_move()

    def computer_move(self):
        # Trigger the computer's move by calling the UCS algorithm to find the best move and update the GUI accordingly
        best_move = self.game.ucs()
        if best_move is not None:
            self.buttons[best_move].config(text=COMPUTER)
            self.game.make_move(best_move)
            if self.game.is_game_over():
                self.show_game_result()

    def show_game_result(self):
        # Display the game result in a message box based on the game outcome (win, lose, or tie)
        if self.game.is_winner(PLAYER):
            messagebox.showinfo("Game Over", "You win!")
        elif self.game.is_winner(COMPUTER):
            messagebox.showinfo("Game Over", "Computer wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")

        self.reset_board()

    def reset_board(self):
        # Reset the game board and GUI for a new game
        self.game = TicTacToe()
        for button in self.buttons:
            button.config(text=EMPTY)

def main():
    # Start the game by initializing the Tkinter root window
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
