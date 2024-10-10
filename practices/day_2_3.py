import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import random
import datetime


TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def do_on_start(message):
    bot.send_message(message.chat.id, "Я умею здороваться и прощаться, "
                     "а еще я могу сообщить текущее время, выдать "
                     "случайное число и рассказать шутку про "
                     "программистов. \nИспользуй "
                     "команды  /greet и /bye, /time, "
                     "/random и /joke. \nНу и напоследок: вы "
                     "можете добавлять заметки с помощью команды "
                     " /add и просматривать их с помощью команды"
                     " /notes.")

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

# Список шуток про программистов
jokes = [
    "Почему программисты не любят природу? Слишком много багов.",
    "Сколько программистов нужно, чтобы вкрутить лампочку? Ни одного, это аппаратная проблема.",
    "Почему программисты путают Рождество с Хэллоуином? Потому что Oct 31 == Dec 25.",
    "Программист заходит в бар, заказывает 1 пиво. "
    "Заказывает 10 пива. Заказывает 0 пива. Заказывает -1 пива. Заказывает qwerty пива."
]

# Обработчик команды /joke
@bot.message_handler(commands=['joke'])
def do_on_joke(message):
    joke = random.choice(jokes)
    bot.reply_to(message, joke)

user_notes = {}

def add_note(user_id, note):
    if user_id not in user_notes:
        user_notes[user_id] = []
    user_notes[user_id].append(note)

def get_notes(user_id):
    return user_notes.get(user_id, [])

@bot.message_handler(commands=['add'])
def add_note_handler(message):
    note = message.text[len('/add'):].strip()
    if note:
        add_note(message.from_user.id, note)
        bot.reply_to(message, "Заметка добавлена!")
    else:
        bot.reply_to(message, "Пожалуйста, введите текст заметки после команды /add")

@bot.message_handler(commands=['notes'])
def list_notes_handler(message):
    notes = get_notes(message.from_user.id)
    if notes:
        response = "Ваши заметки:\n" + "\n".join(notes)
    else:
        response = "У вас пока нет заметок."
    bot.reply_to(message, response)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    username = message.from_user.first_name
    if username:
        bot.send_message(message.chat.id,
                         f"Извините, {username}, я вас не понял. Попробуйте использовать команды /greet или /bye.")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Попробуйте использовать команды /greet или /bye.")

# Запуск бота
bot.infinity_polling()