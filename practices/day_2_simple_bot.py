import telebot


API_TOKEN = 'YOUR_API_TOKEN'


# Создаем сущность нашего бота
bot = telebot.TeleBot(API_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def do_on_start(message):
   bot.reply_to(message, "Добро пожаловать в дружелюбного бота.")


# Запуск бота.
bot.infinity_polling()
