
# Module 2 - Exercise 01
# Check if a number is even or odd

def check_number(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

# Test the function
print(check_number(8))
print(check_number(7))
print(check_number(10))
