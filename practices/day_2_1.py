import telebot

# Замените 'YOUR_API_TOKEN' на токен вашего бота, который вы получили от BotFather
API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш дружелюбный бот. Для взаимодействия используйте команды /start или /bye.")

# Обработчик команды /greet
@bot.message_handler(commands=['greet'])
def welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     'Добро пожаловать в дружелюбного бота. Рад вас видеть! Чем я могу быть вам сегодня полезен?')

# Обработчик команды /bye
@bot.message_handler(commands=['bye'])
def send_goodbye(message):
    bot.reply_to(message, "До свидания! Надеюсь, скоро увидимся снова.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Извините, я вас не понял. Попробуйте использовать команды /greet или /bye.")

# Запуск бота
bot.infinity_polling()
