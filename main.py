import telebot
from config import TOKEN
from extensions import *

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f'Отправьте сообщение в виде: \n<имя валюты, цену\
 которой вы хотите узнать>, <имя валюты, в которой надо узнать цену первой\
 валюты> <количество первой валюты>. \
Используйте: \n /help - инструкция по применению бота\n \
/values - доступные валюты.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys:
        text = text + f'\n{key.capitalize()}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        variables = message.text.split(' ')

        if len(variables) > 3:
            raise APIException('Переменных больше 3')
        elif len(variables) == 2:
            print(variables)
            variables.append('1')
            print(variables)
        elif len(variables) == 1:
            raise APIException('Переменная одна')

        base, quote, amount = variables
        base, quote, answer = Converter.convert(base, quote, amount)

    except APIException as e:
        print(message.text)
        bot.reply_to(message, e)
    except Exception as e:
        print(message.text)
        bot.reply_to(message, f'Не удалось обработать команду. Ошибка: {e}')
    else:
        bot.reply_to(message, f'В {amount} {base} - {answer} {quote} ')


bot.polling()
