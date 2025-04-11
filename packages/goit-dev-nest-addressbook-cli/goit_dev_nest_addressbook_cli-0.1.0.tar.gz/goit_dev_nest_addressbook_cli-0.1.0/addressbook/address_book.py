from collections import UserDict
from datetime import datetime, timedelta, date
from .error_handler import PhoneValidationError, BirthdayValidationError, AddressValidationError
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise PhoneValidationError()
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise BirthdayValidationError()
        
class Email(Field):
    def __init__(self, value):
        if self.is_valid_email(value):
            super().__init__(value)
        else:
            raise ValueError("Invalid email address: {value}")   #Need to add this exeption to the error handler

    def is_valid_email(self, value):
        # Simple and general regex for emails
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(pattern, value) is not None
    
class Address(Field):
    def __init__(self, value):
        if len(value) > 120:
            raise AddressValidationError() 
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def add_email(self, email_str):
        self.emails.append(Email(email_str))

    def edit_email(self, old_email, new_email):
          "This method checks that if the old email is exist in the list and edit it "
          for e in self.emails:
                if e.value == old_email: 
                    e.value = Email(new_email).value
                    return
          raise ValueError("Email is not found") #Need to add this exeption to the error handler
    
    def remove_email(self, email):
        "This method checks if the email number exists in the list and deletes it"
        for e in self.emails:
              if e.value == email:
                  self.emails.remove(e)
                  return
        raise ValueError("Email is not found") #Need to add this exeption to the error handler
    
    def add_address(self, address_str):
        self.address = Address(address_str)

    def edit_address(self, new_address):
        if hasattr(self, "address"):
            self.address = Address(new_address)  # Replace with new validated address
        else:
            raise ValueError("No existing address to edit.")
        
    def remove_address(self):
        self.address = None
        
    
    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        bday = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        emails = '; '.join(e.value for e in self.emails)
        address = f"Address: {self.address}" if self.address else ""
        return f"Contact name: {self.name.value}, phones: {phones}, {emails},{address},{bday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming_birthdays = []
        
        for record in self.data.values():
            if record.birthday:
                name = record.name.value
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)
                    
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
                days_until_birthday = (birthday_this_year - today).days
                
                if 0 <= days_until_birthday <= days:
                    if birthday_this_year.weekday() >= 5:  
                        while birthday_this_year.weekday() >= 5:
                            birthday_this_year += timedelta(days=1)
                    
                    upcoming_birthdays.append({
                        "name": name,
                        "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                    })
        
        return upcoming_birthdays
