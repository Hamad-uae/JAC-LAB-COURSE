
# Module 3 - Exercise 02: Echo Server
# Create a POST API that receives a message
# and returns it with the server timestamp.

# Import FastAPI and Body.
from fastapi import FastAPI, Body

# Import datetime to get the server time.
from datetime import datetime


# Create the FastAPI application.
app = FastAPI()


# Create a POST endpoint called /echo.
@app.post("/echo")
def echo_message(message: str = Body(..., embed=True)):

    # Get the current date and time of the server.
    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    # Return the same message and server timestamp.
    return {
        "message": message,
        "timestamp": timestamp
    }
