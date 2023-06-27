from collections import UserDict
from datetime import datetime
import re


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.page_size = 1
        self.count = 0

    def add_record(self, record):
        # Add a record to the address book
        self.data[record.name.value] = record

    def search(self, search_obj):
        # Search for a user or phone number in the address book
        if search_obj.value in self.data:
            phones_iter = self.data[search_obj.value].phones
            print(list(map(lambda x: x.value, phones_iter)))
        else:
            for key, val in self.data.items():
                if list(filter(lambda x: x.value == search_obj.value, val.phones)):
                    print(key)
                else:
                    print("I can't find this user or phone number")

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
            print("Incorrect phone number. Please try again.")
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