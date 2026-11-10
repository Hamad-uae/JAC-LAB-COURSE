
# Exercise 05 - Speaking is Expensive

def speaking_price(text, price_per_letter):
    shifted = ""
    letter_count = 0

    for letter in text:
        if "a" <= letter <= "z":
            if letter == "z":
                shifted += "a"
            else:
                shifted += chr(ord(letter) + 1)
            letter_count += 1

        elif "A" <= letter <= "Z":
            if letter == "Z":
                shifted += "A"
            else:
                shifted += chr(ord(letter) + 1)
            letter_count += 1

        else:
            shifted += letter

    word_count = len(text.split())
    total_price = letter_count * price_per_letter

    return {
        "shifted_string": shifted,
        "word_count": word_count,
        "price_of_string": total_price
    }

# Test
result = speaking_price("dog cat!", 3)
print(result)
