
# Module 8 - Exercise 02
# MCP with SQLite Database

import sqlite3
from pathlib import Path
from contextlib import closing
from fastmcp import FastMCP

mcp = FastMCP("Hamad MCP Database")

DB_FILE = Path(__file__).resolve().parent / "hamad_module8_2.db"


# Connect to database (read-only)
def connect_db():
    if not DB_FILE.exists():
        raise FileNotFoundError("Database file not found")

    connection = sqlite3.connect(
        DB_FILE.as_uri() + "?mode=ro",
        uri=True
    )
    connection.row_factory = sqlite3.Row
    return connection


# Tool 1: Count users
@mcp.tool
def get_total_users() -> int:
    """Get total number of users in database."""

    with closing(connect_db()) as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()
        return result[0]


# Tool 2: Show users
@mcp.tool
def list_users() -> list[dict]:
    """Show all users saved in SQLite."""

    with closing(connect_db()) as conn:
        rows = conn.execute(
            "SELECT id, name, phone, user_key FROM users"
        ).fetchall()
        return [dict(row) for row in rows]


# Tool 3: Find user by ID
@mcp.tool
def get_user_by_id(user_id: int) -> dict:
    """Find one user using an ID."""

    with closing(connect_db()) as conn:
        row = conn.execute(
            "SELECT id, name, phone, user_key FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if row is None:
            return {"message": "User not found"}

        return dict(row)


if __name__ == "__main__":
    mcp.run()
