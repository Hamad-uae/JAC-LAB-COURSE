
# Exercise 06 - Where You Live

# Class to store person information
class Person:
    def __init__(self, name, contact, address, phone):
        self.name = name
        self.contact = contact
        self.address = address
        self.phone = phone

# Function to collect and save information
def save_person():
    name = input("Enter your name: ")
    contact = input("Enter your contact: ")
    address = input("Enter your address: ")
    phone = input("Enter your phone number: ")

    person = Person(name, contact, address, phone)

    # Save information in a text file
    with open("address.txt", "w", encoding="utf-8") as file:
        file.write("Name: " + person.name + "\n")
        file.write("Contact: " + person.contact + "\n")
        file.write("Address: " + person.address + "\n")
        file.write("Phone: " + person.phone + "\n")

    return "Information saved successfully!"

# Run the function
print(save_person())
