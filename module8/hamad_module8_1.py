
# Module 8 - Exercise 01: MCP
# Show system date and generate a random number.
# Framework: FastMCP

from datetime import datetime
import secrets

from fastmcp import FastMCP


# Step 1: Create an MCP server
mcp = FastMCP("Hamad MCP Server")


# Step 2: Tool to display system date and time
@mcp.tool
def get_system_date() -> str:
    """Return the current system date and time."""

    now = datetime.now().astimezone()

    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


# Step 3: Tool to generate a random number
@mcp.tool
def generate_random_number() -> int:
    """Generate a random integer between 1 and 100."""

    return secrets.randbelow(100) + 1


# Step 4: Start MCP server
if __name__ == "__main__":
    mcp.run()
