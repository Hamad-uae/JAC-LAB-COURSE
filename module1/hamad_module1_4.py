
# Module 1 - Exercise 04
# Fibonacci for Today

from datetime import datetime


# Function to get the current date and time
def get_current_datetime():
    now = datetime.now()

    # Format: seconds:minutes:hours, day/month/year
    return now.strftime("%S:%M:%H , %d/%m/%Y")


# Function to calculate Fibonacci numbers
def fibonacci_for_today():

    # Get the current minute
    current_minute = datetime.now().minute

    # Calculate the number of Fibonacci terms
    number_of_terms = 2 * current_minute

    # Create an empty list
    sequence = []

    # First two Fibonacci numbers
    first = 0
    second = 1

    # Generate the Fibonacci sequence
    for i in range(number_of_terms):

        # Add the current number to the list
        sequence.append(first)

        # Calculate the next number
        next_number = first + second

        # Update the first and second numbers
        first = second
        second = next_number

    # Return the minute and the sequence
    return current_minute, sequence


# Main function
def main():

    # Display the current date and time
    print("Current Date and Time:")
    print(get_current_datetime())

    # Get the current minute and Fibonacci sequence
    current_minute, sequence = fibonacci_for_today()

    # Display the results
    print("Current Minute:", current_minute)
    print("Number of Terms:", len(sequence))
    print("Fibonacci Sequence:")
    print(sequence)


# Run the main function
if __name__ == "__main__":
    main()
