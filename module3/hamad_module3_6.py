
# Module 3 - Exercise 06: Pagination
# Create a FastAPI endpoint to display items
# using page number and page size.

# Why pagination?
# Pagination divides large amounts of data
# into smaller pages.
# It reduces the amount of data transferred
# and makes results easier to browse.

from fastapi import FastAPI, Query


# Create the FastAPI application.
app = FastAPI()


# Create a sample list of 20 items.
items = []

for i in range(1, 21):
    items.append({
        "id": i,
        "name": f"Item {i}"
    })


# Create a GET endpoint for pagination.
@app.get("/items")
def get_items(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=5, ge=1, le=100)
):

    # Calculate the total number of items.
    total_items = len(items)

    # Calculate the number of pages.
    total_pages = (total_items + size - 1) // size

    # Calculate the starting position.
    start = (page - 1) * size

    # Calculate the ending position.
    end = start + size

    # Select only the items for this page.
    page_items = items[start:end]

    # Return the items and page metadata.
    return {
        "page": page,
        "size": size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "items": page_items
    }



# Why do we use pagination?
#
# Pagination helps us divide large datasets
# into smaller and manageable pages.
#
# Benefits:
# 1. Reduces the amount of data sent per request.
# 2. Improves response time for large datasets.
# 3. Makes it easier for users to browse items.
# 4. Allows users to request specific pages.

