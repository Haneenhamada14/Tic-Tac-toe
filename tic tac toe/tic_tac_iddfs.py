# Constants
EMPTY = " "
PLAYER = "X"
COMPUTER = "O"

# Tic Tac Toe game class
class TicTacToe:
    def __init__(self):
        self.board = [EMPTY] * 9
        self.current_player = PLAYER

    def make_move(self, position):
        self.board[position] = self.current_player

    def get_valid_moves(self):
        return [i for i, val in enumerate(self.board) if val == EMPTY]

    def is_winner(self, player):
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
        return self.is_winner(PLAYER) or self.is_winner(COMPUTER) or len(self.get_valid_moves()) == 0

    def switch_players(self):
        self.current_player = PLAYER if self.current_player == COMPUTER else COMPUTER

    def iddfs(self, depth):
        for move in self.get_valid_moves():
            self.make_move(move)
            if self.is_winner(PLAYER):
                self.make_move(move)  # Undo move
                return move
            elif not self.is_game_over() and depth > 1:
                result = self.iddfs(depth - 1)
                if result is not None:
                    self.make_move(move)  # Undo move
                    return move
            self.make_move(move)  # Undo move
        return None

# Main function
def main():
    game = TicTacToe()
    while not game.is_game_over():
        print("Current Board:")
        print(" ".join(game.board[:3]))
        print(" ".join(game.board[3:6]))
        print(" ".join(game.board[6:]))
        print()

        if game.current_player == PLAYER:
            while True:
                try:
                    position = int(input("Enter position (0-8): "))
                    if position in game.get_valid_moves():
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            game.make_move(position)
        else:
            depth = 1
            while True:
                best_move = game.iddfs(depth)
                if best_move is not None:
                    game.make_move(best_move)
                    break
                depth += 1

        game.switch_players()

    print("Game Over!")
    if game.is_winner(PLAYER):
        print("You win!")
    elif game.is_winner(COMPUTER):
        print("Computer wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()
