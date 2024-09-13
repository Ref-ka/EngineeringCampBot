import telebot
import sqlite3


def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            note TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Функция для добавления заметки в базу данных
def add_note(user_id, note):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (user_id, note) VALUES (?, ?)', (user_id, note))
    conn.commit()
    conn.close()

# Функция для получения всех заметок пользователя
def get_notes(user_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT note FROM notes WHERE user_id = ?', (user_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Вы можете добавлять заметки с помощью команды /add и просматривать их с помощью команды /notes.")

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
        response = "Ваши заметки:\n" + "\n".join([note[0] for note in notes])
    else:
        response = "У вас пока нет заметок."
    bot.reply_to(message, response)

# Запуск бота
bot.polling()