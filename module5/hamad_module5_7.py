
# Module 5 - Exercise 07: Full Chat
# Create a chatbot that remembers previous messages
# during the same Streamlit session.

import json
import streamlit as st
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Ollama API settings
API_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:0.5b"

# Define the AI personality
SYSTEM_PROMPT = """
You are Hamad AI Assistant.
You are friendly and helpful.
Answer in the same language as the user.
Use previous messages to understand follow-up questions.
Remember details provided earlier in this conversation.
If you do not know something, say so.
"""

# Configure the Streamlit page
st.set_page_config(
    page_title="Hamad AI - Full Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Hamad AI - Full Chat")
st.caption("A chatbot with conversation history")


# Initialize the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Function to call Ollama API
def ask_ollama(chat_history):

    # Include system instructions and chat history
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

    # Convert data to JSON
    json_data = json.dumps(data).encode("utf-8")

    # Prepare the HTTP request
    request = Request(
        API_URL,
        data=json_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    # Send the request to Ollama
    with urlopen(request, timeout=180) as response:
        result = json.load(response)

    # Extract the AI answer
    return result["message"]["content"]


# Sidebar settings
with st.sidebar:

    st.header("Chat Settings")
    st.write("Model:", MODEL)

    st.write(
        "Saved messages:",
        len(st.session_state.messages)
    )

    # Clear conversation history
    if st.button("New Chat"):
        st.session_state.messages = []
        st.rerun()


# Display all previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get a new question
question = st.chat_input("Write your message...")

if question and question.strip():

    # Save and display the new user message
    user_message = {
        "role": "user",
        "content": question.strip()
    }

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.write(question)

    # Ask the LLM using the full chat history
    with st.chat_message("assistant"):

        try:
            with st.spinner("Hamad AI is thinking..."):
                answer = ask_ollama(
                    st.session_state.messages
                )

            # Display the AI response
            st.write(answer)

            # Save the AI response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except HTTPError as error:
            st.error(f"API Error: {error.code}")
            st.session_state.messages.pop()

        except (URLError, TimeoutError):
            st.error("Ollama is not connected.")
            st.session_state.messages.pop()

        except (KeyError, ValueError):
            st.error("Invalid response from Ollama.")
            st.session_state.messages.pop()
