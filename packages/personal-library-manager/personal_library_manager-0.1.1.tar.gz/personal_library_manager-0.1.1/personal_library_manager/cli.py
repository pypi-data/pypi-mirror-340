import os
from personal_library_manager.library import add_book, remove_book, search_book, display_books, display_statistics, save_library, load_library

def main_menu():
    """Display the main menu and handle user input."""
    load_library()
    while True:
        print("\nWelcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Enter the book title: ")
            author = input("Enter the author: ")
            year = int(input("Enter the publication year: "))
            genre = input("Enter the genre: ")
            read_status = input("Have you read this book? (yes/no): ").strip().lower() == 'yes'
            add_book(title, author, year, genre, read_status)
        elif choice == "2":
            title = input("Enter the title of the book to remove: ")
            remove_book(title)
        elif choice == "3":
            query = input("Search by (1) Title or (2) Author: ").strip()
            search_query = input("Enter your search query: ").lower()
            results = search_book(search_query)
            if results:
                print("Matching Books:")
                for book in results:
                    print(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read_status'] else 'Unread'}")
            else:
                print("No books found.")
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            save_library()
            print("Library saved to file. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
