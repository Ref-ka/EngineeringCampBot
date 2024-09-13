import telebot
import random
import datetime


# Получение токена из переменной окружения
TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Список шуток про программистов
jokes = [
    "Почему программисты не любят природу? Слишком много багов.",
    "Сколько программистов нужно, чтобы вкрутить лампочку? Ни одного, это аппаратная проблема.",
    "Почему программисты путают Рождество с Хэллоуином? Потому что Oct 31 == Dec 25.",
    "Программист заходит в бар, заказывает 1 пиво. Заказывает 10 пива. Заказывает 0 пива. Заказывает -1 пива. Заказывает qwerty пива."
]

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может сообщить текущее время, выдать случайное число и рассказать шутку про программистов. Используй команды /time, /random и /joke.")

# Обработчик команды /time
@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    bot.reply_to(message, f"Сейчас {current_time}")

# Обработчик команды /random
@bot.message_handler(commands=['random'])
def send_random_number(message):
    random_number = random.randint(1, 100)
    bot.reply_to(message, f"Случайное число: {random_number}")

# Обработчик команды /joke
@bot.message_handler(commands=['joke'])
def send_joke(message):
    joke = random.choice(jokes)
    bot.reply_to(message, joke)

# Запуск бота
bot.polling()