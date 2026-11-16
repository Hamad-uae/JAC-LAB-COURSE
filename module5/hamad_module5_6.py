
# Module 5 - Exercise 06: Chat
# Build a web chat interface using Streamlit.
# Connect the interface to a local Ollama LLM.

import json
import streamlit as st
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Ollama settings
API_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:0.5b"

SYSTEM_PROMPT = """
You are Hamad AI Assistant.
You are friendly and helpful.
Answer user questions clearly.
Reply in the same language as the user.
"""

# Configure the web page
st.set_page_config(
    page_title="Hamad AI Chat",
    page_icon="🤖"
)

# Display the page title
st.title("🤖 Hamad AI Chat")
st.caption("My first AI chatbot using Streamlit and Ollama")

# Create chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Function to call the Ollama API
def ask_ollama(messages):

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + messages,
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


# Add a sidebar
with st.sidebar:
    st.header("Chat Settings")
    st.write("Model:", MODEL)

    # Button to clear chat history
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Get a new question from the user
question = st.chat_input("Ask me anything...")

if question:

    # Save the user's message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Show the user's message
    with st.chat_message("user"):
        st.write(question)

    # Generate and display the AI response
    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:
                answer = ask_ollama(
                    st.session_state.messages
                )

            except HTTPError as error:
                st.error(
                    f"Ollama API error: {error.code}"
                )
                answer = None

            except (URLError, TimeoutError):
                st.error(
                    "Cannot connect to Ollama. "
                    "Make sure Ollama is running."
                )
                answer = None

            except (KeyError, ValueError):
                st.error("Invalid response from Ollama.")
                answer = None

        if answer is not None:

            # Display AI answer
            st.write(answer)

            # Save the answer in chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
