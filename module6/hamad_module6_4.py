
# Module 6 - Exercise 04: AI Math Agent
# Use LangChain and Ollama to create a math agent.
# The agent chooses Python tools to solve calculations.

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# Tool 1: Addition
@tool
def add(a: float, b: float) -> str:
    """Add two numbers together."""
    result = a + b
    print(f"[ADD TOOL] {a} + {b} = {result}")
    return str(result)


# Tool 2: Subtraction
@tool
def subtract(a: float, b: float) -> str:
    """Subtract b from a."""
    result = a - b
    print(f"[SUBTRACT TOOL] {a} - {b} = {result}")
    return str(result)


# Tool 3: Multiplication
@tool
def multiply(a: float, b: float) -> str:
    """Multiply two numbers."""
    result = a * b
    print(f"[MULTIPLY TOOL] {a} * {b} = {result}")
    return str(result)


# Tool 4: Division
@tool
def divide(a: float, b: float) -> str:
    """Divide a by b."""
    if b == 0:
        return "Error: Division by zero is not allowed."

    result = a / b
    print(f"[DIVIDE TOOL] {a} / {b} = {result}")
    return str(result)


# Create the AI model
llm = ChatOllama(
    model="qwen3:4b-instruct",
    temperature=0
)


# Create the LangChain agent
agent = create_agent(
    model=llm,
    tools=[add, subtract, multiply, divide],
    system_prompt=(
        "You are Hamad Math AI Agent. "
        "Always use the provided math tools for calculations. "
        "Use tools step by step for complex expressions. "
        "Explain the final answer simply. "
        "Reply in the same language as the user."
    )
)


# Main program
def main():

    print("Welcome to Hamad Math AI Agent!")
    print("I can add, subtract, multiply and divide.")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a math question.")
            continue

        try:
            # Send the question to the agent
            response = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                },
                config={"recursion_limit": 12}
            )

            # Display the final answer
            answer = response["messages"][-1].content
            print("\nAI Agent:", answer)

        except Exception as error:
            print("Error:", error)
            print("Check Ollama, model and LangChain.")


if __name__ == "__main__":
    main()
