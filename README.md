# Address Book

This repository contains an implementation of an address book that allows users to manage contacts. The address book provides functionality for adding, deleting, editing, and searching records.

## Classes

### AddressBook

The `AddressBook` class is a subclass of `UserDict` and represents the address book. It provides the following methods:

- `add_record(record)`: Adds a `Record` object to the address book.
- `search(search_obj)`: Searches for records in the address book based on a given search object.

### Record

The `Record` class represents a contact record in the address book. It has a `name` field and a list of `phones`. The class provides the following methods:

- `__init__(name, phone=None)`: Initializes a record with a name and an optional phone number.
- `add_phone(phone)`: Adds a phone number to the record.
- `delete_phone(phone)`: Deletes a phone number from the record.
- `edit_phone(old_phone, new_phone)`: Edits a phone number in the record.

### Field

The `Field` class is the parent class for fields in a contact record. It has a `value` attribute that holds the field's value.

### Name

The `Name` class represents the name field in a contact record. It inherits from the `Field` class.

### Phone

The `Phone` class represents a phone number field in a contact record. It inherits from the `Field` class. A contact record can have multiple phone numbers.

## Usage

To use the address book, follow these steps:

1. Import the required classes from the module:
   ```python
   `from collections import UserDict`
   ```
   
2. Create an instance of the AddressBook class:
    ```python
    address_book = AddressBook()
    ```

3. Create instances of the Name and Phone classes:
    ```python
   name = Name("John Doe")
   phone = Phone("123-456-7890")
   ```

4. Create a Record object and add it to the address book:
    ```python
    record = Record(name, phone)
   address_book.add_record(record)
   ```

5. Perform operations on the address book:
    - Add a phone number to a record:
    ```python
      phone2 = Phone("987-654-3210")
       record.add_phone(phone2)
    ```

   - Delete a phone number from a record:
    ```python
       record.delete_phone(phone)
    ```

   - Edit a phone number in a record:
   ```python
       new_phone = Phone("555-555-5555")
       record.edit_phone(phone2, new_phone)
   ```

   - Search for records:
   ```python
       search_name = Name("John Doe")
       address_book.search(search_name)
   ```
