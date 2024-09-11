import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

API_TOKEN = 'some token'

bot = telebot.TeleBot(API_TOKEN)

markups = {'default': ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('помощь'), KeyboardButton('кнопка'))}


@bot.message_handler(commands=['помощь', 'начать'])
def send_welcome(message):
    bot.reply_to(message, 'Привет, я бот, который умеет повторять сообщения!', reply_markup=markups['default'])


@bot.message_handler(commands=['кнопка'])
def button_check(message):
    bot.reply_to(message, 'Кнопка была нажата!', reply_markup=markups['default'])


bot.infinity_polling()
