import telebot
import easy_sql

'''
У вас должна быть создана база данных с названием notes.db, названием таблицы notes,
колонками:
id, integer, primary key, autoincrement
user_id, integer, not null
note, text, not null
'''

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Функция для добавления заметки в базу данных
def add_note(user_id, note):
    easy_sql.insert('notes.db', 'notes', {'user_id': user_id, 'note': note})

# Функция для получения всех заметок пользователя
def get_notes(user_id):
    notes = easy_sql.fetchall('notes.db', 'notes', ['note'], f'user_id = {user_id}')
    return notes

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Вы можете добавлять "
                          "заметки с помощью команды /add и просматривать их с помощью команды /notes.")

# Обработчик команды /add
@bot.message_handler(commands=['add'])
def add_note_handler(message):
    note = message.text[len('/add '):].strip()
    if note:
        add_note(message.from_user.id, note)
        bot.reply_to(message, "Заметка добавлена!")
    else:
        bot.reply_to(message, "Пожалуйста, введите текст заметки после команды /add.")

# Обработчик команды /notes
@bot.message_handler(commands=['notes'])
def list_notes_handler(message):
    notes = get_notes(message.from_user.id)
    if notes:
        response = "Ваши заметки:\n" + "\n".join([note['note'] for note in notes])
    else:
        response = "У вас пока нет заметок."
    bot.reply_to(message, response)

# Запуск бота
bot.polling()