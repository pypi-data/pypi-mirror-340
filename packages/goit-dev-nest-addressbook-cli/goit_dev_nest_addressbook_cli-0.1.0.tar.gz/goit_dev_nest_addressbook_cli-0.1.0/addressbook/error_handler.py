class PhoneValidationError(ValueError):
    pass

class BirthdayValidationError(ValueError):
    pass

class AddressValidationError(Exception):
    """Custom exception for address validation errors."""
    pass

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."
        except PhoneValidationError:
            return "Phone must have exactly 10 digits."
        except BirthdayValidationError:
            return "Birthday must be in DD.MM.YYYY format."
        except AddressValidationError:
            return "Address is too long. It must be 120 characters or fewer."
        except ValueError:
            return "Give me name and phone please."
    return inner