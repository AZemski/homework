from authenticator import Authenticator
from exceptions import RegistrationError, AuthorizationError
from datetime import datetime
import random



def guess_number_game():
    random_number = random.randint(1, 5)
    attempts_game = 0
    while True:
        hidden_number = int(input(f"Попытка №{attempts_game + 1}. \nУгадай число от 1 до 5: "))
        if hidden_number == random_number:
            print(f"Поздравляю! \nТы угадал c {attempts_game + 1} попытки!")
            break
        attempts_game += 1
        # print(f"Сгенерированное число {random_number}. Играем дальше, ты не угадал")
        print("Играем дальше. \nТы не угадал.\n")

def cycle(func):
    def wrapper():
        while True:
            if func():
                break

    return wrapper

@cycle
def main() -> bool:

    if user_authenticator.login:
        print("Авторизация")
    else:
        print("Требуется зарегистрироваться")
    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    if user_authenticator.login:
        try:
            user_authenticator.authorize(login, password)
        except AuthorizationError as error:
            print(error)
            return False
        # clock = datetime.fromisoformat(user.last_success_login_at).strftime("%d.%m.%Y %H:%M:%S")
        clock = user_authenticator.last_success_login_at.strftime("%d.%m.%Y %H:%M:%S")
        print(f"Привет, {user_authenticator.login[0].upper() + user_authenticator.login[1:]} \nВремя авторизации: {clock} \nВы пытались войти: {user_authenticator.errors_count} раз")
    else:
        try:
            user_authenticator.registrate(login, password)
        except RegistrationError as error:
            print(error)
            return False
    # guess_number_game()
    return True

    # while True:
    #     login = input("Введите логин: ")
    #     password = input("Введите пароль: ")
    #
    #     if user.login:
    #         try:
    #             user.authorize(login, password)
    #             clock = datetime.fromisoformat(user.last_success_login_at).strftime("%d.%m.%Y %H:%M:%S")
    #             print(f"Привет, {user.login[0].upper() + user.login[1:]} \nВремя авторизации: {clock} \nВы пытались войти: {user.errors_count} раз")
    #             break
    #         except AuthorizationError as error:
    #             print(error)
    #
    #     else:
    #         try:
    #             user.registrate(login, password)
    #         except RegistrationError as error:
    #             print(error)
    #         break


if __name__ == '__main__':
    user_authenticator = Authenticator()
    main()
guess_number_game()
