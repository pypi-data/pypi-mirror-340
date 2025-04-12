from colorama import Fore, Style

class PhoneValidationError(ValueError):
    """Custom exception for phone validation errors."""
    pass

class BirthdayValidationError(ValueError):
    """Custom exception for birthday validation errors."""
    pass

class AddressValidationError(Exception):
    """Custom exception for address validation errors."""
    pass

class EmailValidationError(Exception):
    """Custom exception for email validation errors."""
    pass

class EmailIsNotFound(Exception):
    """Custom exception for email validation errors."""
    pass

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return Fore.RED + "Contact not found." + Style.RESET_ALL
        except IndexError:
            return Fore.YELLOW + "Enter user name." + Style.RESET_ALL
        except PhoneValidationError:
            return Fore.YELLOW + "Phone must have exactly 10 digits." + Style.RESET_ALL
        except BirthdayValidationError:
            return Fore.YELLOW + "Birthday must be in DD.MM.YYYY format." + Style.RESET_ALL
        except AddressValidationError:
            return Fore.YELLOW + "Address is too long. It must be 120 characters or fewer." + Style.RESET_ALL
        except EmailValidationError:
            return Fore.YELLOW + "Please enter Name and email" + Style.RESET_ALL
        except EmailIsNotFound:
            return Fore.RED + "Email is not found" + Style.RESET_ALL
        except ValueError:
            return Fore.YELLOW + "Give me name and phone please." + Style.RESET_ALL
    return inner