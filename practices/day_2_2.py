import telebot

# Замените 'YOUR_API_TOKEN' на токен вашего бота, 
# который вы получили от BotFather.
API_TOKEN = 'YOUR_API_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def do_on_start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я ваш дружелюбный бот. Для взаимодействия используйте команды /greet или /bye.")

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

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    username = message.from_user.first_name
    if username:
        bot.send_message(message.chat.id,
                         f"Извините, {username}, я вас не понял. Попробуйте использовать команды /greet или /bye.")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Попробуйте использовать команды /greet или /bye.")

# Запуск бота.
# Выполняйте эту инструкцию самой последней!
bot.infinity_polling()