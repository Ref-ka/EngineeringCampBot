
from sys import argv
from time import sleep
import random
from datetime import datetime

from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener

class BotsCommands:
    def __init__(self, bot: Bot):
        self.bot = bot

    def start(self, message):  # действия на команду /start
        self.bot.send_message(message.chat.id, "Привет! Я бот. Используйте команды /time, /roll и /joke.")

    def echo(self, message, value: str):  # команда /echo [значение: str]
        self.bot.send_message(message.chat.id, value)

    def add(self, message, a: float, b: float):  # команда сложения чисел
        self.bot.send_message(message.chat.id, str(a + b))

    def time(self, message):  # команда для получения текущей даты и времени
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.bot.send_message(message.chat.id, f"Текущая дата и время: {current_time}")

    def roll(self, message):  # команда броска кубика
        result = random.randint(1, 6)
        self.bot.send_message(message.chat.id, f"Вы бросили кубик и получили: {result}")

    def joke(self, message):  # команда для отправки случайной шутки
        jokes = [
            "Почему программисты предпочитают тьму? Потому что свет притягивает жуков!",
            "Как программист называет свой компьютер? 'Своим личным сервером!'",
            "Почему у программистов нет друзей? Потому что они всегда все отлаживают!"
        ]
        self.bot.send_message(message.chat.id, random.choice(jokes))

    def _not_a_command(self):  # Не команда, недоступна из чата Телеграмм
        print("I am not a command")

class MessageListener(Listener):
    def __init__(self, bot):
        self.bot = bot
        self.m_count = 0

    def on_message(self, message):  # Вызывается при любом сообщении
        self.m_count += 1
        print(f"Всего сообщений: {self.m_count}")

    def on_command_failure(self, message, err=None):  # Вызывается, когда команда вызывает ошибку
        if err is None:
            self.bot.send_message(message.chat.id, "Провал при привязке аргументов к команде!")
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

