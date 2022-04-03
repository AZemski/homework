from datetime import datetime
import os.path
from exceptions import AuthorizationError, RegistrationError

class Authenticator:
    def __init__(self):
        self.login: str | None = None
        self._password: str | None = None
        self.last_success_login_at: datetime | None = None
        self.errors_count: int = 0

        if self._is_auth_file_exist():
            self._read_auth_file()
        else:
            print("Требуется зарегистрироваться")

    def _is_auth_file_exist(self) -> bool:
        """Метод проверки наличия файла 'auth.txt'"""
        return os.path.isfile('auth.txt')

    def _read_auth_file(self) -> None:
        """Метод чтения данных из файла 'auth.txt"""
        print("Авторизация")
        with open('auth.txt', 'r') as f:
            self.login = f.readline().strip()
            self._password = f.readline().strip()
            self.last_success_login_at = f.readline().strip()
            self.errors_count = int(f.readline().strip())

    def _update_auth_file(self) -> None:
        """Метод перезаписи данные в файле 'auth.txt'"""
        with open('auth.txt', 'w') as f:
            self.last_success_login_at = datetime.utcnow().isoformat(" ")
            f.write(f"{self.login}\n")
            f.write(f"{self._password}\n")
            f.writelines(self.last_success_login_at + '\n')
            f.write(f"{self.errors_count}\n")

    def authorize(self, login, password) -> None:
        """Функция принимает строки, сверяет их со строками из файла и перезаписывает файл"""
        if login:

            if login != self.login or password != self._password:
                self.errors_count: int
                self.errors_count += 1
                self._update_auth_file()
                raise AuthorizationError("Неверный пароль")

            else:
                self._update_auth_file()

        else:
            raise AuthorizationError("Введите логин")

    def registrate(self, login, password) -> None:
        """Функция принимает строки и перезаписывает файл 'auth.txt"""
        if self.login:
            self.errors_count += 1
            raise RegistrationError("Ошибка регистрации")

        if login:
            self.login = login
            self._password = password
            self._update_auth_file()

        else:
            self.errors_count += 1
            self._update_auth_file()
            raise RegistrationError("Введите логин")
