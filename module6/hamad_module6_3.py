
# Module 6 - Exercise 03: LLM with DB
# Create a Streamlit chat application.
# Use Ollama to generate AI answers.
# Save questions and answers in SQLite as TEXT.
# Restore previous conversations when the app opens.

import json
import sqlite3
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import streamlit as st


# Configuration
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "hamad_module6_3.db"

API_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:0.5b"

SYSTEM_PROMPT = """
You are Hamad AI Assistant.
Answer questions clearly and accurately.
Use the same language as the user.
If you are unsure, say you do not know.
"""


# Step 1: Create the SQLite database
def create_database():
    connection = sqlite3.connect(DB_FILE)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()


# Step 2: Read saved chat messages
def load_messages():
    connection = sqlite3.connect(DB_FILE)

    try:
        cursor = connection.execute("""
            SELECT role, content
            FROM messages
            ORDER BY id ASC
        """)

        rows = cursor.fetchall()

        return [
            {"role": role, "content": content}
            for role, content in rows
        ]

    finally:
        connection.close()


# Step 3: Save the question and the answer
def save_chat(question, answer):
    connection = sqlite3.connect(DB_FILE)

    try:
        connection.executemany(
            """
            INSERT INTO messages (role, content)
            VALUES (?, ?)
            """,
            [
                ("user", question),
                ("assistant", answer)
            ]
        )

        connection.commit()

    finally:
        connection.close()


# Step 4: Get an AI answer from Ollama
def ask_ollama(question, history):

    # Include recent messages as conversation context
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ] + history[-16:] + [
        {
            "role": "user",
            "content": question
        }
    ]

    data = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    json_data = json.dumps(data).encode("utf-8")

    request = Request(
        API_URL,
        data=json_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request, timeout=180) as response:
        result = json.load(response)

    return result["message"]["content"]


# Step 5: Build the Streamlit interface
st.set_page_config(
    page_title="Hamad AI - LLM with DB",
    page_icon="🤖"
)

st.title("🤖 Hamad AI - LLM with DB")
st.caption("Streamlit + Ollama + SQLite Database")

# Initialize and load the database
create_database()
history = load_messages()

with st.sidebar:
    st.header("Database Information")
    st.write("AI Model:", MODEL)
    st.write("Database:", DB_FILE.name)
    st.write("Saved messages:", len(history))
    st.info("Questions and answers are stored in SQLite.")


# Step 6: Display previous conversations
for message in history:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Step 7: Receive a question from the user
question = st.chat_input("Ask Hamad AI...")

if question and question.strip():

    question = question.strip()

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        try:
            with st.spinner("AI is thinking..."):
                answer = ask_ollama(question, history)

                # Save only after a valid AI response
                save_chat(question, answer)

            st.write(answer)

            st.success("Chat saved to SQLite!")

        except HTTPError as error:
            st.error(f"Ollama API Error: {error.code}")

        except (URLError, TimeoutError):
            st.error("Cannot connect to Ollama.")

        except sqlite3.Error as error:
            st.error(f"Database Error: {error}")

        except (KeyError, ValueError) as error:
            st.error(f"Invalid AI response: {error}")
