import telebot
from telebot import types
from telebot.handler_backends import State, StatesGroup
from telebot.custom_filters import StateFilter

# Замените 'YOUR_API_TOKEN' на токен вашего бота
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Определяем состояния
class MyStates(StatesGroup):
    name = State()  # Состояние приветствия
    eye_color = State()  # Состояние запроса имени
    hobby = State()  # Состояние прощания

# Создаем хранилище состояний в памяти
state_storage = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message: types.Message):
    bot.set_state(message.from_user.id, MyStates.name, message.chat.id)
    bot.send_message(message.chat.id, "Привет! Как тебя зовут?")

# Обработчик для состояния name
@bot.message_handler(state=MyStates.name)
def get_name(message: types.Message):
    name = message.text
    if message.chat.id not in state_storage:
        state_storage[message.chat.id] = {}
    state_storage[message.chat.id]['name'] = name
    bot.set_state(message.from_user.id, MyStates.eye_color, message.chat.id)
    bot.send_message(message.chat.id, f"Приятно познакомиться, {name}!\nНапиши свой цвет глаз.")

# Обработчик для состояния eye_color
@bot.message_handler(state=MyStates.eye_color)
def get_eye_color(message: types.Message):
    eye_color = message.text
    state_storage[message.chat.id]['eye_color'] = eye_color
    bot.set_state(message.from_user.id, MyStates.hobby, message.chat.id)
    bot.send_message(message.chat.id, f"Отлично!\nТеперь напиши своё хобби.")

# Обработчик для состояния hobby
@bot.message_handler(state=MyStates.hobby)
def get_hobby(message: types.Message):
    hobby = message.text
    state_storage[message.chat.id]['hobby'] = hobby
    data = state_storage[message.chat.id]
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, f"Вот всё что я запомнил:\nТебя зовут {data['name']}\n"
                                      "Твой цвет глаз {data['eye_color']}\nТвое хобби {data['hobby']}")

# Добавляем фильтр состояний
bot.add_custom_filter(StateFilter(bot))

# Запуск бота
bot.infinity_polling()