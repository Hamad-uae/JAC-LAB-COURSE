"""Module 8 / Exercise 04 - FastAPI API backed by SQLite."""

import os
import re
import secrets
import sqlite3
from contextlib import asynccontextmanager, closing
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastmcp import Client
from hamad_module8_4_mcp import mcp
from pydantic import BaseModel, Field

DATA_DIR = Path(os.getenv("DATA_DIR", str(Path(__file__).resolve().parent / "data")))
DB_PATH = DATA_DIR / "hamad_module8_4.db"


class NewUser(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    phone: str = Field(min_length=3, max_length=40)


class ChatQuestion(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


def db_connection():
    con = sqlite3.connect(DB_PATH, timeout=15)
    con.row_factory = sqlite3.Row
    return con


@asynccontextmanager
async def lifespan(app: FastAPI):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with closing(db_connection()) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                user_key TEXT NOT NULL UNIQUE
            )
        """)
        con.commit()
    yield


app = FastAPI(title="Hamad AI Database API", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def home_page():
    """Small built-in HTML interface, no Streamlit required."""
    return (Path(__file__).resolve().parent / "hamad_module8_4_ui.html").read_text(
        encoding="utf-8"
    )


async def invoke_mcp(tool_name: str, args: dict):
    """FastAPI -> real FastMCP client -> MCP tool."""
    async with Client(mcp) as client:
        result = await client.call_tool(tool_name, args)
    if result.is_error:
        raise HTTPException(status_code=502, detail=str(result.content)[:500])
    return result.data


@app.post("/save-user")
async def save_user_via_mcp(user: NewUser):
    """Save user from browser through FastMCP and the database API."""
    return await invoke_mcp("add_user", user.model_dump())


@app.post("/chat")
async def chat_via_mcp(message: ChatQuestion):
    """Send database questions to Ollama through an MCP tool."""
    question = message.question.strip()
    match = re.fullmatch(
        r"add user:\s*(.+?)\s*,\s*phone:\s*(.+?)\s*",
        question,
        flags=re.IGNORECASE,
    )
    if match:
        data = await invoke_mcp("add_user", {"name": match.group(1), "phone": match.group(2)})
        return {"answer": f"Saved user #{data['id']}: {data['name']}"}
    answer = await invoke_mcp("ask_database", {"question": question})
    return {"answer": answer}


@app.get("/health")
def health():
    return {"status": "ok", "database": DB_PATH.name}


@app.post("/records", status_code=201)
def create_record(user: NewUser):
    name, phone = user.name.strip(), user.phone.strip()
    if not name or not phone:
        raise HTTPException(status_code=422, detail="Name and phone must not be blank")

    # A unique user_key is created privately and stored in SQLite.
    with closing(db_connection()) as con:
        cursor = con.execute(
            "INSERT INTO users (name, phone, user_key) VALUES (?, ?, ?)",
            (name, phone, secrets.token_hex(16)),
        )
        con.commit()
        return {"id": cursor.lastrowid, "name": name, "phone": phone}


@app.get("/records")
def list_records(limit: int = Query(default=50, ge=1, le=100)):
    with closing(db_connection()) as con:
        rows = con.execute(
            "SELECT id, name, phone FROM users ORDER BY id LIMIT ?", (limit,)
        ).fetchall()
    return [dict(row) for row in rows]


@app.get("/summary")
def summary():
    with closing(db_connection()) as con:
        total = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    return {"total_users": total}


@app.get("/records/{user_id}")
def get_record(user_id: int):
    with closing(db_connection()) as con:
        row = con.execute(
            "SELECT id, name, phone FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(row)
