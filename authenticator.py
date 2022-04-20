from datetime import datetime
import os.path
from exceptions import AuthorizationError, RegistrationError
import json
import hashlib
import uuid
import re

#
class Validator:
    errors_count: int = 0

    def __init__(self, login, password):
        self.salt = uuid.uuid4().hex
        self.login = login
        self.password = password
        self.valid_login(self.login)
        self.valid_password(self.password)
        self.convert_password_hesh()

    @classmethod
    def valid_login(cls, login):
        if len(re.findall(r".+@.+\..+", login)) != 1:
            cls.errors_count += 1
            raise RegistrationError("Для регистрации введите почту")

    @classmethod
    def valid_password(cls, password):
        if len(set(re.findall(r"[^A-z0-9А-яЁё]", password))) == 0 or \
                len(set(re.findall(r"[a-zа-яё]", password))) == 0 or \
                len(set(re.findall(r"[A-ZА-ЯЁ]", password))) == 0 or \
                len(set(re.findall(r"[0-9]", password))) == 0 or \
                len(password) < 4:
            cls.errors_count += 1
            raise RegistrationError("Пароль должен содержать не менее 4 символов, не менее одного символа в верхнем регистре, не менее одного символа в верхнем регистре, не менее одной цифры, не менее одного специального символа")

    def convert_password_hesh(self):
        self.password = {"key": self.salt,
                         "hesh": hashlib.sha512(self.salt.encode() + self.password.encode()).hexdigest()}
#

class Authenticator:
    def __init__(self):
        self.data: list[Validator] = []
        self.login: str | None = None
        self._password: str | None = None
        self.last_success_login_at: datetime | None = None
        self.errors_count: int = 0

        if self._is_auth_file_exist():
            self._read_auth_file()

    @staticmethod
    def _is_auth_file_exist() -> bool:
        """Метод проверки наличия файла 'auth.json'"""
        return os.path.isfile('auth.json')

    def _read_auth_file(self) -> None:
        """Метод чтения данных из файла 'auth.json"""
        with open('auth.json', 'r') as f:
            data = json.load(f)
            self.login = data["login"]
            self._password = data["password"]
            self.last_success_login_at = datetime.fromisoformat(data["time"])
            self.errors_count = int(data["errors_count"])

    def _update_auth_file(self) -> None:
        """Метод перезаписи данные в файле 'auth.txt'"""
        with open("auth.json", "w") as f:
            self.last_success_login_at = datetime.utcnow()
            data = {"login": self.login,
                    "password": self._password,
                    "time": datetime.utcnow().isoformat(" "),
                    "errors_count": self.errors_count
                    }
            json.dump(data, f)

    def authorize(self, login, password) -> None:
        """Функция принимает строки, сверяет их со строками из файла и перезаписывает файл"""
        if login and password:
            key = dict(self._password)["key"]
            password = hashlib.sha512(key.encode() + password.encode()).hexdigest()
            if login != self.login or password != dict(self._password)["hesh"]:
                self.errors_count += 1
                self._update_auth_file()
                raise AuthorizationError("Неверный пароль\n")

        else:
            self.errors_count += 1
            self._update_auth_file()
            raise AuthorizationError("Введите логин и пароль\n")

    def registrate(self, data: Validator) -> None:
        """Функция принимает строки и перезаписывает файл 'auth.txt"""
        if self.login:
            self.errors_count += 1
            self._update_auth_file()
            raise RegistrationError("Ошибка регистрации")

        self.data.append(data)
        self.login = self.data[-1].login
        self._password = self.data[-1].password
        self.errors_count += self.data[-1].errors_count
        self._update_auth_file()
