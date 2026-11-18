
# Module 7 - Exercise 04: Docker Database
# Generate random user data and save it in SQLite.
# Fields: id, name, phone, user_key.

import random
import secrets
import sqlite3
from pathlib import Path


# Database location
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "module7_4_data"
DB_FILE = DATA_DIR / "hamad_module7_4.db"

# Sample names for testing
NAMES = [
    "Hamad",
    "Ali",
    "Sara",
    "Ahmed",
    "Fatima",
    "Mohammed",
    "Noora",
    "Khalid"
]


# Create database and table
def create_database(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            user_key TEXT NOT NULL UNIQUE
        )
    """)


# Generate random test data
def generate_user():
    name = random.choice(NAMES)

    # Fictional test phone number
    phone = f"000-555-01{random.randint(0, 99):02d}"

    # Generate a unique random key
    user_key = secrets.token_hex(8)

    return name, phone, user_key


# Insert random users into SQLite
def add_users(connection, count=5):
    for _ in range(count):
        name, phone, user_key = generate_user()

        connection.execute(
            """
            INSERT INTO users (name, phone, user_key)
            VALUES (?, ?, ?)
            """,
            (name, phone, user_key)
        )


# Display saved records
def display_users(connection):
    cursor = connection.execute("""
        SELECT id, name, phone, user_key
        FROM users
        ORDER BY id
    """)

    print("\nSaved users in SQLite:")
    print("-" * 65)

    for user in cursor.fetchall():
        print(user)

    print("-" * 65)


# Main program
def main():
    print("Welcome to Hamad Docker Database!")

    # Ensure the database directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_FILE) as connection:

        create_database(connection)

        # Insert 5 new random users
        add_users(connection, count=5)

        connection.commit()

        # Display saved data
        display_users(connection)

    print("\nDatabase saved successfully!")
    print("Database file:", DB_FILE)


if __name__ == "__main__":
    main()
