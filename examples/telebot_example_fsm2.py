import telebot
from telebot.handler_backends import State, StatesGroup
from telebot.custom_filters import StateFilter
from telebot.storage import StateMemoryStorage

# Инициализация бота
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(API_TOKEN, state_storage=state_storage)

# Определение состояний
class TaskStates(StatesGroup):
    adding_name = State()
    adding_surname = State()
    confirm = State()

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я могу запомнить твои имя и фамилию. Используйте команду /add")

# Команда /add для запоминания
@bot.message_handler(commands=['add'])
def add_task(message):
    bot.set_state(message.from_user.id, TaskStates.adding_name, message.chat.id)
    bot.send_message(message.chat.id, "Введите ваше имя:")

# Команда /cancel для выхода из текущего состояния
@bot.message_handler(commands=['cancel'], state='*')
def cancel(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, "Действие отменено. Вы можете начать заново, используя команду /add.")

# Обработка состояния добавления имени
@bot.message_handler(state=TaskStates.adding_name)
def enter_title(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.set_state(message.from_user.id, TaskStates.adding_surname, message.chat.id)
    bot.send_message(message.chat.id, "Введите вашу фамилию:")

# Обработка состояния добавления фамилии
@bot.message_handler(state=TaskStates.adding_surname)
def enter_description(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['surname'] = message.text
    bot.set_state(message.from_user.id, TaskStates.confirm, message.chat.id)
    bot.send_message(message.chat.id, f"Подтверждение обработки запроса.\n"
                                      "Для подтверждения введите 'да', для отмены /cancel")

# Обработка состояния подтверждения
@bot.message_handler(state=TaskStates.confirm)
def confirm(message):
    if message.text == 'да':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            bot.send_message(message.chat.id, f"Отлично, я всё запомнил. Вас зовут: {data['name']} {data['surname']}")
    else:
        bot.reply_to(message, "Вам нужно ввести 'да' для подтверждения, /cancel для отмены.")

# Добавляем фильтр состояний
bot.add_custom_filter(StateFilter(bot))

# Запуск бота
bot.polling(none_stop=True)
