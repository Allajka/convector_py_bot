import telebot
from telebot import types
bot = telebot.TeleBot("5738163783:AAFU7gKJ4w3eb3_W8v7_WT03jUCVbtLsQYk")

from_what_currency = ''
amount = ''
in_what_currency = ''


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Я Конвектор валют на текущую дату")
        bot.send_message(message.from_user.id, "Введите трехбуквенный код валюты, которую вы хотите конвертировать")
        bot.register_next_step_handler(message, input_from_currency)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


def input_from_currency(message):
    global from_what_currency
    from_what_currency = message.text
    from_what_currency = from_what_currency.replace(" ", "")
    if from_what_currency.isalpha() and len(from_what_currency) == 3 :
        bot.send_message(message.from_user.id, "Введите цифрами сколько необходимо конвектировать")
        bot.register_next_step_handler(message, amount_currency)
    else:
        bot.send_message(message.from_user.id, 'Некоректный ввод, повторите попытку')
        bot.send_message(message.from_user.id, "Введите трехбуквенный код валюты, которую вы хотите конвертировать")
        bot.register_next_step_handler(message, input_from_currency)


def amount_currency(message):
    global amount
    amount = message.text
    amount = amount.replace(" ", "")
    if amount.isdigit():
        bot.send_message(message.from_user.id,'Введите трехбуквенный код валюты, в которую вы хотите конвертировать')
        bot.register_next_step_handler(message, input_in_currency)
    else:
        bot.send_message(message.from_user.id, 'Некоректный ввод, повторите попытку')
        bot.send_message(message.from_user.id, "Введите цифрами сколько необходимо конвектировать")
        bot.register_next_step_handler(message, amount_currency)


def input_in_currency(message):
    global in_what_currency
    in_what_currency = message.text
    in_what_currency = in_what_currency.replace(" ", "")
    if in_what_currency.isalpha() and len(in_what_currency) == 3 :
        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = f'Нужно конвектировать {amount} {from_what_currency} в {in_what_currency}?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Некоректный ввод, повторите попытку')
        bot.send_message(message.from_user.id, 'Введите трехбуквенный код валюты, в которую вы хотите конвертировать')
        bot.register_next_step_handler(message, input_in_currency)




# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
#         #код сохранения данных, или их обработки
#         bot.send_message(call.message.chat.id, 'Запомню : )')
#     elif call.data == "no":
#         bot.send_message(call.message.chat.id, 'Начнем с начала! Напиши /start')
#         @bot.message_handler(content_types=['text'])
#         def start(message):
#             bot.send_message(message.from_user.id, "Как тебя зовут?")
#             bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name


bot.polling(none_stop=True, interval=0)