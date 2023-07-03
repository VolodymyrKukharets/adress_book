from collections import UserDict
from datetime import datetime
import re
import csv


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.page_size = 1
        self.count = 0

    def add_record(self, record):
        # Add a record to the address book
        self.data[record.name.value] = record

    def save_to_file(self, filename="address_book.csv"):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Phone", "Birthday"])
            for record in self.data.values():
                phones = ', '.join([phone.value for phone in record.phones])
                birthday = record.birthday.value if len(record.birthday.__dict__) > 0 else ''
                writer.writerow([record.name.value, phones, birthday])

    def load_from_file(self, filename="address_book.csv"):
        self.data.clear()
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header row
            for row in reader:
                name = Name(row[0])
                phones = [Phone(phone.strip()) for phone in row[1].split(',') if phone.strip()]
                birthday = Birthday(row[2]) if row[2] else None
                record = Record(name, phones[0] if phones else None, birthday)
                for phone in phones[1:]:
                    record.add_phone(phone)
                self.add_record(record)

    def search(self, search_string):
        results = []
        for record in self.data.values():
            if search_string.lower() in record.name.value.lower():
                results.append(record)
            elif len(record.birthday.__dict__) > 0 and search_string in record.birthday.value:
                results.append(record)
            else:
                for phone in record.phones:
                    if len(phone.__dict__) > 0 and search_string in phone.value:
                        results.append(record)
                        break


        if results:
            for result in results:
                print(f"Name: {result.name.value}")
                print("Phones:")
                for phone in result.phones:
                    if len(phone.__dict__) > 0:
                        print(f"- {phone.value}")

                if len(result.birthday.__dict__) > 0:
                    print(f"Birthday: {result.birthday.value}")
                else:
                    print(f"Birthday: None")


                print()
        else:
            print("No results found.")

    def __next__(self):
        # Iterate over the address book
        items = list(self.data.items())
        if self.count >= len(items):
            raise StopIteration()
        users = []
        for i in range(self.count, min(self.count + self.page_size, len(items))):
            key, val = items[i]
            user_name = val.name.value
            user_numbers = []

            for phone in val.phones:
                try:
                    user_numbers.append(phone.value)
                except:
                    pass
            try:
                user_birthday = val.birthday.value if val.birthday else "None"
            except:
                user_birthday = "None"
            users.append(f"|{user_name:^40}|{', '.join(user_numbers):^40}|{user_birthday:^40}|")

        self.count += self.page_size

        for user in users:
            print(user)

        return users

    def __iter__(self):
        return self


class Record:
    def __init__(self, name, phone=None, birthday=None):
        # Represents a record in the address book
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone is not None:
            self.phones.append(phone)

    def add_phone(self, phone):
        # Add a phone number to the record
        self.phones.append(phone)

    def delete_phone(self, phone):
        # Delete a phone number from the record
        for index, user_phone in enumerate(self.phones):
            if user_phone.value == phone.value:
                self.phones.pop(index)

    def edit_phone(self, old_phone, new_phone):
        # Edit a phone number in the record
        for index, user_phone in enumerate(self.phones):
            if user_phone.value == old_phone.value:
                self.phones[index] = new_phone

    def days_to_birthday(self):
        # Calculate the number of days until the next birthday
        today = datetime.now()
        birthday_in_this_year = datetime(year=today.year, month=self.birthday.value[1], day=self.birthday.value[0])
        if birthday_in_this_year < today:
            birthday_in_this_year = datetime(year=today.year + 1, month=int(self.birthday.value[1]),
                                             day=int(self.birthday.value[0]))
            return (birthday_in_this_year - today).days
        else:
            return (birthday_in_this_year - today).days


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if self.validate_phone_number(value):
            super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.validate_phone_number(new_value):
            self._value = new_value

    @staticmethod
    def validate_phone_number(phone_num):
        pattern = r"^(?:\+?380|0)\d{9}$"
        if re.match(pattern, phone_num):
            return True
        else:
            print(f"Incorrect phone number {phone_num}. Please try again.")
            return False


class Birthday(Field):
    def __init__(self, value):
        # Represents a birthday field in a record
        if self.validate_data(value):
            super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.validate_data(new_value):
            self._value = new_value

    @staticmethod
    def validate_data(birthday):
        # Validate the format of a birthday date
        data_list = birthday.split("/")
        if len(data_list) == 3:
            day, month, year = map(int, data_list)
            if 1 <= day <= 31 and 1 <= month <= 12:
                return True
        else:
            print("Invalid data format. Must be in the format '31/12/1991'")
            return False