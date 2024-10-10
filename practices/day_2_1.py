import telebot

# Не забудьте заменить 'YOUR_API_TOKEN'
#     на токен вашего бота, который вы получили от BotFather
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

# Создаем сущность нашего бота
bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def do_on_start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я ваш дружелюбный бот. Для взаимодействия используйте команды /start или /bye.")

# Обработчик команды /greet
@bot.message_handler(commands=['greet'])
def do_on_greet(message):
    bot.reply_to(message, 'Добро пожаловать в дружелюбного бота. Рад вас видеть! Чем я могу быть вам сегодня полезен?')

# Обработчик команды /bye
@bot.message_handler(commands=['bye'])
def do_on_goodbye(message):
    bot.reply_to(message, "До свидания! Надеюсь, скоро увидимся снова.")

# Обработчик всех текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    bot.reply_to(message, "Извините, я вас не понял. Попробуйте использовать команды /greet или /bye.")

# Запуск бота.
# Выполняйте эту инструкцию самой последней!
bot.infinity_polling()
