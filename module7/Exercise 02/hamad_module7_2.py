
# Module 7 - Exercise 02: Docker Compose
# Streamlit application connecting to Ollama.

import os
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import streamlit as st


# Ollama configuration
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/chat"
)

MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b-instruct")


# Get answer from Ollama
def ask_ollama(messages):

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }

    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urlopen(request, timeout=180) as response:
        result = json.load(response)

    return result["message"]["content"]


# Streamlit interface
st.set_page_config(page_title="Hamad Docker AI")

st.title("Hamad AI - Docker Compose")
st.caption("Python + Streamlit + Docker + Ollama")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


question = st.chat_input("Ask Hamad AI...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("AI is thinking..."):
                answer = ask_ollama(
                    st.session_state.messages
                )

            st.write(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except HTTPError as error:
            st.error(f"Ollama API error: {error.code}")

        except (URLError, TimeoutError, OSError):
            st.error("Cannot connect to Ollama.")

        except (KeyError, ValueError) as error:
            st.error(f"Response error: {error}")
