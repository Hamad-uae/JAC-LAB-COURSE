# Module 7 - Exercise 06: Makefile & ENV
# Streamlit chat + Ollama with an optional persona.

import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import streamlit as st

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434/api/chat")
MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b-instruct")
PERSONA_ENABLED = os.getenv("PERSONA_ENABLED", "false").strip().lower() in {
    "true", "1", "yes", "on"
}
PERSONA_PROMPT = os.getenv(
    "PERSONA_PROMPT",
    "You are a friendly Python teacher. Explain in simple Arabic with short examples."
)


def ask_ollama(chat_history):
    """Ask Ollama using conversation history and an optional system persona."""
    messages = []
    if PERSONA_ENABLED:
        messages.append({"role": "system", "content": PERSONA_PROMPT})
    messages.extend(chat_history)

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
    }
    req = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=180) as response:
        result = json.load(response)
    return result["message"]["content"]


st.set_page_config(page_title="Hamad AI - Makefile & ENV", page_icon="🤖")
st.title("🤖 Hamad AI - Makefile & ENV")
st.caption("Module 7 / Exercise 06 — Streamlit + Ollama + Docker")

with st.sidebar:
    st.subheader("App settings")
    st.write("Model:", MODEL)
    st.write("Persona:", "ON - Python teacher" if PERSONA_ENABLED else "OFF - Normal chat")
    st.info("Change PERSONA_ENABLED in .env, then recreate the container.")
    if st.button("Clear chat"):
        st.session_state.chat_history = []
        st.rerun()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

question = st.chat_input("Ask Hamad AI...")
if question and question.strip():
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Waiting for Ollama..."):
                answer = ask_ollama(st.session_state.chat_history)
            st.write(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
        except HTTPError as exc:
            st.error(f"Ollama HTTP error: {exc.code}")
        except (URLError, TimeoutError, OSError) as exc:
            st.error(f"Cannot connect to Ollama: {exc}")
        except (KeyError, ValueError) as exc:
            st.error(f"Invalid Ollama response: {exc}")
