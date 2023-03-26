import telebot
from config import *
from extensions import Convert



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Что бы начать работу введите запрос в формате: \n' \
           f'{rules_request}'\
           '\nУвидеть список доступных валют: /currency'
    bot.reply_to(message, text)

@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def response(message: telebot.types.Message):
    check = Convert.check_exception(message)                # Проверяем введенный пользователем запрос на наличие ошибок.
    if check[0]:                                            # Если первый элемент tupl'а, который возвращает функция
        response = Convert.get_price(*check[1])             # check_exception() - True (то есть единица) то отправляем
        return bot.send_message(message.chat.id, response)  # второй элемент tupl'а в функцию get_price() для получения
    else:                                                   # ответа на get-запрос.
        return bot.send_message(message.chat.id, check[1])  # Если check_exception() возвращает в первом элементе нуль -
                                                            # отправляем пользователю текст ошибки.
bot.polling(none_stop=True)


