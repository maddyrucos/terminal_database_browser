import navigation

from database import Database
from dbcontainer import Container

import os
class App:
    def __init__(self):
        self.main_db = Container(f'{os.getcwd()}/db.db')
        print('\n\tWelcome to the Terminal DB-browser!\n')
    def loopback(self):
        while True:
            self.choose_db()

    def choose_db(self):
        formated_data = self.main_db.format_data()
        try:
            startup = int(input(f'{formated_data[1]}\nВыберите действие: '))
        except:
            print('Завершение работы...')

        if startup >= len(formated_data[0]):
            if startup == len(formated_data[0]):
                name, path = navigation.add_db()
            else:
                name, path = navigation.create_db()
            self.main_db.add_db_to_db(name, path)
        else:
            path = formated_data[0][startup]
        self.database = Database(path)
        self.choose_action()

    def choose_action(self):
        action = True

        # Цикл выбора действия. Работает, пока пользователь не введет 0 (кнопка выхода)
        while action:

            # Введенное пользователем значение переводится в целочисленное. Иные значения засчитаны не будут.
            try:
                action = int(input('\nВыберите действие:\n'
                                   '\t1. Работа с данными\n'
                                   '\t2. Работа с таблицами\n'
                                   '\t0. Отключиться\n'))
            except:
                print('Неверное значение!')


            if action == 1:
                self.database.choose_table()

            elif action == 2:
                self.database.choose_action()

            # При вводе пользователем нуля, происходит отключение от БД
            elif action == 0:
                print(f'\n\tОтключение от {self.database.name}...\n')
                self.database.disconnect()

            # Условие, которое ограничивает допустимые целочисленные значения (от 0 до 2)
            else:
                print('Неверное значение!')

if __name__ == '__main__':
    app = App()
    app.loopback()