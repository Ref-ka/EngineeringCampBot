from sys import argv
from time import sleep

from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener


class BotsCommands:
    def __init__(
        self, bot: Bot
    ):  # Здесь вы можете иницилазировать свою полезную нагрузку
        self.bot = bot

    def start(self, message):  # действия на команду /start
        self.bot.send_message(message.chat.id, "Hello user!\nThis is an example bot.")

    def echo(self, message, value: str):  # команда /echo [значение: str]
        # повторяет за пользователем сообщение
        self.bot.send_message(message.chat.id, value)

    def add(
        self, message, a: float, b: float
    ):  # команда сложения чисел, выводит сумму /add [a: float] [b: float]
        self.bot.send_message(message.chat.id, str(a + b))

    def _not_a_command(self):  # Не команда, недоступна из чата Телеграмм
        print("I am not a command")

    # Как видно выше, в зависимости от того, как вы назовете функцию,
    # так она и будет вызываться из чата Телеграмм.


class MessageListener(Listener):
    def __init__(self, bot):
        self.bot = bot
        self.m_count = 0

    def on_message(self, message):  # Вызывается при любом сообщении
        # Простой учет количества сообщений
        self.m_count += 1
        print(f"Всего сообщений: {self.m_count}")

    def on_command_failure(
        self, message, err=None
    ):  # Вызывается, когда команда вызывает ошибку
        if err is None:
            self.bot.send_message(
                message.chat.id, "Провал при привязке аргументов к команде!"
            )
        else:
            self.bot.send_message(message.chat.id, f"Ошибка в команде:\n{err}")


if __name__ == "__main__":
    token = argv[1] if len(argv) > 1 else input("Введите токен ТГ-бота: ")
    bot = Bot(token)  # Создает сущность OrigamiBot

    # Добавить события к прослушке
    bot.add_listener(MessageListener(bot))

    # Добавить команды
    bot.add_commands(BotsCommands(bot))

    # Можно добавлять сколько угодно команд
    # как и прослушек событий

    bot.start()  # запускаем бота
    while True:
        sleep(1)
        # Здесь также можно выполнять полезную работу
        # Например, автопостить сообщения
