import datetime

from exceptions import ValidateError

class Data:
    def __init__(self, name: str, age: str):
        self.name = name
        self.age = age
        self._clear_whitespaces()
        self.age = int(self.age)

    def _clear_whitespaces(self):
        self.name = self.name.strip()
        self.age = self.age.strip()


class DataWithDate(Data):
    def __init__(self, name: str, age: str):
        super().__init__(name, age)
        self.clock = datetime.datetime.utcnow()
        # self.clock = datetime.fromtimestamp(timestamp)


class Validator:
    def __init__(self):
        self.data_history: list[Data] = []

    def validate(self, data: Data):
        self.data_history.append(data)
        self._validate_name()
        self._validate_age()

    def _validate_name(self):

        if not self.data_history:
            raise ValidateError('Ошибка: Нет данных.\n')

        name = self.data_history[-1].name

        if not name:
            raise ValidateError('Ошибка: Вы не ввели имя.\n')

        elif len(name) < 3:
            raise ValidateError('Ошибка: Минимальная длина имени - 3 символа.\n')

        elif name.count(' ') > 1:
            raise ValidateError('Ошибка: Максимальное количество пробелов - 1 символ.\n')

    def _validate_age(self):

        if not self.data_history:
            raise ValueError('Неверный тип данных\n')

        age = self.data_history[-1].age

        # print(type(age))

        if age <= 0:
            raise ValidateError('Ошибка: Вам не может быть 0 лет или меньше.\n')

        elif age < 14:
            raise ValidateError('Ошибка: Программой запрещено пользоваться, если вам меньше 14 лет.\n')

