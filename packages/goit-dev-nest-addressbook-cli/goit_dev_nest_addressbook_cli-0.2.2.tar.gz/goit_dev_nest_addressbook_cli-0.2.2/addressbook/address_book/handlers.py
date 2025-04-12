from addressbook.error_handler import input_error, EmailValidationError, EmailIsNotFound
from addressbook.address_book.address_book import Record, AddressBook, Email
from colorama import init, Fore, Back, Style

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = Fore.GREEN + "Contact updated." + Style.RESET_ALL
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = Fore.GREEN + "Contact added." + Style.RESET_ALL
    if phone:
        record.add_phone(phone)
    return message

@input_error
def edit_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return Fore.RED + "Contact not found." + Style.RESET_ALL
    if not record.edit_phone(old_phone, new_phone):
        return Fore.YELLOW + f"Phone number {old_phone} not found for contact {name}." + Style.RESET_ALL
    return Fore.GREEN + f"Phone number updated for contact {name}." + Style.RESET_ALL

@input_error
def get_contact(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return f"{name}: {', '.join(p.value for p in record.phones)}"

@input_error
def add_birthday(args, book):
    name, bday_str, *_ = args
    record = book.find(name)
    if record is None:
        return Fore.RED + "Contact not found." + Style.RESET_ALL
    record.add_birthday(bday_str)
    return Fore.GREEN + "Birthday added." + Style.RESET_ALL

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return Fore.RED + "Contact not found." + Style.RESET_ALL
    if record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return Fore.RED + "Birthday not set."  + Style.RESET_ALL

@input_error
def birthdays(args, book):
    try:
        days = int(args[0]) if args else 7
    except ValueError:
        return Fore.YELLOW + "Please enter a valid number of days."  + Style.RESET_ALL

    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return Fore.YELLOW + f"No birthdays in the upcoming {days} days."  + Style.RESET_ALL
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )

@input_error
def add_email(args, book: AddressBook):
    if len(args) < 2:
        raise EmailValidationError
    name, email_str, *_ = args
    record = book.find(name)
    if record is None:
        return Fore.RED + "Contact not found."  + Style.RESET_ALL
    record.add_email(email_str)
    return Fore.GREEN + f"Email added to contact {name}." + Style.RESET_ALL

@input_error
def edit_email(args, book: AddressBook):
    if len(args) < 3:
        return Fore.YELLOW + "Error: Provide both a name and an email." + Style.RESET_ALL
    name, old_email, new_email, *_ = args
    record = book.find(name)

    if record is None:
        return Fore.RED + f"Contact '{name}' not found." + Style.RESET_ALL

    record.edit_email(old_email, new_email)
    return Fore.GREEN + f"Email updated for contact '{name}'." + Style.RESET_ALL

@input_error 
def remove_email(args, book: AddressBook):
    if len(args) < 1:
        return Fore.YELLOW + "Error: Provide a name and email witch need to be deleted." + Style.RESET_ALL
    name, email, *_ = args
    record = book.find(name)

    if record is None:
        return Fore.RED + f"Contact '{name}' not found." + Style.RESET_ALL

    try:
        record.remove_email(email)
        return Fore.GREEN + f"Email '{email}' removed from contact '{name}'." + Style.RESET_ALL
    except EmailIsNotFound:
        return Fore.RED + "Email is not found" + Style.RESET_ALL

@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        raise EmailValidationError
    name, *address_parts = args
    address = ' '.join(address_parts)
    record = book.find(name)
    if record is None:
        return Fore.RED + "Contact not found." + Style.RESET_ALL
    record.add_address(address)
    return Fore.GREEN + f"Address added to contact {name}." + Style.RESET_ALL

@input_error
def edit_address(args, book: AddressBook):
    if len(args) < 2:
        return Fore.YELLOW + "Error: Provide both a name and an address." + Style.RESET_ALL
    name, *address_parts = args
    address = ' '.join(address_parts)
    record = book.find(name)
    if record is None:
        return Fore.RED + f"Contact '{name}' not found." + Style.RESET_ALL

    record.edit_address(address)
    return Fore.GREEN + f"Address updated for contact '{name}'." + Style.RESET_ALL

@input_error 
def remove_address(args, book: AddressBook):
    if len(args) < 1:
        return Fore.YELLOW + "Error: Provide a name and address witch need to be deleted." + Style.RESET_ALL
    name, *_ = args
    record = book.find(name)

    if record is None:
        return Fore.RED + f"Contact '{name}' not found." + Style.RESET_ALL

    try:
        record.remove_address()
        return Fore.GREEN + f"Address '{address}' removed from contact '{name}'." + Style.RESET_ALL
    except EmailIsNotFound:
        return Fore.RED + "Address is not found" + Style.RESET_ALL


@input_error
def show_all(args, book):
    """Displays all contacts with their phone numbers."""
    if not book.data:
        return Fore.YELLOW + "The address book is empty." + Style.RESET_ALL
    return "\n".join(str(record) for record in book.data.values())