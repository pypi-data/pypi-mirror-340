import pickle
from .error_handler import input_error
from .address_book import AddressBook

ADDRESSBOOK_FILE = "addressbook.pkl"

def save_data(book: AddressBook, filename=ADDRESSBOOK_FILE):
    """Serialize the address book to a binary file."""
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
            print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data(filename=ADDRESSBOOK_FILE) -> AddressBook:
    """Deserialize the address book from a binary file or return a new book if not found."""
    try:
        with open(filename, "rb") as f:
            book = pickle.load(f)
            print(f"Data loaded from {filename}.")
            return book
    except FileNotFoundError:
        print("No existing address book found. Creating a new one.")
        return AddressBook()
    except Exception as e:
        print(f"Error loading data: {e}")
        return AddressBook()

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args