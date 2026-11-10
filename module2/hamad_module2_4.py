
# Module 2 - Exercise 04
# Just One String or Number

# Import JSON to save data into a JSON file.
import json


# Create a class to store person information.
class Person:
    def __init__(self, name, number, location, job_title):
        self.name = name
        self.number = number
        self.location = location
        self.job_title = job_title

    # Convert person information into a dictionary.
    def to_dict(self):
        return {
            "name": self.name,
            "number": self.number,
            "location": self.location,
            "job_title": self.job_title
        }


# Create five fictional people.
people = [
    Person("Ali", 101, "Abu Dhabi", "Engineer"),
    Person("Sara", 102, "Dubai", "Teacher"),
    Person("Omar", 103, "Sharjah", "Doctor"),
    Person("Lina", 104, "Al Ain", "Designer"),
    Person("Noor", 105, "Ajman", "Developer")
]


# Function to save people into a JSON file.
def save_people(people):
    data = []

    # Convert each person into a dictionary.
    for person in people:
        data.append(person.to_dict())

    # Write the data into a JSON file.
    with open("people.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return "People saved successfully!"


# Run the function and display the result.
result = save_people(people)
print(result)
