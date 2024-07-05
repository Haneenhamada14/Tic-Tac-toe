import copy
import tkinter as tk
from tkinter import messagebox
#lastinfirstout
# Function to check if a player has won
def check_winner(board, player):
    # Check rows
    for row in board:
        if row.count(player) == 3:
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Check diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

# Function to perform a depth-first search
def dfs(board, player):
    if check_winner(board, 'X'):
        return -1
    elif check_winner(board, 'O'):
        return 1
    elif len(get_empty_cells(board)) == 0:
        return 0

    if player == 'X':
        best_score = float('-inf')
    else:
        best_score = float('inf')

    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = player
                score = dfs(board, 'O' if player == 'X' else 'X')
                board[i][j] = ''
                if player == 'X':
                    best_score = max(best_score, score)
                else:
                    best_score = min(best_score, score)

    return best_score

# Function to get the empty cells on the board
def get_empty_cells(board):
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                empty_cells.append((i, j))
    return empty_cells

# Function to handle button click event
def handle_click(row, col):
    global board, current_player
    
    if board[row][col] == '':
        board[row][col] = 'X'
        buttons[row][col].config(text='X', state=tk.DISABLED)
        current_player = 'O'
        if not check_game_over():
            make_computer_move()

# Function to make the computer's move
def make_computer_move():
    global board, current_player

    best_score = float('-inf')
    best_move = None
    for move in get_empty_cells(board):
        board[move[0]][move[1]] = 'O'
        score = dfs(board, 'X')
        board[move[0]][move[1]] = ''
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move[0]][best_move[1]] = 'O'
    buttons[best_move[0]][best_move[1]].config(text='O', state=tk.DISABLED)
    current_player = 'X'
    check_game_over()

# Function to check if the game is over
def check_game_over():
    global board, current_player

    if check_winner(board, 'X'):
        messagebox.showinfo("Game Over", "X wins!")
        reset_game()
        return True
    elif check_winner(board, 'O'):
        messagebox.showinfo("Game Over", "O wins!")
        reset_game()
        return True
    elif len(get_empty_cells(board)) == 0:
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_game()
        return True

    return False

# Function to reset the game
def reset_game():
    global board

    for i in range(3):
        for j in range(3):
            board[i][j] = ''
            buttons[i][j].config(text='', state=tk.NORMAL)

# Create the main window
window = tk.Tk()
window.title("Tic Tac Toe")

# Create the game board
board = [['', '', ''], ['', '', ''], ['', '', '']]
buttons = []
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(window, text='', width=10, height=5, command=lambda row=i, col=j: handle_click(row, col))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Initialize the current player
current_player = 'X'

# Start the main loop
window.mainloop()