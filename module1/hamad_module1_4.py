
# Exercise 04 - Date and Time

from datetime import datetime

def show_current_time():
    now = datetime.now()
    formatted_time = now.strftime("%S:%M:%H, %d/%m/%Y")
    return formatted_time

# Test the function
print(show_current_time())
