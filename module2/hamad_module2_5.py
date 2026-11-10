
# Module 2 - Exercise 05: X/O Game
# Two-player Tic-Tac-Toe game in the terminal.
# Each player enters a name before starting.

# Display the current game board.
def show_board(board):
    print()
    for i in range(0, 9, 3):
        print(" | ".join(board[i:i + 3]))
        if i < 6:
            print("--+---+--")
    print()


# Check all possible winning combinations.
def check_winner(board, player):
    winning_positions = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    # Return True when three positions match.
    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] == player:
            return True

    return False


# Run the game for two players.
def play_game():
    print("Welcome to X/O Game!")

    # Ask both players for their names.
    player_x = input("Enter Player X name: ").strip()
    player_o = input("Enter Player O name: ").strip()

    # Use default names if nothing is entered.
    if not player_x:
        player_x = "Player X"

    if not player_o:
        player_o = "Player O"

    # Store each name with its symbol.
    players = {
        "X": player_x,
        "O": player_o
    }

    print(f"\n{player_x} (X) vs {player_o} (O)")

    # Create the game board.
    board = [str(i) for i in range(1, 10)]

    # X starts the game.
    player = "X"
    moves = 0

    # Keep playing until a win or draw.
    while True:
        show_board(board)

        # Ask the current player for a position.
        choice = input(
            f"{players[player]} ({player}), choose 1-9: "
        ).strip()

        # Accept only numbers from 1 to 9.
        if choice not in [str(i) for i in range(1, 10)]:
            print("Invalid choice! Enter a number from 1 to 9.")
            continue

        # Convert choice to a list index.
        position = int(choice) - 1

        # Check if the position is already taken.
        if board[position] in ["X", "O"]:
            print("Position already taken! Try again.")
            continue

        # Place the current player's symbol.
        board[position] = player
        moves += 1

        # Check if the player wins.
        if check_winner(board, player):
            show_board(board)
            print(f"Congratulations {players[player]}! You win!")
            break

        # Check if the board is full.
        if moves == 9:
            show_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player.
        player = "O" if player == "X" else "X"


# Start the program when run directly.
if __name__ == "__main__":
    play_game()
