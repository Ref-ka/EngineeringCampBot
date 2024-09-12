
from sys import argv
from time import sleep
from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener

class BotsCommands:
    def __init__(self, bot: Bot):
        self.bot = bot

    def greet(self, message):  # команда /привет
        self.bot.send_message(message.chat.id, "Привет, пользователь!")

    def goodbye(self, message):  # команда /пока
        self.bot.send_message(message.chat.id, "Пока, до свидания!")

class MessageListener(Listener):
    def __init__(self, bot):
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

