
# Module 4 - Exercise 03: Insert
# Create a POST API to insert two tasks
# into the existing SQLite database.

import sqlite3
from pathlib import Path

from fastapi import FastAPI, Body, HTTPException


# Create the FastAPI application.
app = FastAPI()


# Use the database created in Exercise 02.
DB_FILE = Path(__file__).with_name("tasks.db")


# Create a POST endpoint to insert two tasks.
@app.post("/tasks", status_code=201)
def insert_tasks(
    tasks: list[dict] = Body(..., embed=True)
):

    # Check that exactly two tasks are provided.
    if len(tasks) != 2:
        raise HTTPException(
            status_code=422,
            detail="You must provide exactly 2 tasks"
        )

    # Validate the tasks before saving them.
    new_tasks = []

    for task in tasks:
        title = task.get("title")
        description = task.get("description", "")
        status = task.get("status", "pending")

        # Check that the title is a valid string.
        if not isinstance(title, str) or not title.strip():
            raise HTTPException(
                status_code=422,
                detail="Each task must have a title"
            )

        # Check the other text fields.
        if not isinstance(description, str):
            raise HTTPException(
                status_code=422,
                detail="Description must be text"
            )

        if not isinstance(status, str):
            raise HTTPException(
                status_code=422,
                detail="Status must be text"
            )

        new_tasks.append(
            (title.strip(), description, status)
        )

    # Check that the database already exists.
    if not DB_FILE.is_file():
        raise HTTPException(
            status_code=500,
            detail="Run Exercise 02 to create tasks.db first"
        )

    # Connect to the SQLite database.
    connection = sqlite3.connect(DB_FILE)

    try:
        cursor = connection.cursor()

        # Check that the tasks table exists.
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'tasks'
        """)

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=500,
                detail="Tasks table does not exist"
            )

        inserted_ids = []

        # Insert two rows into the tasks table.
        for title, description, status in new_tasks:
            cursor.execute("""
                INSERT INTO tasks
                (title, description, status)
                VALUES (?, ?, ?)
            """, (title, description, status))

            # Get the ID of the inserted row.
            inserted_ids.append(cursor.lastrowid)

        # Save the new rows permanently.
        connection.commit()

        # Return the result to the user.
        return {
            "message": "Two tasks inserted successfully",
            "inserted_count": len(inserted_ids),
            "inserted_ids": inserted_ids
        }

    except sqlite3.Error:
        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error while inserting tasks"
        )

    finally:
        # Close the database connection.
        connection.close()
