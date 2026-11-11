
# Module 2 - Exercise 07: 2048 Advance
# A 2048 game with Save and Continue features.
# The player can save the game in a JSON file
# and continue playing later.

import random
import json
from pathlib import Path


# Save the JSON file next to this Python file.
SAVE_FILE = Path(__file__).with_name("2048_save.json")


# Display the game board and current score.
def show_board(board, score):
    print("\n2048 GAME - Score:", score)
    print("+------+------+------+------+")

    for row in board:
        print(
            "|" + "|".join(
                f"{number if number else '.':^6}"
                for number in row
            ) + "|"
        )
        print("+------+------+------+------+")


# Add a new number to a random empty position.
def add_new_tile(board):
    empty_cells = []

    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                empty_cells.append((row, col))

    if empty_cells:
        row, col = random.choice(empty_cells)

        # 90% chance for 2, 10% chance for 4.
        board[row][col] = (
            2 if random.random() < 0.9 else 4
        )


# Merge matching numbers in a row or column.
def merge_line(line):
    numbers = [n for n in line if n != 0]

    result = []
    points = 0
    i = 0

    while i < len(numbers):

        if (
            i + 1 < len(numbers)
            and numbers[i] == numbers[i + 1]
        ):
            combined = numbers[i] * 2
            result.append(combined)
            points += combined
            i += 2

        else:
            result.append(numbers[i])
            i += 1

    # Fill remaining empty positions with zeros.
    while len(result) < 4:
        result.append(0)

    return result, points


# Move all tiles in the chosen direction.
def move_board(board, direction):
    new_board = [[0] * 4 for _ in range(4)]
    points = 0

    for i in range(4):

        # Move left or right.
        if direction in ("a", "d"):
            line = board[i][:]

            if direction == "d":
                line.reverse()

            changed_line, gained = merge_line(line)

            if direction == "d":
                changed_line.reverse()

            new_board[i] = changed_line

        # Move up or down.
        else:
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


# Check if the player can make another move.
def can_move(board):
    for row in range(4):
        for col in range(4):

            # An empty cell means a move is possible.
            if board[row][col] == 0:
                return True

            # Check the cell on the right.
            if col < 3:
                if board[row][col] == board[row][col + 1]:
                    return True

            # Check the cell below.
            if row < 3:
                if board[row][col] == board[row + 1][col]:
                    return True

    return False


# Save the board and score to a JSON file.
def save_game(board, score):
    data = {
        "board": board,
        "score": score
    }

    try:
        with open(
            SAVE_FILE, "w", encoding="utf-8"
        ) as file:
            json.dump(data, file, indent=4)

        print("Game saved successfully!")
        return True

    except OSError:
        print("Error: Could not save the game.")
        return False


# Load a previously saved game.
def load_game():
    try:
        with open(
            SAVE_FILE, "r", encoding="utf-8"
        ) as file:
            data = json.load(file)

        board = data["board"]
        score = data["score"]

        # Check that the saved data is valid.
        valid_board = (
            isinstance(board, list)
            and len(board) == 4
            and all(
                isinstance(row, list)
                and len(row) == 4
                and all(
                    type(number) is int and number >= 0
                    for number in row
                )
                for row in board
            )
        )

        valid_score = (
            type(score) is int and score >= 0
        )

        if not valid_board or not valid_score:
            raise ValueError("Invalid save data")

        print("Saved game loaded successfully!")
        return board, score

    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        UnicodeError
    ):
        print("No valid saved game found.")
        return None


# Create a new game.
def new_game():
    board = [[0] * 4 for _ in range(4)]
    score = 0

    # Start with two random tiles.
    add_new_tile(board)
    add_new_tile(board)

    return board, score


# Main game function.
def play_game():
    print("Welcome to 2048 Advance!")

    # Ask the player to start or continue.
    while True:
        choice = input(
            "New game (N) or Continue (C)? "
        ).strip().lower()

        if choice in ("n", "c"):
            break

        print("Please enter N or C.")

    if choice == "c":
        saved_game = load_game()

        if saved_game is not None:
            board, score = saved_game
        else:
            board, score = new_game()
            print("Starting a new game.")

    else:
        board, score = new_game()

    print("\nGame Controls:")
    print("W = Up")
    print("A = Left")
    print("S = Down")
    print("D = Right")
    print("P = Save")
    print("Q = Save and Quit")

    # Automatically save the starting position.
    save_game(board, score)

    while True:
        show_board(board, score)

        # Stop if there are no available moves.
        if not can_move(board):
            print("Game Over!")
            print("Final Score:", score)
            save_game(board, score)
            break

        direction = input(
            "Your move (W/A/S/D/P/Q): "
        ).strip().lower()

        # Save the game without leaving.
        if direction == "p":
            save_game(board, score)
            continue

        # Save and quit the game.
        if direction == "q":
            if save_game(board, score):
                print("See you next time!")
                break

            # Stay in the game if saving failed.
            continue

        # Check the entered direction.
        if direction not in ("w", "a", "s", "d"):
            print("Invalid direction!")
            continue

        new_board, gained = move_board(
            board, direction
        )

        # Do not add a tile if nothing moved.
        if new_board == board:
            print("No tiles moved. Try again.")
            continue

        board = new_board
        score += gained

        # Check if the player has reached 2048.
        if any(2048 in row for row in board):
            show_board(board, score)
            print("Congratulations! You reached 2048!")
            save_game(board, score)
            break

        # Add a new number after each valid move.
        add_new_tile(board)

        # Automatically save the current session.
        save_game(board, score)


# Start the program.
if __name__ == "__main__":
    play_game()
