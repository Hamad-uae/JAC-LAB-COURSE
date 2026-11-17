
# Module 6 - Exercise 06
# Pydantic and Structured Data
# Streamlit + Ollama + Pydantic + SQLite

import json
import sqlite3
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import re
import streamlit as st
from pydantic import BaseModel, Field, ValidationError, field_validator


# Configuration
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "hamad_module6_6.db"

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen3:4b-instruct"


# Step 1: Define the Pydantic structure
class UserInfo(BaseModel):

    # Required field
    name: str = Field(
        description="Name provided by the user. Empty if missing."
    )

    # Optional fields
    time: str | None = None
    number: float | None = None

    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        if not value.strip():
            raise ValueError("Name is required.")
        return value.strip()


# Step 2: Create SQLite database
def create_database():

    with sqlite3.connect(DB_FILE) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS user_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                name TEXT NOT NULL,
                time TEXT,
                number REAL,
                result_json TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


# Step 3: Save validated data
def save_record(question, record):

    with sqlite3.connect(DB_FILE) as connection:
        connection.execute(
            """
            INSERT INTO user_records
            (question, name, time, number, result_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                question,
                record.name,
                record.time,
                record.number,
                record.model_dump_json()
            )
        )


# Step 4: Load previous records
def load_records():

    with sqlite3.connect(DB_FILE) as connection:
        return connection.execute("""
            SELECT question, result_json
            FROM user_records
            ORDER BY id ASC
        """).fetchall()


# Step 5: Ask Ollama to extract structured data
def extract_information(question):

    system_prompt = """
    Extract information from the user's message.

    Return JSON with these fields:
    name, time, number.

    Rules:
    - Never invent missing information.
    - If name is missing, use an empty string.
    - If time is missing, use null.
    - If number is missing, use null.
    - Number must be numeric.
    - Return JSON only.
    - Extract the number when the user says "my number is".
    - Example: "my number is 25" means number = 25.
    - Do not confuse the time 09:30 with the number 25.
    python -m streamlit run hamad_module6_6.py- Use null for number only if no number is provided.
    """

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "format": UserInfo.model_json_schema(),
        "stream": False,
        "options": {"temperature": 0}
    }

    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request, timeout=180) as response:
        result = json.load(response)

    # Validate the AI-generated JSON using Pydantic
    content = result["message"]["content"]

    
    # Validate the AI response with Pydantic
    record = UserInfo.model_validate_json(content)

    # Extract an explicitly provided number
    match = re.search(
        r"\bmy\s+number\s+is\s+(-?\d+(?:\.\d+)?)\b",
        question,
        flags=re.IGNORECASE
    )

    if match:
        number = float(match.group(1))

        # Validate the corrected data again
        record = UserInfo.model_validate({
            **record.model_dump(),
            "number": number
        })

    return record



# Step 6: Create Streamlit interface
st.set_page_config(
    page_title="Hamad AI - Pydantic",
    page_icon="🤖"
)

st.title("🤖 Hamad AI - Structured Data")
st.caption("Streamlit + Ollama + Pydantic + SQLite")

create_database()
records = load_records()

with st.sidebar:
    st.header("Database Information")
    st.write("Model:", MODEL)
    st.write("Saved records:", len(records))
    st.write("Required field: name")
    st.write("Optional fields: time, number")


# Display saved records
for saved_question, saved_json in records:

    with st.chat_message("user"):
        st.write(saved_question)

    with st.chat_message("assistant"):
        st.json(json.loads(saved_json))


# Step 7: Receive a new message
question = st.chat_input(
    "Enter your name, time and number..."
)

if question and question.strip():

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        try:
            with st.spinner("AI is extracting information..."):
                record = extract_information(question)

            # Save validated result into SQLite
            save_record(question, record)

            st.json(record.model_dump())
            st.success("Validated and saved to SQLite!")

        except ValidationError:
            st.error(
                "Validation failed. Please provide a name "
                "and valid values for the other fields."
            )

        except HTTPError as error:
            st.error(f"Ollama API error: {error.code}")

        except (URLError, TimeoutError):
            st.error("Cannot connect to Ollama.")

        except (KeyError, ValueError, sqlite3.Error) as error:
            st.error(f"Error: {error}")
