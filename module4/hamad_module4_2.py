
# Module 4 - Exercise 02: Schema
# Create a SQLite3 database with a tasks table.
# The table stores task details and creation time.

# Import the SQLite3 module.
import sqlite3

# Import Path to locate the database file.
from pathlib import Path


# Store the database next to the Python file.
DB_FILE = Path(__file__).with_name("tasks.db")


# Function to create the database and table.
def create_database():

    # Connect to the SQLite database.
    # The file will be created if it does not exist.
    connection = sqlite3.connect(DB_FILE)

    try:
        cursor = connection.cursor()

        # Create the tasks table with five columns.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Save changes to the database.
        connection.commit()

        print("Database created successfully!")
        print("Database file: tasks.db")
        print("Table name: tasks")

        # Read the table schema from SQLite.
        cursor.execute("""
            SELECT sql
            FROM sqlite_master
            WHERE type = 'table' AND name = 'tasks'
        """)

        schema = cursor.fetchone()

        # Display the schema in the terminal.
        if schema:
            print("\nTasks Table Schema:")
            print(schema[0])

        # Display the names of all table columns.
        cursor.execute("PRAGMA table_info(tasks)")
        columns = cursor.fetchall()

        print("\nTable Columns:")

        for column in columns:
            print(column[1], "-", column[2])

    finally:
        # Close the database connection.
        connection.close()


# Run the main function.
if __name__ == "__main__":
    create_database()
