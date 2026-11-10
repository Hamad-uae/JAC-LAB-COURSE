
# Module 2 - Exercise 02
# My encryption method: Shift and Reverse

def encrypt_text(text):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""

    for letter in text:
        lower_letter = letter.lower()

        if lower_letter in alphabet:
            index = alphabet.index(lower_letter)
            new_index = (index + 2) % 26
            print(new_index)
            new_letter = alphabet[new_index]

            if letter.isupper():
                new_letter = new_letter.upper()

            result += new_letter
        else:
            result += letter

    return result[::-1]


# Test the encryption
message = "Hamad"
encrypted = encrypt_text(message)

print("Original:", message)
print("Encrypted:", encrypted)
