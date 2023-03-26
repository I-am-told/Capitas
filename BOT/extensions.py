import requests
import json
from config import *

class BotException(Exception):         # Пожалуй, можно было обойтись только одним родительским классом по исключениям,
    pass                               # но когда я только начинал писать программу, я думал, что, возможно, будут
                                       # ошибки, связанные не только с неправильным вводом пользователя. И решил
class InputError(BotException):        # сделать отдельного родителя конкретно под неправильный ввод. Однако,
    pass                               # возможность создать класс с ошибками другого рода - осталась не востребована.
                                       # Но я все же решил оставить такую возможность. Потому что код должен быть гибким
class WrongLenRequest(InputError):
    def __str__(self):
        return 'Не удалось обработать запрос\n'\
               'Запрос должен быть введен в формате:\n' \
               f'{rules_request}'

class NotFoundCurrency(InputError):
    def __init__(self, arg):
        self.arg = arg
    def __str__(self):
        return 'Не удалось обработать запрос\n'\
               f'Валюта {self.arg} не найдена\n' \

class SameCurrencies(InputError):
    def __str__(self):
        return 'Не удалось обработать запрос\n'\
               'Введены одинаковые валюты\n'


class Convert:
    '''Класс, хранящий в себе метод по проверке на корректность введенных
    пользователем запросов, метод обрабаотывающий пользовательский запрос,
    который формирует переменные для дальнейшего осуществления get-запроса
    а так же метод, осуществляющий сам get-запрос'''

    # Метод, обрабатывающий пользовательский запрос.
    @classmethod
    def get_values(cls, values: list) -> list:
        values.pop(2)                                   # Удаляем букву "в".
        amount, quote, base = values                    # Присваиваем переменным соответствующие значения.
        for j in keys.values():                         # Ищем в словаре keys значения.
            for i in j:                                 # В этих значениях проходимся циклом по содержимому, напр.
                if i[:3].lower() == quote[:3].lower():  # в ['USD', 'Доллар', 'dollar'] ищем совпадения первых трех
                    quote = j[0]                        # символов. Если  находим - присваиваем соответствующей
                if i[:3].lower() == base[:3].lower():   # переменной новое значение, которое потом можно будет
                    base = j[0]                         # подставить в get-запрос.
        return [float(amount), quote, base]

    # Метод по проверке на корректность введенных пользователем запросов. В нем мы
    # имеем вызов функции  get_values(). Возвращает tuple состоящий из двух элементов.
    # Первый элемент - нуль если была ошибка, и единица - если все прошло хорошо. Второй элемент это либо
    # текст ошибки, либо список с уже обработанными переменными amount, quote, base, которые мы в
    # дальнейшем передаем в фунцкию get_price() для получения ответа.
    @classmethod
    def check_exception(cls, message: telebot.types.Message) -> tuple:
        values = message.text.split()                   # Разбиваем строку, введенную пользоватлем на список слов
        try:                                            # Пытаемся перевести первое слово в тип данных float, если это
            values[0] = float(values[0].replace(',', '.'))   # не удается сделать, то отлавливаем соответствующую ошибку
        except ValueError:                              # и добавляем единицу в начало. Это сделано на случай, если
            values.insert(0, '1')                       # пользователю станет интересен просто курс двух валют и он
        try:                                            # введет просто две валюты, напр. "дол евро".
            if values[2] != 'в':                        # Далее добавляем в запрос букву "в" если пользователь этого
                values.insert(2, 'в')                   # по какой-то причине не сделал. При чем здесь же сразу идет
        except IndexError:                              # отлов ошибки, если пользователь ввел менее 2 слов (то есть,
            print(WrongLenRequest)                      # в сообщении пользователя не было найдено слово с  индексом 2)
        try:                                            # К этому моменту у нас должно быть ровно 4 слова в сообщении
            if len(values) != 4:                        # пользователя, даже если он ввел всего два, напр. "дол евро".
                raise WrongLenRequest                   # Делаем соответствующую проверку.
        except InputError as e:
            return (0, e)
        else:
            get_values = cls.get_values(values)         # Если до сих пор все было хорошо и сообщение пользователя
            try:                                        # прошло все проверки - вызываем функцию get_values()
                for i in get_values[1:]:                        # Осуществляем проверку полученных переменных на наличие
                    lst_val = [i[0] for i in keys.values()]     # их в списке валют ['RUB', 'USD', 'EUR', 'GBP']
                    if i not in lst_val:
                        raise NotFoundCurrency(i)       # Если совпадений не было найдено - вызываем ошибку.
                if get_values[1] == get_values[2]:      # Если введены одинаковые валюты - вызываем ошибку.
                    raise SameCurrencies
            except InputError as e:
                return (0, e)
            else:                                       # Если все проверки успешно были пройдены - возвращаем
                return (1, get_values)                  # положительный ответ с переменными.

    # Метод, осуществляющий get-запрос. Принимает в себя переменные от функции check_exception() и
    # длину округления, по умолчанию 2.
    @staticmethod
    def get_price(amount: float, quote: str, base: str, rounding_length = 2) -> str:
        r = requests.get(f'https://v6.exchangerate-api.com/v6/bc5667c30dd0a28de4a4a4f8/pair/{quote}/{base}')
        rate = float(json.loads(r.content)['conversion_rate'])   # Изымание курса из ответа
        date = json.loads(r.content)['time_last_update_utc']     # Изымание последней даты обновления курса
        text = f'По состоянию на {date[5:17]} \n' \
               f'Стоимость {amount} {quote} составляет {round((rate * amount), rounding_length)} {base}'
        return text