
# Module 4 - Exercise 04: Where Is My Data?
# This program displays the SQLite database tables,
# their schemas, columns, and stored records.

# Import the SQLite3 module.
import sqlite3

# Import Path to locate the database file.
from pathlib import Path


# Use the database created in previous exercises.
DB_FILE = Path(__file__).with_name("hamad_module4_3.db")


# Function to view database tables and records.
def view_database():

    # Check that the database file exists.
    if not DB_FILE.is_file():
        print("Error: tasks.db was not found.")
        print("Run Exercise 02 and 03 first.")
        return

    # Connect to the existing SQLite database.
    connection = sqlite3.connect(DB_FILE)

    try:
        cursor = connection.cursor()

        print("SQLite Database Viewer")
        print("Database:", DB_FILE.name)

        # Find all user-created tables.
        cursor.execute("""
            SELECT name, sql
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)

        tables = cursor.fetchall()

        # Check if the database has any tables.
        if not tables:
            print("No tables found.")
            return

        print("\nTotal Tables:", len(tables))

        # Display every table.
        for table_name, schema in tables:

            print("\n--------------------------")
            print("Table Name:", table_name)
            print("--------------------------")

            # Display the table schema.
            print("\nTable Schema:")
            print(schema)

            # Read all records from this table.
            # Quote the table name safely.
            safe_name = table_name.replace('"', '""')

            cursor.execute(
                f'SELECT * FROM "{safe_name}"'
            )

            # Get the names of all columns.
            columns = [
                column[0]
                for column in cursor.description
            ]

            # Get all rows from the table.
            rows = cursor.fetchall()

            print("\nColumns:")
            print(columns)

            print("\nTotal Rows:", len(rows))

            # Display the stored data.
            print("\nStored Data:")

            if not rows:
                print("The table is empty.")
            else:
                for row in rows:
                    print(dict(zip(columns, row)))

    except sqlite3.Error as error:

        # Display SQLite errors if they occur.
        print("Database Error:", error)

    finally:
        # Close the database connection.
        connection.close()


# Run the program.
if __name__ == "__main__":
    view_database()
