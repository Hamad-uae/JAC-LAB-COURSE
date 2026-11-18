
# Module 7 - Exercise 05
# Docker Database V2
#
# Add users to the existing Exercise 04 database.
# Never delete old users or recreate the database.

import sqlite3
import secrets
from pathlib import Path


# Use the SAME database as Exercise 04
DATA_DIR = Path(__file__).resolve().parent / "module7_4_data"
DB_FILE = DATA_DIR / "hamad_module7_4.db"


def create_table(connection):
    # This creates the table ONLY if it does not exist.
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            user_key TEXT NOT NULL UNIQUE
        )
    """)
    connection.commit()


def show_users(connection):
    rows = connection.execute("""
        SELECT id, name, phone, user_key
        FROM users
        ORDER BY id
    """).fetchall()

    print("\n--- Saved Users ---")

    for row in rows:
        print(row)

    print("-------------------")
    print("Total users:", len(rows))


def add_user(connection, name, phone, user_key):
    connection.execute(
        """
        INSERT INTO users (name, phone, user_key)
        VALUES (?, ?, ?)
        """,
        (name, phone, user_key)
    )

    connection.commit()
    print("\nNew user saved successfully!")


def main():
    print("Welcome to Hamad Docker Database V2!")
    print("Old database records will be preserved.")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_FILE)

    try:
        create_table(connection)

        # Display existing users first
        show_users(connection)

        while True:
            print("\n--- Add New User ---")

            name = input(
                "Enter name (or exit): "
            ).strip()

            if name.lower() == "exit":
                break

            if not name:
                print("Name cannot be empty.")
                continue

            phone = input(
                "Enter phone number: "
            ).strip()

            if not phone:
                print("Phone cannot be empty.")
                continue

            user_key = input(
                "Enter user key (Enter = random): "
            ).strip()

            if not user_key:
                user_key = secrets.token_hex(8)

            try:
                add_user(
                    connection,
                    name,
                    phone,
                    user_key
                )

            except sqlite3.IntegrityError:
                print("This user key already exists.")
                continue

            # Show old and new records together
            show_users(connection)

        print("\nFinal database records:")
        show_users(connection)
        print("\nGoodbye!")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
