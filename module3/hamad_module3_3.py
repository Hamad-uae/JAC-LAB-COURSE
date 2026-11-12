
# Module 3 - Exercise 03: Type Correctly

from fastapi import FastAPI, Body

# Create the FastAPI app.
app = FastAPI()


# Validate the required Text field.
@app.post("/validate")
def validate_text(
    text: str = Body(..., embed=True, alias="Text")
):
    return {
        "message": "Text received successfully",
        "Text": text
    }
