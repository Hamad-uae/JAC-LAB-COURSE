
# Exercise 08 - What It Hides

def count_address_words():
    try:
        with open("address.txt", "r", encoding="utf-8") as file:
            content = file.read()

    except FileNotFoundError:
        print("Address file not found")
        return []

    counts = []

    for line in content.splitlines():
        if line.startswith("Address:"):
            address = line.split(":", 1)[1].strip()
            word_count = len(address.split())
            counts.append(word_count)

    if not counts:
        print("No addresses found")
        return []

    with open("address.txt", "a", encoding="utf-8") as file:
        for i, count in enumerate(counts, start=1):
            label = f"Address {i} Word Count:"
            if label not in content:
                file.write(f"\n{label} {count}")

    return counts


# Run the function
result = count_address_words()
print("Word counts:", result)

