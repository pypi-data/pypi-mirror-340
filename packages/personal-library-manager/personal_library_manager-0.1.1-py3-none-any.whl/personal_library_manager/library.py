import json

# Initialize the library as an empty list
library = []

def add_book(title, author, year, genre, read_status):
    """Add a new book to the library."""
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read_status": read_status
    }
    library.append(book)
    print(f"Book '{title}' added successfully!")

def remove_book(title):
    """Remove a book from the library by title."""
    global library
    library = [book for book in library if book["title"].lower() != title.lower()]
    print(f"Book '{title}' removed successfully!")

def search_book(query):
    """Search for books by title or author."""
    results = [book for book in library if query in book["title"].lower() or query in book["author"].lower()]
    return results

def display_books():
    """Display all books in the library."""
    if library:
        for i, book in enumerate(library, 1):
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")
    else:
        print("Your library is empty.")

def display_statistics():
    """Display statistics about the library."""
    total_books = len(library)
    read_books = sum(1 for book in library if book["read_status"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    print(f"Total books: {total_books}")
    print(f"Books read: {read_books} ({read_percentage:.2f}%)")

def save_library():
    """Save the library to a file."""
    with open("library.json", "w") as file:
        json.dump(library, file)
    print("Library saved successfully!")

def load_library():
    """Load the library from a file."""
    global library
    try:
        with open("library.json", "r") as file:
            library = json.load(file)
        print("Library loaded successfully!")
    except FileNotFoundError:
        print("No saved library found. Starting with an empty library.")
