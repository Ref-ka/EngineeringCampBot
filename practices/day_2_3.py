import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import random
import datetime


TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Список шуток про программистов
jokes = [
    "Почему программисты не любят природу? Слишком много багов.",
    "Сколько программистов нужно, чтобы вкрутить лампочку? Ни одного, это аппаратная проблема.",
    "Почему программисты путают Рождество с Хэллоуином? Потому что Oct 31 == Dec 25.",
    "Программист заходит в бар, заказывает 1 пиво. "
    "Заказывает 10 пива. Заказывает 0 пива. Заказывает -1 пива. Заказывает qwerty пива."
]

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def do_on_start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("/greet"), KeyboardButton("/bye"))
    bot.send_message(message.chat.id, "Я умею здороваться и прощаться, "
                     "а еще я могу сообщить текущее время, выдать случайное "
                     "число и рассказать шутку про программистов. \nИспользуй "
                     "команды  /greet и /bye, /time, /random и /joke.",
                     reply_markup=markup)

# Обработчик команды /greet
@bot.message_handler(commands=['greet'])
def do_on_greet(message):
    username = message.from_user.first_name
    if username:
        bot.reply_to(message, f"Привет, {username}! Я ваш дружелюбный бот. Как я могу помочь вам сегодня?")
    else:
        bot.reply_to(message, "Привет! Я ваш дружелюбный бот. Как я могу помочь вам сегодня?")

# Обработчик команды /bye
@bot.message_handler(commands=['bye'])
def do_on_goodbye(message):
    username = message.from_user.first_name
    if username:
        bot.reply_to(message, f"До свидания, {username}! Надеюсь, скоро увидимся снова.")
    else:
        bot.reply_to(message, "До свидания! Надеюсь, скоро увидимся снова.")


# Обработчик команды /time
@bot.message_handler(commands=['time'])
def do_on_time(message):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    bot.reply_to(message, f"Сейчас {current_time}")

# Обработчик команды /random
@bot.message_handler(commands=['random'])
def do_on_random(message):
    random_number = random.randint(1, 100)
    bot.reply_to(message, f"Случайное число: {random_number}")

# Обработчик команды /joke
@bot.message_handler(commands=['joke'])
def do_on_joke(message):
    joke = random.choice(jokes)
    bot.reply_to(message, joke)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
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
bot.infinity_polling()