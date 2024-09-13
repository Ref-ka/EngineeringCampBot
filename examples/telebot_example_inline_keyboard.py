import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TELEGRAM_TOKEN = 'some token'

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Да", callback_data="cb_yes"),
               InlineKeyboardButton("Нет", callback_data="cb_no"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Ответ - Да")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Ответ - Нет")


@bot.message_handler(commands=['начать'])
def message_handler(message):
    bot.send_message(message.chat.id, "Да/нет?", reply_markup=gen_markup())


bot.infinity_polling()
