
# Exercise 07 - Mistakes

def show_string(value):
    try:
        if not isinstance(value, str):
            raise TypeError("Only strings are allowed")

        print(value)
        return value

    except TypeError:
        return None


# Test 1 - String
show_string("Hello Hamad")

# Test 2 - Integer
result = show_string(123)
print(result)
