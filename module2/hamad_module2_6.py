# Module 2 - Exercise 06: 2048
# A terminal-based 2048 game for one player.
# Use W (up), A (left), S (down), D (right), or Q (quit).

import random


# Display the board and the current score.
def show_board(board, score):
    print("\n2048 GAME | Score:", score)
    print("+------+------+------+------+")
    for row in board:
        print("|" + "|".join(f"{number or '.':^6}" for number in row) + "|")
        print("+------+------+------+------+")


# Add a 2 or a 4 to a randomly selected empty cell.
def add_new_tile(board):
    empty_cells = [
        (row, col)
        for row in range(4)
        for col in range(4)
        if board[row][col] == 0
    ]

    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 2 if random.random() < 0.9 else 4


# Move a row toward the left and merge equal neighboring numbers.
def merge_line(line):
    numbers = [number for number in line if number != 0]
    result = []
    points = 0
    i = 0

    while i < len(numbers):
        if i + 1 < len(numbers) and numbers[i] == numbers[i + 1]:
            combined = numbers[i] * 2
            result.append(combined)
            points += combined
            i += 2  # Skip both numbers: a new tile merges only once per turn.
        else:
            result.append(numbers[i])
            i += 1

    # Fill remaining cells with zeros to make exactly four cells.
    return result + [0] * (4 - len(result)), points


# Move every row or column in the chosen direction.
def move_board(board, direction):
    new_board = [[0] * 4 for _ in range(4)]
    points = 0

    for i in range(4):
        if direction in ("a", "d"):
            # A and D work with horizontal rows.
            line = board[i][:]
            if direction == "d":
                line.reverse()

            changed_line, gained = merge_line(line)

            if direction == "d":
                changed_line.reverse()
            new_board[i] = changed_line
        else:
            # W and S work with vertical columns.
            line = [board[row][i] for row in range(4)]
            if direction == "s":
                line.reverse()

            changed_line, gained = merge_line(line)

            if direction == "s":
                changed_line.reverse()
            for row in range(4):
                new_board[row][i] = changed_line[row]

        points += gained

    return new_board, points


# Check whether at least one valid move is still possible.
def can_move(board):
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                return True
            if col < 3 and board[row][col] == board[row][col + 1]:
                return True
            if row < 3 and board[row][col] == board[row + 1][col]:
                return True
    return False


# Start and manage the game.
def play_game():
    board = [[0] * 4 for _ in range(4)]
    score = 0

    # Start with two random tiles.
    add_new_tile(board)
    add_new_tile(board)

    print("Welcome to 2048!")
    print("Controls: W = Up, A = Left, S = Down, D = Right, Q = Quit")

    while True:
        show_board(board, score)

        if not can_move(board):
            print("Game over! No more moves. Final score:", score)
            break

        direction = input("Your move (W/A/S/D/Q): ").strip().lower()

        if direction == "q":
            print("Thanks for playing! Final score:", score)
            break

        if direction not in ("w", "a", "s", "d"):
            print("Invalid input. Use W, A, S, D, or Q.")
            continue

        new_board, gained = move_board(board, direction)

        # A move that changes nothing does not create another tile.
        if new_board == board:
            print("No tiles moved. Choose another direction.")
            continue

        board = new_board
        score += gained

        if any(2048 in row for row in board):
            show_board(board, score)
            print("Congratulations! You reached 2048!")
            break

        add_new_tile(board)


# Run the game only when this file is executed directly.
if __name__ == "__main__":
    play_game()
