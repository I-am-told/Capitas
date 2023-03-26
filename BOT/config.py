import telebot


TOKEN = '5752026259:AAEvvzUuPxdHVb1aTBxvMdtOhCSO7_xv2us'

bot = telebot.TeleBot(TOKEN)

keys = {
    'Рубль': ['RUB','Рубль'],
    'Доллар': ['USD', 'Доллар', 'dollar'],
    'Евро': ['EUR', 'Евро'],
    'Фунт': ['GBP','Фунт', 'pound']}

rules_request = '\n<Количество валюты> <Валюта, КОТОРУЮ конвертируете> ' \
                'В <Валюта, В КОТОРУЮ конвертируете> \n' \
                '\nНапример: "10 Евро в фунтах" или "5.25 дол в руб" или просто "usd rub"\n'

