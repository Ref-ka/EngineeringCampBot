import telebot

API_TOKEN = 'some token'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['помощь', 'начать'])
def send_welcome(message):
    bot.reply_to(message, 'Привет, я бот, который умеет повторять сообщения!')


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
