
# Module 4 - Exercise 07: Messy Database
# Approach 2: Sort data using Python sorted()

import sqlite3
from pathlib import Path

# Database file
DB_FILE = Path(__file__).with_name("hamad_module4_4.db")


def sort_with_python():

    # Check if the database exists.
    if not DB_FILE.is_file():
        print("Database not found!")
        return

    # Connect to SQLite.
    connection = sqlite3.connect(DB_FILE)

    try:
        cursor = connection.cursor()

        # Read tasks without SQL sorting.
        cursor.execute("""
            SELECT id, title, missing_field
            FROM tasks
        """)

        rows = cursor.fetchall()

        # Sort using the Python function sorted().
        # row[2] is the missing_field value.
        sorted_rows = sorted(
            rows,
            key=lambda row: (row[2] or "").lower()
        )

        print("Approach 2: Python sorted()")

        for row in sorted_rows:
            print(row)

    except sqlite3.Error as error:
        print("Database Error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    sort_with_python()
