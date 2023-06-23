from collections import UserDict


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, search_obj):
        if search_obj.value in self.data:
            phones_iter = self.data[search_obj.value].phones
            print(list(map(lambda x: x.value, phones_iter)))

        else:
            for key, val in self.data.items():
                if list(filter(lambda x: x.value == search_obj.value, val.phones)):
                    print(key)
                else:
                    print("I can't find this user or phone number")


class Record:

    def __init__(self, name, phone=None):
        self.name = name
        self.phones = []
        if phone is not None:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        for index, user_phone in enumerate(self.phones):
            if user_phone.value == phone.value:
                self.phones.pop(index)

    def edit_phone(self, old_phone, new_phone):
        for index, user_phone in enumerate(self.phones):
            if user_phone.value == old_phone.value:
                self.phones[index] = new_phone


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass
