
# Module 5 - Exercise 03: LLM API
# Send user input to the local Ollama API.
# Display the AI response in the terminal.

import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Ollama API address
API_URL = "http://127.0.0.1:11434/api/generate"

# The small model installed in Exercise 02
MODEL = "qwen2.5:0.5b"


def ask_ollama(user_message):

    # Prepare the data sent to Ollama
    data = {
        "model": MODEL,
        "prompt": user_message,
        "stream": False
    }

    # Convert Python data into JSON bytes
    json_data = json.dumps(data).encode("utf-8")

    # Create an HTTP POST request
    request = Request(
        API_URL,
        data=json_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    # Send the request and read the response
    with urlopen(request, timeout=180) as response:
        result = json.load(response)

    # Return the AI-generated answer
    return result.get("response", "No answer received.")


def main():

    print("Welcome to Hamad AI Assistant!")
    print("Type 'exit' to stop the program.")

    while True:

        # Get text from the user
        user_message = input("\nYou: ").strip()

        # Exit the program
        if user_message.lower() == "exit":
            print("Goodbye!")
            break

        # Prevent empty questions
        if not user_message:
            print("Please enter a question.")
            continue

        try:
            # Call the Ollama API
            answer = ask_ollama(user_message)

            # Display the AI response
            print("\nAI:", answer)

        except HTTPError as error:
            print("API Error:", error.code)
            print("Check that the model is installed.")
            print(error.read().decode("utf-8"))

        except (URLError, TimeoutError) as error:
            print("Connection Error:", error)
            print("Make sure Ollama is running.")


if __name__ == "__main__":
    main()
