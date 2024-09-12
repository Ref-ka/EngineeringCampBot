
from sys import argv
from time import sleep
from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener

class BotsCommands:
    def init(self, bot: Bot):
        self.bot = bot

    def start(self, message):  # команда /start
        user_first_name = message.from_user.first_name  # Получаем имя пользователя
        self.bot.send_message(message.chat.id, f"Привет, {user_first_name}!\nЭто пример бота.")

    def greet(self, message):  # команда /greet
        user_first_name = message.from_user.first_name
        self.bot.send_message(message.chat.id, f"Привет, {user_first_name}!")

    def goodbye(self, message):  # команда /goodbye
        user_first_name = message.from_user.first_name
        self.bot.send_message(message.chat.id, f"Пока, {user_first_name}, до свидания!")

class MessageListener(Listener):
    def init(self, bot):
        self.bot = bot

    def on_message(self, message):
        print(f"Получено сообщение: {message.text}")

    def on_command_failure(self, message, err=None):
        if err is None:
            self.bot.send_message(message.chat.id, "Ошибка при выполнении команды!")
        else:
            self.bot.send_message(message.chat.id, f"Ошибка в команде:\n{err}")

if __name__ == "__main__":
    token = argv[1] if len(argv) > 1 else input("Введите токен ТГ-бота: ")
    bot = Bot(token)

    # Добавить события к прослушке
    bot.add_listener(MessageListener(bot))

    # Добавить команды
    bot.add_commands(BotsCommands(bot))

    bot.start()  # запускаем бота
    while True:
        sleep(1)

