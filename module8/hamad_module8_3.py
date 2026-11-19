# Module 8 - Exercise 03: MCP with Ollama
# Receive a user question in MCP Inspector, send it to local Ollama,
# and return the AI answer to MCP Inspector.

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastmcp import FastMCP


MCP_SERVER = FastMCP("Hamad MCP Ollama")
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_MODEL = "qwen3:4b-instruct"


@MCP_SERVER.tool()
def ask_ollama(question: str) -> str:
    """Send a user's question to the local Ollama model and return its answer."""
    question = question.strip()
    if not question:
        return "Please enter a question."

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": question}],
        "stream": False,
    }

    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=180) as response:
            result = json.load(response)
        return result["message"]["content"]
    except HTTPError as exc:
        return f"Ollama returned HTTP error {exc.code}. Check the model name."
    except (URLError, TimeoutError, OSError):
        return "Cannot connect to Ollama. Check that Ollama is running on this computer."
    except (KeyError, ValueError):
        return "Ollama returned an unexpected response."


if __name__ == "__main__":
    MCP_SERVER.run()  # STDIO transport; MCP Inspector starts this script.
