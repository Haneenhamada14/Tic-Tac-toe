import tkinter as tk
from tkinter import messagebox
#firstinfirstout
# Game constants
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "

# Game board
board = [[EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]

# BFS algorithm to find the best move
def bfs(board):
    queue = [(board, 0)]
    while queue:
        current_board, depth = queue.pop(0)
        result = check_winner(current_board)
        if result == PLAYER_X:
            return -1 * depth
        elif result == PLAYER_O:
            return depth
        elif result == "tie":
            return 0
        else:
            for i in range(3):
                for j in range(3):
                    if current_board[i][j] == EMPTY:
                        new_board = [row[:] for row in current_board]
                        new_board[i][j] = PLAYER_O
                        queue.append((new_board, depth + 1))
    return 0

# Check if there is a winner
def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    # Check for tie
    if all(board[i][j] != EMPTY for i in range(3) for j in range(3)):
        return "tie"
    return None

# Make a player move
def make_move(row, col):
    global board
    if board[row][col] == EMPTY:
        board[row][col] = PLAYER_X
        update_board()
        result = check_winner(board)
        if result is None:
            best_score = float("-inf")
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = PLAYER_O
                        score = bfs(board)
                        board[i][j] = EMPTY
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
            if best_move is not None:
                board[best_move[0]][best_move[1]] = PLAYER_O
                update_board()
                result = check_winner(board)
        if result == PLAYER_X:
            messagebox.showinfo("Game Over", "You win!")
            reset_game()
        elif result == PLAYER_O:
            messagebox.showinfo("Game Over", "You lose!")
            reset_game()
        elif result == "tie":
            messagebox.showinfo("Game Over", "It's a tie!")
            reset_game()

# Update the GUI board
def update_board():
    for i in range(3):
        for j in range(3):
            button_texts[i][j].set(board[i][j])

# Reset the game
def reset_game():
    global board
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]
    update_board()

# Create the GUI
root = tk.Tk()
root.title("Tic Tac Toe")

button_texts = [[tk.StringVar() for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, textvariable=button_texts[i][j], font=("Arial", 20), padx=20, pady=20,
                                 command=lambda row=i, col=j: make_move(row, col))
        buttons[i][j].grid(row=i, column=j, sticky="nsew")

reset_button = tk.Button(root, text="Reset", font=("Arial", 14), padx=20, pady=10, command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

# Start the game
root.mainloop()