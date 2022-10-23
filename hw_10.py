from collections import UserDict
from datetime import datetime


class AddressBook(UserDict):
    #Класс AddressBook, который наследуется от UserDict, и мы потом добавим логику поиска по записям в этот класс.
    current_index = 0
    N = 2
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self):
        show_list = []
        names = [name for name in self.data]
        while len(self.data) >= AddressBook.current_index:
            for name in names[AddressBook.current_index: min(len(self.data), AddressBook.current_index + AddressBook.N)]:
                if self.data[name].birthday != "":
                    show_list.append(f"{self.data[name].name.value}: phone{[phone.value for phone in self.data[name].phones]}, birthday {self.data[name].birthday}")
                else:
                    show_list.append(f"{self.data[name].name.value}: phone{[phone.value for phone in self.data[name].phones]}")
            yield show_list
            AddressBook.current_index += AddressBook.N
            show_list = []


class Record:
    #Класс Record, который отвечает за логику добавления/удаления/редактирования необязательных полей и хранения обязательного поля Name.
    def __init__(self, name, phone = None, birthday = None):
        self.name = Name(name)
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = ""

    def add_birthday(self, birthday):
        self.birthday += Birthday(birthday).value.strftime('%d.%m.%Y')

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone_for_delete):
        for phone in self.phones:
            if phone.value == phone_for_delete:
                self.phones.remove(phone)

    def change_phone(self, phone_for_change, new_phone):
        for index, phone in enumerate(self.phones):
            if phone.value == phone_for_change:
                self.phones[index] = Phone(new_phone)

    def days_to_birthday(self):
        if self.birthday:
            birthday = datetime.strptime(self.birthday,'%d.%m.%Y')
            if ((birthday).replace(year=(datetime.now()).year)) > datetime.now():
                print (f"to birthday {(((birthday).replace(year=(datetime.now()).year)) - datetime.now()).days} days")
            else:
                print (f"to birthday {(((birthday).replace(year=(datetime.now()).year + 1)) - datetime.now()).days} days")
        else:
            print("Contact's birthday wasn't added")


class Field:
    #Класс Field, который будет родительским для всех полей, в нем потом реализуем логику общую для всех полей.
    def __init__(self, value):
        self.value = value


class Name(Field):
    #Класс Name, обязательное поле с именем.
    pass
    

class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value:str):
        if not all((value.startswith('+380'), value[1:].isdigit(), len(value) == 13)):
            raise ValueError(print("Your phone should be like this: +380888888888"))
        self.__value = value


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return datetime.strftime(self.__value, '%d.%m.%Y')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            date_birthday = datetime.strptime(value, '%d.%m.%Y')
            self.__value = date_birthday
        except:
            raise ValueError(print("Your birthday should be like this: 20.12.2000"))