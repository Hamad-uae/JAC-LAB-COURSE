
# Module 6 - Exercise 05: Multi Agent
# Agent 1: Solve math problems using Python tools.
# Agent 2: Review and verify the first agent's answer.

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama


# Step 1: Create math tools

@tool
def add(a: float, b: float) -> str:
    """Add two numbers."""
    result = a + b
    print(f"[ADD TOOL] {a} + {b} = {result}")
    return str(result)


@tool
def subtract(a: float, b: float) -> str:
    """Subtract the second number from the first."""
    result = a - b
    print(f"[SUBTRACT TOOL] {a} - {b} = {result}")
    return str(result)


@tool
def multiply(a: float, b: float) -> str:
    """Multiply two numbers."""
    result = a * b
    print(f"[MULTIPLY TOOL] {a} * {b} = {result}")
    return str(result)


@tool
def divide(a: float, b: float) -> str:
    """Divide the first number by the second."""
    if b == 0:
        return "Error: Division by zero is not allowed."

    result = a / b
    print(f"[DIVIDE TOOL] {a} / {b} = {result}")
    return str(result)


# Step 2: Configure the local AI model
MODEL = "qwen3:4b-instruct"

llm = ChatOllama(
    model=MODEL,
    temperature=0
)

math_tools = [add, subtract, multiply, divide]


# Step 3: Create Agent 1 - Math Agent
math_agent = create_agent(
    model=llm,
    tools=math_tools,
    system_prompt=(
        "You are Math Agent. "
        "Solve the user's math problem. "
        "Always use the provided math tools for calculations. "
        "Use multiple tools for multi-step problems. "
        "Return the final numerical answer clearly."
    )
)


# Step 4: Create Agent 2 - Reviewer Agent
reviewer_agent = create_agent(
    model=llm,
    tools=math_tools,
    system_prompt=(
        "You are Reviewer Agent. "
        "Your job is to check the work of Math Agent. "
        "You will receive the original math question "
        "and the first agent's answer. "
        "Independently verify the calculation using math tools. "
        "State whether the answer is correct or incorrect. "
        "If incorrect, give the corrected answer. "
        "Explain your conclusion briefly."
    )
)


# Step 5: Ask an agent and return its final answer
def get_agent_answer(agent, message):

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": message}
            ]
        },
        config={"recursion_limit": 20}
    )

    return result["messages"][-1].content


# Step 6: Connect both agents
def run_multi_agent(question):

    print("\n" + "=" * 45)
    print("AGENT 1: MATH AGENT")
    print("=" * 45)

    # Agent 1 solves the problem
    math_answer = get_agent_answer(
        math_agent,
        question
    )

    print("\nMath Agent Answer:")
    print(math_answer)

    print("\n" + "=" * 45)
    print("AGENT 2: REVIEWER AGENT")
    print("=" * 45)

    # Pass the first agent's output to Agent 2
    review_request = (
        f"Original question:\n{question}\n\n"
        f"Math Agent's answer:\n{math_answer}\n\n"
        "Check this calculation independently."
    )

    review_answer = get_agent_answer(
        reviewer_agent,
        review_request
    )

    print("\nReviewer Agent Feedback:")
    print(review_answer)


# Step 7: Main program
def main():

    print("Welcome to Hamad Multi-Agent Math System!")
    print("Agent 1: Math Solver")
    print("Agent 2: Math Reviewer")
    print("Type 'exit' to quit.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a math problem.")
            continue

        try:
            run_multi_agent(question)

        except Exception as error:
            print("Error:", error)
            print("Check Ollama, LangChain and model settings.")


if __name__ == "__main__":
    main()
