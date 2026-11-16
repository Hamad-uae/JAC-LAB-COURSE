
# Module 5 - Exercise 05: Too Many Words
# Increase the context window and change temperature.
#
# Context window controls how much text the LLM can consider.
# Temperature controls randomness in generated answers.
# Lower temperature = more focused answers.
# Higher temperature = more varied answers.

import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Ollama API settings
API_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "qwen2.5:0.5b"

# Model generation settings
CONTEXT_SIZE = 8192
TEMPERATURE = 0.9


def ask_ollama(question):

    # Prepare the request data
    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful Python teacher."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False,
        "options": {
            "num_ctx": CONTEXT_SIZE,
            "temperature": TEMPERATURE
        }
    }

    # Convert data to JSON bytes
    json_data = json.dumps(data).encode("utf-8")

    # Create POST request
    request = Request(
        API_URL,
        data=json_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    # Call the Ollama API
    with urlopen(request, timeout=180) as response:
        result = json.load(response)

    # Return the model answer
    return result["message"]["content"]


def main():

    print("Welcome to Hamad AI Assistant")
    print("Context Window:", CONTEXT_SIZE)
    print("Temperature:", TEMPERATURE)
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
            answer = ask_ollama(question)
            print("\nAI:", answer)

        except HTTPError as error:
            print("API Error:", error.code)
            print(error.read().decode("utf-8"))

        except (URLError, TimeoutError) as error:
            print("Connection Error:", error)
            print("Check that Ollama is running.")

        except (KeyError, ValueError) as error:
            print("Response Error:", error)


if __name__ == "__main__":
    main()
