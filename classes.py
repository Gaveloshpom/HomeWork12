from collections import UserDict
from datetime import date, datetime


class Field:

    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phones(Field):
    @Field.value.setter
    def value(self, value):
        if not value.isnumeric():
            raise ValueError("Must be only numbers")
        else:
            self._value = int(value)



class Birthday(Field):
    @Field.value.setter
    def value(self, new_value: str):
        try:
            new_value_1 = [int(i) for i in new_value.split(".")]
            birthday_date = date(*new_value_1)
        except ValueError:
            raise ValueError("Incorrect value, try again")
        except TypeError:
            raise TypeError("Incorrect format. Example: yyyy.mm.dd.")

        if birthday_date <= date.today():
            self._value = birthday_date
        else:
            raise ValueError("Incorrect date, try again")


class AddressBook(UserDict):

    def add_record(self, name):
        self.data[name] = Record(name)

    def change_contact_name(self, old_name, new_name: str):
        old = old_name.name.value
        self.data[new_name], self.data[old_name.name.value].name.value = self.data[old_name.name.value], new_name
        del self.data[old]
        return f"Name {old} changed to {new_name}."

    def get_records(self):
        print(self.data)
        return self.data

    def record_checker(self, name):
        return bool(self.data.get(name))

    def get_by_name(self, name):
        return self.data.get(name)

    def remove_record(self, name):
        del self.data[name]

    def search(self, value):
        if self.record_checker(value):
            return self.get_by_name(value)

        for record in self.get_records().values():
            for phone in record.phones:
                if phone.value == value:
                    return record

        raise ValueError("Contact with this value does not exist.")

    def iterator(self, value_1, value_2):
        full_list = []
        for i in range(value_1, value_2 + 1):
            a = 0

            for k, v in self.data.items():
                a += 1
                if i == a:
                    full_list.append(f"{v.name.value} | Phones: {[i.value for i in v.phones]} | Birthday:{v.birthday.value if v.birthday else None}")

        return full_list


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phones(phone)] if phone else []
        self.birthday = Birthday(birthday) if birthday else None

    def get_info(self):
        phone_info = ''

        for phone in self.phones:
            phone_info += f'{phone.value}, '

        return f'{self.name.value} : {phone_info[:-2]}'

    def add_phone(self, phone):
        self.phones.append(Phones(phone))
        return f"{phone} added to {self.name.value}"

    def delete_phone(self, number):
        for values in self.phones:
            if values.value == number:
                self.phones.remove(values)
                return f"Phone number {number} deleted for user {self.name.value}."
        else:
            return f"Can`t find {number} for user {self.name.value}"

    def change_phone(self, phones):
        for phone in phones:
            if not self.delete_phone(phone):
                self.add_phone(phone)

    def add_birthday(self, birthday_data):
        self.birthday = Birthday(birthday_data)
        return f"{self.birthday.value} added to {self.name.value}"

    def days_to_birthday(self):
        today = datetime.now()
        birthday_data = datetime(year=today.year, month=self.birthday.value.month, day=self.birthday.value.day)
        result = (birthday_data - today).days
        if result < 0:
            birthday_data = datetime(year=today.year+1, month=self.birthday.value.month, day=self.birthday.value.day)
            result = (birthday_data - today).days
            return f"{result} days to birthday!"
        elif result == 0:
            result += 1
            return f"{result} days left!"
        return f"{result} days left!"
