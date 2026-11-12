
# Module 3 - Exercise 04: Back and Forth
# Create a POST API to save a person's information.
# Create a GET API to read the saved information
# and display it with a random number.

# Import FastAPI tools.
from fastapi import FastAPI, Body, HTTPException

# Import random to generate a random number.
import random


# Create the FastAPI application.
app = FastAPI()


# Create an empty dictionary to store the person.
saved_person = {}


# API 1: Save a person's name and phone number.
@app.post("/person")
def save_person(
    name: str = Body(...),
    phone_number: str = Body(...)
):

    # Store the person's information.
    saved_person["name"] = name
    saved_person["phone_number"] = phone_number

    # Return a success message.
    return {
        "message": "Person saved successfully",
        "person": saved_person.copy()
    }


# API 2: Read the person and add a random number.
@app.get("/person")
def get_person():

    # Check if a person has been saved.
    if not saved_person:
        raise HTTPException(
            status_code=404,
            detail="No person saved yet"
        )

    # Generate a random number between 1000 and 9999.
    random_number = random.randint(1000, 9999)

    # Return the saved person with the random number.
    return {
        "name": saved_person["name"],
        "phone_number": saved_person["phone_number"],
        "random_number": random_number
    }
