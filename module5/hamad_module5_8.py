
# Module 5 - Exercise 08: Remember My Chat
# Save all chat messages in a local SQLite database.
# Restore previous conversations when the app reopens.

import json
import sqlite3
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import streamlit as st


# Ollama settings
API_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:0.5b"

# Save the database beside this Python file
DB_FILE = Path(__file__).with_name("hamad_module5_8.db")

SYSTEM_PROMPT = """
You are Hamad AI Assistant.
You are friendly and helpful.
Answer in the same language as the user.
Use previous messages to understand the conversation.
If you are unsure, say so.
"""


# Step 1: Create the database and table
def create_database():
    connection = sqlite3.connect(DB_FILE)

    try:
        cursor = connection.cursor()

        cursor.execute("""
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


# Step 2: Read all saved messages
def load_messages():
    connection = sqlite3.connect(DB_FILE)

    try:
        cursor = connection.cursor()

        cursor.execute("""
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


# Step 3: Save the user question and AI answer
def save_messages(question, answer):
    connection = sqlite3.connect(DB_FILE)

    try:
        cursor = connection.cursor()

        cursor.executemany(
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


# Step 4: Send chat history to Ollama
def ask_ollama(chat_history):

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + chat_history,
        "stream": False,
        "options": {
            "num_ctx": 8192,
            "temperature": 0.3
        }
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


# Step 5: Build the Streamlit UI
st.set_page_config(
    page_title="Hamad AI - Memory Chat",
    page_icon="🤖"
)

st.title("🤖 Hamad AI - Memory Chat")
st.caption("My AI assistant with permanent chat history")

# Initialize the database
create_database()

# Restore previous messages
messages = load_messages()

with st.sidebar:
    st.header("Memory Settings")
    st.write("Model:", MODEL)
    st.write("Saved messages:", len(messages))
    st.success("Chat history saved in SQLite")


# Show all saved messages
for message in messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Step 6: Receive a new question
question = st.chat_input("Ask Hamad AI...")

if question and question.strip():

    question = question.strip()

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        try:
            with st.spinner("Hamad AI is thinking..."):

                # Add new question to previous messages
                chat_history = messages + [
                    {
                        "role": "user",
                        "content": question
                    }
                ]

                # Get the AI answer
                answer = ask_ollama(chat_history)

            st.write(answer)

            # Save both messages permanently
            save_messages(question, answer)

        except HTTPError as error:
            st.error(f"Ollama API Error: {error.code}")

        except (URLError, TimeoutError):
            st.error(
                "Cannot connect to Ollama. "
                "Make sure Ollama is running."
            )

        except (sqlite3.Error, KeyError, ValueError) as error:
            st.error(f"Application Error: {error}")
