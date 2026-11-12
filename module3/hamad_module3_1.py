
# Module 3 - Exercise 01: Hello API
# Create an API to greet a person by name.

from fastapi import FastAPI

# Create the FastAPI application.
app = FastAPI()


# Create a GET endpoint for /hello.
@app.get("/hello")
def say_hello(name: str):

    # Return a greeting with the person's name.
    return {"message": f"Hello {name}"}
