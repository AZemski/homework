"""
1. Создать 3 переменных с одинаковыми данными с одинаковыми идентификаторами.
2. Создать 2 переменных с одинаковыми данными с разными идентификаторами.
3. *Поменять их типы так, чтобы у 1х трех были разные идентификаторы, а у 2х последних были одинаковые.
"""
#
# a = b = c = 1
#
# print(id(a))
# print(id(b))
# print(id(c))
#
# print()
#
# x = [1]
# y = [1]
#
# print(id(x))
# print(id(y))
#
# print()

# a = int(1)
# b = float(1)
# c = str(1)
#
# print(id(a))
# print(id(b))
# print(id(c))
#
# print()
#
# x = int(1)
# y = int(1)
#
# print(id(x))
# print(id(y))
#
# print()

"""
Домашка:
1. Сделать последнюю домашку
2. Сделать функцию is_palindrome, которая определяет является ли строка палиндромом или нет. При этом введено может быть как слово, так и целые предложения с пробелами и с различными знаками препинания. Необходимо избегать всех символов кроме букв. А также не копировать входящие данные (например, развернуть строку через срез — это скопировать входящие данные)
3. Функции на проверку имени, возраста и совет паспорт должны возвращать None (иначе говоря, ничего не должны возвращать), если не было ошибок или нет советов
4. Сделать функцию, которая генерирует случайное число от 1 до 10, и в бесконечном цикле просит пользователя угадать это число, если пользователь ввёл имя и возраст корректные
"""

# def is_palindrome(word: str) -> bool:
#     """
#     Это функция проверяет строку на палиндром
#     """
#     i = 0
#     j = len(word) - 1
#
#     while i <= j:
#         if not word[i].isalpha():
#             i += 1
#             continue
#
#         elif not word[j].isalpha():
#             j -= 1
#             continue
#
#         elif word[i] != word[j]:
#             return False
#
#         i += 1
#         j -= 1
#
#     return True
#
# text = input("Введите слово или фразу для проверки на палиндром: ").lower()
# print(is_palindrome(text))

"""
Домашнее задание

1. Оптимизировать алгоритм
2. Переименовать функции на:
   1. validate_name - проверка имени
   2. validate_age - проверка возраста
   3. clear_whitespaces - функция очистки строки от пробелов в начале и конце
   4. get_passport_advice - функция получения совета по замену паспорту
   5. guess_number_game - игра "угадай число", где пользователь вводит число и пытается отгадать случайно сгенерированное число от 1 до 5
3. Все функции валидации (`validate_name`, validate_age`) должны всегда возвращать `None, а в случае ошибки - делать raise Exception(текст ошибки).
4. Использовать функцию clear_whitespaces еще и для введенной строки, в которой должно быть число.
5. В функции main, необходимо отловить ошибки из функций validate_name, validate_age. Вывести пользователю: "Я поймал ошибку: {текст ошибки}". И если были ошибки, тогда вам необходимо заново запросить у пользователя ввод данных.
6. В функции main обрабатывать ошибку ValueError (не используем Exception) во время перевода строки к int.
7. Перед запросом данных в функции main пользователю должно печататься номер текущей попытки ввода данных. Пользователю отображать попытки начиная с 1, в коде попытки должны быть с 0.
8. Во время игры "угадай число" тоже должен быть счетчик попыток, который будет отображаться при успешно угаданному числу. Пользователю отображать попытки начиная с 1, в коде попытки должны быть с 0.
"""

from exceptions import ValidateError
from validator import Validator
from validator import DataWithDate
from datetime import datetime
import random

# import re

__author__ = 'Anton Zemski'

def get_passport_advice(age: int) -> str | None:
    """Рекомендации по действиям с паспортом"""
    if 16 <= age <= 17:
        return '\nНе забудь получить первый паспорт по достижению 16 лет.'

    elif 25 <= age <= 26:
        return '\nНе забудь заменить паспорт по достижению 25 лет.'

    elif 45 <= age <= 46:
        return '\nНе забудь заменить паспорт по достижению 45 лет.'

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


def main() -> None:
    attempts_main = 0
    reference_point = datetime.utcnow()
    validator = Validator()
    while True:
        if attempts_main > 1:
            print(f'Количество ошибок {attempts_main}')
        name = input(f'ведите ваше имя: ')
        age = input('Введите ваш возраст: ')
        try:
            datavieu = DataWithDate(name, age)
        except ValueError as e:
            print(f'Неверный тип данных\n{e}')
            attempts_main += 1
            continue

        try_time = datavieu.clock

        try:
            validator.validate(datavieu)
        except ValidateError as e:
            print(f'{e}')
            attempts_main += 1
            continue
        else:
            time_format = "%Y-%m-%d %H:%M:%S"
            print(f'Время начала ввода данных: {reference_point:{time_format}}')
            print(f'Время конца обработки данных: {try_time:{time_format}}')
            print(f'Время затрачено на обработку данных: {try_time-reference_point}')
            name = datavieu.name
            age = datavieu.age

        break

    text = f'Привет, {name.title()}! \nТебе {age} лет.'
    advice = get_passport_advice(age)
    if advice is not None:
        text += advice

    print(text)
    # guess_number_game()

main()

print(f'Программа создана при поддержке {__author__}')
