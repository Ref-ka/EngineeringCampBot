import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from telebot.custom_filters import StateFilter
import sqlite3
from datetime import datetime

# Создаем соединение с базой данных SQLite
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицу tasks, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    description TEXT,
    due_date TEXT
)
''')
conn.commit()

# Инициализация бота
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage)

# Определение состояний
class TaskStates(StatesGroup):
    adding_title = State()
    adding_description = State()
    adding_due_date = State()

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я TaskMasterBot. Я помогу тебе управлять твоими задачами. Используй /add для добавления новой задачи.")

# Команда /add для добавления новой задачи
@bot.message_handler(commands=['add'])
def add_task(message):
    bot.set_state(message.from_user.id, TaskStates.adding_title, message.chat.id)
    bot.send_message(message.chat.id, "Введите название задачи:")

# Обработка состояния добавления названия задачи
@bot.message_handler(state=TaskStates.adding_title)
def enter_title(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['title'] = message.text
    bot.set_state(message.from_user.id, TaskStates.adding_description, message.chat.id)
    bot.send_message(message.chat.id, "Введите описание задачи:")

# Обработка состояния добавления описания задачи
@bot.message_handler(state=TaskStates.adding_description)
def enter_description(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['description'] = message.text
    bot.set_state(message.from_user.id, TaskStates.adding_due_date, message.chat.id)
    bot.send_message(message.chat.id, "Введите срок выполнения задачи (в формате YYYY-MM-DD):")

# Обработка состояния добавления срока выполнения задачи
@bot.message_handler(state=TaskStates.adding_due_date)
def enter_due_date(message):
    try:
        due_date = datetime.strptime(message.text, '%Y-%m-%d')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            cursor.execute('''
                INSERT INTO tasks (user_id, title, description, due_date) VALUES (?, ?, ?, ?)
            ''', (message.from_user.id, data['title'], data['description'], due_date.strftime('%Y-%m-%d')))
            conn.commit()
        bot.send_message(message.chat.id, "Задача успешно добавлена!")
        bot.delete_state(message.from_user.id, message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат даты. Пожалуйста, введите дату в формате YYYY-MM-DD.")

# Команда /list для просмотра всех задач
@bot.message_handler(commands=['list'])
def list_tasks(message):
    cursor.execute('SELECT id, title, due_date, description FROM tasks WHERE user_id = ?', (message.from_user.id,))
    tasks = cursor.fetchall()
    if tasks:
        response = "Ваши задачи:\n"
        for task in tasks:
            response += f"{task[0]}. {task[1]} (до {task[2]})\n    {task[3]}\n"
    else:
        response = "У вас нет задач."
    bot.send_message(message.chat.id, response)

# Добавляем фильтр состояний
bot.add_custom_filter(StateFilter(bot))

# Запуск бота
bot.polling(none_stop=True)