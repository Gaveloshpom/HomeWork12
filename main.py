from classes import AddressBook, Record
""""
Commands to use:
hello: Says "Hello" to you
create Name: creates a new contact with {Name}
add number Name Phone: add phone number {Phone} to user with name {Name}
change Name New_name: change users {Name} to {New_name}
show all: shows all users in Book
good bye/close/exit: stops program
delete phone Name Phone: deletes {Phone} of user with name {Name}
page A B : shows users with index from A to B,
birthday Name Birthday_date: add {birthday_date} to {Name},
days left Name: shows how many days left for {Name}`s  birthday,
!!! ДЗ 12 !!!
Якщо файл відсутній напишіть NO і по завершенню роботи він автоматично створиться і ви зможете його використати наступного разу
find A: знайде контакти в імені або в номері телефону яких є збіги 
"""


def input_error(func):
    def inner(*user_data):
        try:
            return func(*user_data)
        except IndexError:
            return "Недостатньо інформації, перевірте дані."
        except ValueError as exception:
            return exception.args[0]

    return inner


@input_error
def create(data, *_):
    name = data[0]
    if name not in book:
        book.add_record(name)
        return f"successful created {name} "
    else:
        raise ValueError('This contact already exist.')


@input_error
def create_1(data, *_):
    name = data
    if name not in book:
        book.add_record(name)
        return f"successful created {name} "
    else:
        raise ValueError('This contact already exist.')


@input_error
def delete_phone(main_record: Record, user_info: list):
    return main_record.delete_phone(int(user_info[1]))


@input_error
def change(old_name: Record, new_name):
    if old_name.name.value != new_name[1]:
        return book.change_contact_name(old_name, new_name[1])
    else:
        return f"Old name {old_name.name.value} the same as new {new_name[1]}"


@input_error
def add_number(main_record: Record, user_info: list):
    return main_record.add_phone(user_info[1])


@input_error
def add_number_2(main_record: Record, user_info: list):
    return main_record.add_phone(user_info)


@input_error
def add_birthday(main_record: Record, user_info):
    return main_record.add_birthday(user_info[1])


# @input_error
def days_to_birthday(main_record: Record, *_):
    return main_record.days_to_birthday()


@input_error
def phone_search(name):
    if name.strip() not in book:
        raise ValueError("This contact does`t exist")
    a = book.get(name.strip())
    return a


@input_error
def exit_func(*_):
    global global_true
    global_true = False
    print("Bye!")


@input_error
def hello_func(*_):
    return "Hello"


def show_all(*_):
    full_list = []
    for k, v in book.items():
        full_list.append(f"{v.name.value}. Phones: {[i.value for i in v.phones]}. Birthday:{v.birthday.value if v.birthday else None}")
    print(full_list)
    return full_list


def show_part(data: list):
    value_1 = int(data[0])
    value_2 = int(data[1])
    print(book.iterator(value_1, value_2))


def create_data(data):

    new_data = data.strip().split(" ")
    name = new_data[0]
    phone = new_data[1]
    if name.isnumeric():
        raise ValueError("Must be a str, not int/float")
    if not phone.isnumeric():
        raise ValueError("Must be a number, not str")
    return name, phone


def change_input(data):
    if not data:
        return ['', '']
    splited_text = data.split()

    if splited_text[0].lower() in ("add", "good", "delete", "days"):
        return [" ".join(splited_text[:2]).lower(), splited_text[2:]]
    else:
        return [splited_text[0].lower(), splited_text[1:]]


def reaction_func(reaction):
    signature = command_dict[reaction]
    return signature


def break_func():
    return 'Wrong enter.'


def find(user_info):
    users_list = []
    if user_info[0].isnumeric():
        user_info = str(user_info[0])
        for phone in book.values():
            for phone_1 in phone.phones:
                phone_1 = str(phone_1.value)
                answer = phone_1.find(user_info)
                if answer >= 0:
                    users_list.append(f"{phone.name.value}| Phones: {[i.value for i in phone.phones]} | Birthday:{phone.birthday.value if phone.birthday else None}███ ")
                    break

        print(users_list)
    else:
        user_info = str(user_info[0])
        for a in book.keys():
            answer = a.find(user_info)
            if answer >= 0:
                users_list.append(f"{a}| Phones: {[i.value for i in book[a].phones]} | Birthday:{book[a].birthday.value if book[a].birthday else None}███ ")

        print(users_list)


def load():
    answer = input("Чи бажаєте ви відновити дані з файлу: data.bin (Yes)/(No)? ")
    if answer.lower() == "yes":
        answer = True
    else:
        answer = False

    if answer is True:
        file_name = "Phonebook.txt"
        with open(file_name, "r") as fh:
            raw_data = fh.readlines()
            for line in raw_data:
                name, phones, birthday = line.split("|")
                _, phones = phones.split(":")
                _, birthday = birthday.split(":")
                birthday = birthday.removesuffix("\n")
                birthday = birthday.replace("-", ".")
                phones = phones[phones.find("[") + 1:phones.find("]")]
                phones = phones.split(", ")
                list_birthday = ["1"]
                list_birthday.append(birthday)
                list_phones = []
                list_phones.append(phones)
                create_1(name)
                if phones:
                    for number in phones:
                        add_number_2(book[name], number)
                if birthday:
                    add_birthday(book[name], list_birthday)


def save():
    answer_2 = input("Чи бажаєте зберегти зміни (Yes)/(No)? ")
    if answer_2 == "Yes":
        answer_2 = True
    else:
        answer_2 = False
    if answer_2 is True:
        file_name = "Phonebook.txt"
        with open(file_name, "w") as fh:
            for k, v in book.items():
                fh.write(f"{v.name.value}| Phones: {[i.value for i in v.phones]} | Birthday:{v.birthday.value if v.birthday else None} \n")


global_true = True


def main():
    global global_true
    load()
    while global_true is True:
        command = input('Enter command for bot: ')
        user_command, user_data = change_input(command)

        if user_command not in command_dict:
            print(f"Unknown command  '{user_command}'")
            continue

        if user_command == "create":
            result = reaction_func(user_command)(user_data)
            print(result)
            continue

        if user_command == "show" or user_command == "page" or user_command == "find":
            reaction_func(user_command)(user_data)
            continue

        try:
            main_record = book[user_data[0]] if user_data else None
        except KeyError:
            print(
                f"This contact {user_data[0]} doesn't found. Please repeat or create new command")
            continue
        result = reaction_func(user_command)(main_record, user_data)
        if result:
            print(result)
    save()

command_dict = {
    'hello': hello_func,
    'create': create,
    'change': change,
    'add number': add_number,
    'delete phone': delete_phone,
    'phone': phone_search,
    'show': show_all,
    'good bye': exit_func,
    'close': exit_func,
    'exit': exit_func,
    'page': show_part,
    'birthday': add_birthday,
    'days left': days_to_birthday,
    'find': find,
}


if __name__ == '__main__':
    book = AddressBook()
    main()
