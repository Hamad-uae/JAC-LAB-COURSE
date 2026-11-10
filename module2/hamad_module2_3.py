
# Module 2 - Exercise 03: Unique
# Remove duplicate numbers from a list.

def unique_numbers(numbers):
    # Create an empty list for unique numbers.
    unique_list = []

    # Check each number in the original list.
    for number in numbers:

        # Add the number only if it is not already in the list.
        if number not in unique_list:
            unique_list.append(number)

    # Return the list without duplicates.
    return unique_list


# Test the function
numbers = [1, 2, 2, 3, 4, 4, 5]

result = unique_numbers(numbers)

print("Original list:", numbers)
print("Unique list:", result)
