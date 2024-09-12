from sys import argv
from time import sleep
import sqlite3
from typing import Dict, List

from origamibot import OrigamiBot as Bot
from origamibot.listener import Listener

# Определение FSM
fsm = {
    'initial': 'q0',
    'accepting': ['q3'],
    'transitions': {
        'q0': {'answer': 'q1'},
        'q1': {'answer': 'q2'},
        'q2': {'answer': 'q3'},
        'q3': {}
    }
}

class BotsCommands:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.database = 'user_data.db'
        self.create_table()
        self.user_states = {}  # Хранение текущих состояний пользователей
        self.questions = [
            ("Какой у вас цвет глаз?", "eye_color"),
            ("Какой у вас цвет волос?", "hair_color"),
            ("Какой ваш любимый цвет?", "favorite_color"),
            ("Какое ваше любимое число?", "favorite_number")
        ]

    def create_table(self):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY,
                                eye_color TEXT,
                                hair_color TEXT,
                                favorite_color TEXT,
                                favorite_number INTEGER
                            )''')
            conn.commit()

    def start(self, message):  # действия на команду /start
        self.bot.send_message(message.chat.id, "Привет! Давайте соберем информацию о вас.")
        self.user_states[message.from_user.id] = fsm['initial']  # Устанавливаем начальное состояние
        self.ask_question(message)

    def ask_question(self, message):
        user_id = message.from_user.id
        current_state = self.user_states.get(user_id)

        if current_state == 'q0':
            question_text, column_name = self.questions[0]
            self.bot.send_message(message.chat.id, question_text)
            self.user_states[user_id] = 'q1'
            self.bot.add_listener(AnswerListener(self.bot, message, column_name, user_id))
        elif current_state == 'q1':
            question_text, column_name = self.questions[1]
            self.bot.send_message(message.chat.id, question_text)
            self.user_states[user_id] = 'q2'
            self.bot.add_listener(AnswerListener(self.bot, message, column_name, user_id))
        elif current_state == 'q2':
            question_text, column_name = self.questions[2]
            self.bot.send_message(message.chat.id, question_text)
            self.user_states[user_id] = 'q3'
            self.bot.add_listener(AnswerListener(self.bot, message, column_name, user_id))
        elif current_state == 'q3':
            question_text, column_name = self.questions[3]
            self.bot.send_message(message.chat.id, question_text)
            self.user_states[user_id] = 'q4'
            self.bot.add_listener(AnswerListener(self.bot, message, column_name, user_id))

    def save_user_data(self, message, user_data: Dict):
        insert(self.database, 'users', user_data)
        self.bot.send_message(message.chat.id, "Ваши данные сохранены!")

    def get_user_data(self, message):
        user_data = fetchall(self.database, 'users', ['*'], f'user_id = {message.from_user.id}')
        if user_data:
            user_info = user_data[0]
            response = (f"Цвет глаз: {user_info['eye_color']}\n"
                        f"Цвет волос: {user_info['hair_color']}\n"
                        f"Любимый цвет: {user_info['favorite_color']}\n"
                        f"Любимое число: {user_info['favorite_number']}")
            self.bot.send_message(message.chat.id, response)
        else:
            self.bot.send_message(message.chat.id, "Информация о вас не найдена.")

class AnswerListener(Listener):
    def __init__(self, bot, message, column_name, user_id):
        self.bot = bot
        self.message = message
        self.column_name = column_name
        self.user_id = user_id
        self.user_data = {'user_id': user_id}

    def on_message(self, message):
        self.user_data[self.column_name] = message.text
        bots_commands = BotsCommands(self.bot)
        bots_commands.save_user_data(self.message, self.user_data)
        bots_commands.ask_question(self.message)

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

