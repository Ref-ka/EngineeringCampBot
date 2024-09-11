import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage

# Initialize the bot
state_storage = StateMemoryStorage()  # don't use this in production; switch to redis
bot = telebot.TeleBot("some token", state_storage=state_storage, use_class_middlewares=True)


# Define states
class MyStates(StatesGroup):
    name = State()
    age = State()
    color = State()
    hobby = State()


# Start command handler
@bot.message_handler(commands=["начать"])
def start_ex(message: types.Message, state: StateContext):
    state.set(MyStates.name)
    bot.send_message(
        message.chat.id,
        "Привет! Как тебя зовут?",
        reply_to_message_id=message.message_id,
    )


# Cancel command handler
@bot.message_handler(state="*", commands=["отмена"])
def any_state(message: types.Message, state: StateContext):
    state.delete()
    bot.send_message(
        message.chat.id,
        "Ваша информация была очищена. Напишите /начать, чтобы заполнить заново.",
        reply_to_message_id=message.message_id,
    )


# Handler for name input
@bot.message_handler(state=MyStates.name)
def name_get(message: types.Message, state: StateContext):
    state.set(MyStates.age)
    bot.send_message(
        message.chat.id, "Сколько тебе лет?", reply_to_message_id=message.message_id
    )
    state.add_data(name=message.text)


# Handler for age input
@bot.message_handler(state=MyStates.age, is_digit=True)
def ask_color(message: types.Message, state: StateContext):
    state.set(MyStates.color)
    state.add_data(age=message.text)

    # Define reply keyboard for color selection
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    colors = ["Красный", "Серый", "Синий", "Желтый", "Фиолетовый", "Оранжевый", "Другой"]
    buttons = [types.KeyboardButton(color) for color in colors]
    keyboard.add(*buttons)

    bot.send_message(
        message.chat.id,
        "Какой твой любимый цвет? Вибери из предоставленных вариантов",
        reply_markup=keyboard,
        reply_to_message_id=message.message_id,
    )


# Handler for color input
@bot.message_handler(state=MyStates.color)
def ask_hobby(message: types.Message, state: StateContext):
    state.set(MyStates.hobby)
    state.add_data(color=message.text)

    # Define reply keyboard for hobby selection
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    hobbies = ["Чтение", "Путешествия", "Игры", "Готовка"]
    buttons = [types.KeyboardButton(hobby) for hobby in hobbies]
    keyboard.add(*buttons)

    bot.send_message(
        message.chat.id,
        "Какое у тебя хобби? Выбери что-то одно.",
        reply_markup=keyboard,
        reply_to_message_id=message.message_id,
    )


# Handler for hobby input
@bot.message_handler(
    state=MyStates.hobby, text=["Чтение", "Путешествия", "Игры", "Готовка"]
)
def finish(message: types.Message, state: StateContext):
    with state.data() as data:
        name = data.get("name")
        age = data.get("age")
        color = data.get("color")
        hobby = message.text  # Get the hobby from the message text

        # Provide a fun fact based on color
        color_facts = {
            "Красный": "Красный часто ассоциируется с волнением и страстью.",
            "Зеленый": "Зеленый – цвет природы и спокойствия.",
            "Синий": "Синий известен своим успокаивающим и безмятежным действием.",
            "Желтый": "Желтый — жизнерадостный цвет, часто ассоциирующийся со счастьем.",
            "Фиолетовый": "Фиолетовый означает королевскую власть и роскошь.",
            "Оранжевый": "Оранжевый — яркий цвет, который стимулирует энтузиазм.",
            "Другой": "Цвета имеют различные значения в зависимости от контекста.",
        }
        color_fact = color_facts.get(
            color, "Цвета имеют разные значения, и ваше уникально!"
        )

        msg = (
            f"Спасибо, что поделились! Ваша информация: \n"
            f"Имя: {name}\n"
            f"Возраст: {age}\n"
            f"Любимый цвет: {color}\n"
            f"Интересный факт про ваш цвет: {color_fact}\n"
            f"Ваше хобби: {hobby}"
        )

    bot.send_message(
        message.chat.id, msg, parse_mode="html", reply_to_message_id=message.message_id
    )
    state.delete()


# Handler for incorrect age input
@bot.message_handler(state=MyStates.age, is_digit=False)
def age_incorrect(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Пожалуйста, введите верный возраст.",
        reply_to_message_id=message.message_id,
    )


# Add custom filters
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())

# necessary for state parameter in handlers.
from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))

# Start polling
bot.infinity_polling()