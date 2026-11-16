
# Module 5 - Exercise 04: Guidance
# Give the LLM a persona using a System Prompt.
# Receive questions from the user.

import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Ollama configuration
API_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:0.5b"

# System Prompt: Define the AI personality
SYSTEM_PROMPT = """
You are a friendly and patient Python teacher.
Your name is Hamad AI Teacher.

Explain programming concepts step by step.
Use short Python code examples when helpful.
Be encouraging, clear, and concise.
If you are unsure, say you are unsure.
"""


def ask_ai(question):

    # Prepare system and user messages
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False
    }

    # Convert data to JSON
    json_data = json.dumps(data).encode("utf-8")

    # Create POST request
    request = Request(
        API_URL,
        data=json_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    # Send question to Ollama
    with urlopen(request, timeout=180) as response:
        result = json.load(response)

    # Get the AI answer
    return result["message"]["content"]


def main():

    print("Welcome to Hamad AI Teacher!")
    print("Type 'exit' to quit.")

    while True:

        # Get question from user
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            answer = ask_ai(question)
            print("\nHamad AI:", answer)

        except HTTPError as error:
            print("API Error:", error.code)
            print("Check your model name.")

        except (URLError, TimeoutError) as error:
            print("Connection Error:", error)
            print("Make sure Ollama is running.")

        except (KeyError, ValueError) as error:
            print("Invalid API response:", error)


if __name__ == "__main__":
    main()
