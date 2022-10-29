import telebot
from telebot import types
from convector import *


bot = telebot.TeleBot("5738163783:AAFU7gKJ4w3eb3_W8v7_WT03jUCVbtLsQYk")

from_what_currency = ''
amount = ''
in_what_currency = ''
result = ''


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "🤖🤖🤖🤖🤖🤖🤖 \nЯ бот - Конвертер валют на текущую дату")
        bot.send_message(message.from_user.id, "Введите трехбуквенный код валюты, ИЗ которой нужно конвертировать\n\n\nНапример: AUD, EUR, USD, CNY, RUB и д.р.")
        bot.register_next_step_handler(message, input_from_currency)
        info_logger(f'{message.from_user.username} /start')
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


def input_from_currency(message):
    global from_what_currency
    from_what_currency = message.text
    from_what_currency = from_what_currency.replace(" ", "")
    info_logger(f'{message.from_user.username} {from_what_currency}')
    if from_what_currency.isalpha() and len(from_what_currency) == 3:
        bot.send_message(message.from_user.id, "Сколько нужно конвертировать(введите цифрами)?")
        bot.register_next_step_handler(message, amount_currency)
    else:
        bot.send_message(message.from_user.id, '❗ ❗ ❗ \nНекорректный ввод, повторите попытку')
        bot.send_message(message.from_user.id, "Введите трехбуквенный код валюты, которую вы хотите конвертировать")
        bot.register_next_step_handler(message, input_from_currency)


def amount_currency(message):
    global amount
    amount = message.text
    amount = amount.replace(" ", "")
    info_logger(f'{message.from_user.username} {amount}')
    if amount.isdigit():
        bot.send_message(message.from_user.id, 'Введите трехбуквенный код валюты, в которую вы хотите конвертировать.\n\n Например: AUD, EUR, USD, CNY, RUB и д.р.')
        bot.register_next_step_handler(message, input_in_currency)
    else:
        bot.send_message(message.from_user.id, '❗ ❗ ❗ \nНекорректный ввод, повторите попытку')
        bot.send_message(message.from_user.id, "Введите цифрами сколько необходимо конвертировать")
        bot.register_next_step_handler(message, amount_currency)


def input_in_currency(message):
    global in_what_currency
    in_what_currency = message.text
    info_logger(f'{message.from_user.username} {in_what_currency}')
    in_what_currency = in_what_currency.replace(" ", "")
    if in_what_currency.isalpha() and len(in_what_currency) == 3:
        global result
        result = button_click(from_what_currency, amount, in_what_currency, message.from_user.username)
        keyboard = types.InlineKeyboardMarkup();
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = f'Нужно конвертировать {amount} {from_what_currency} в {in_what_currency}?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, '❗ ❗ ❗ \nНекорректный ввод, повторите попытку')
        bot.send_message(message.from_user.id, 'Введите трехбуквенный код валюты, в которую вы хотите конвертировать')
        bot.register_next_step_handler(message, input_in_currency)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, result)
        bot.send_message(call.message.chat.id, 'Можем повторить! Напиши /start')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Начнем с начала! Напиши /start')


bot.polling(none_stop=True, interval=0)
