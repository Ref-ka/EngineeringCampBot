import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Замените 'YOUR_API_TOKEN' на токен вашего бота, который вы получили от BotFather
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("/greet"), KeyboardButton("/bye"))
    bot.send_message(message.chat.id, "Я умею здороваться и прощаться! Используйте команды /greet и /bye",
                     reply_markup=markup)

# Обработчик команды /greet
@bot.message_handler(commands=['greet'])
def send_welcome(message):
    username = message.from_user.first_name
    if username:
        bot.reply_to(message, f"Привет, {username}! Я ваш дружелюбный бот. Как я могу помочь вам сегодня?")
    else:
        bot.reply_to(message, "Привет! Я ваш дружелюбный бот. Как я могу помочь вам сегодня?")

# Обработчик команды /bye
@bot.message_handler(commands=['bye'])
def send_goodbye(message):
    username = message.from_user.first_name
    if username:
        bot.reply_to(message, f"До свидания, {username}! Надеюсь, скоро увидимся снова.")
    else:
        bot.reply_to(message, "До свидания! Надеюсь, скоро увидимся снова.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    username = message.from_user.first_name
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("/greet"), KeyboardButton("/bye"))
    if username:
        bot.send_message(message.chat.id,
                         f"Извините, {username}, я вас не понял. Попробуйте использовать команды /greet или /bye.",
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Попробуйте использовать команды /greet или /bye.",
                         reply_markup=markup)

# Запуск бота
bot.polling()