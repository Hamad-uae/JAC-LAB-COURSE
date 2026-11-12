
# Module 3 - Exercise 05: Logging
# Log every HTTP request method, path and status.
# Display logs in the terminal and save them
# in a file named my_file.log.

import logging
import sys

from pathlib import Path
from fastapi import FastAPI, Request, Body


# Create the FastAPI application.
app = FastAPI()


# Save the log file next to this Python file.
LOG_FILE = Path(__file__).with_name("my_file.log")


# Create a logger for HTTP requests.
logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)

# Prevent duplicate messages from the root logger.
logger.propagate = False


# Configure the logging handlers.
if not logger.handlers:

    # Define the format of each log message.
    formatter = logging.Formatter(
        "%(asctime)s | %(message)s"
    )

    # Handler 1: Display logs in the terminal.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Handler 2: Save logs in my_file.log.
    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="a",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Add both handlers to the logger.
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


# Middleware runs for every HTTP request.
@app.middleware("http")
async def log_requests(request: Request, call_next):

    # Send the request to the correct API endpoint.
    try:
        response = await call_next(request)

    # Log unexpected server errors as status 500.
    except Exception:
        logger.error(
            "%s %s %s",
            request.method,
            request.url.path,
            500
        )
        raise

    # Log the request method, path and status code.
    logger.info(
        "%s %s %s",
        request.method,
        request.url.path,
        response.status_code
    )

    # Return the response to the client.
    return response


# API 1: Test a GET request.
@app.get("/ping")
def ping():
    return {
        "message": "Server is running"
    }


# API 2: Test a POST request.
@app.post("/echo")
def echo_message(
    message: str = Body(..., embed=True)
):
    return {
        "message": message
    }
