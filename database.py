from table import Table
import sqlite3 as sq

'''
Класс Database создан для взаимодействия с базами данных.
Методы:
1. disconnect() - отключение от БД. Не принимает аргументы.
2. show_tables() - вывод список имеющихся в БД таблиц. Не принимает аргументы.
3. add_table() - добавление таблицы. Не принимает аргументы.
4. remove_table() - удаление таблицы. Не принимает аругменты
5. choose_table() - переключение между имеющимися в БД таблицами. Не принимает аргументы.
6. get_name_of_table() - получение названия таблицы. Не принимает аргументы.
7. get_name_of_column() - получение названия столбца. Не принимает аргументы.
8. add_column() - добавить столбец. Не принимает аргументы.
'''
class Database:
    def __init__(self, path):
        self.path = path
        self.name = self.path.split('/')[-1].split('.')[0]
        self.db = sq.connect(self.path)
        self.cur = self.db.cursor()

    def disconnect(self):
        self.db.close()

    def show_tables(self):
        print('\n № |\tНазвание\t|\tЗапрос')
        # При помощи курсора делает запрос к БД, в частности к sqlite_master
        # Тип данных "таблица" (type = "table")
        tables = self.cur.execute(f'SELECT * FROM sqlite_master WHERE type ="table"').fetchall()

        # Вывод названия и запроса каждой таблицы
        for index, table in enumerate(tables):  # 2
            table_name = table[1]
            table_request = table[4]
            table_number = index + 1

            if len(table_name) < 4:
                table_name += '\t\t'

            elif len(table_name) < 12:
                table_name += '\t'

            print(f' {table_number} |  {table_name}\t|  {table_request}')

        return tables

    def add_table(self):
        name_of_new_table = self.get_name_of_table()
        name_of_key_column = self.get_name_of_column()
        key_column_args = self.add_column()

        type_of_column = key_column_args[0]
        add_autoincrement = key_column_args[1]

        # Создание новой таблицы с полученными значениями.
        # В случае существования таблицы с таким названием, пользователю будет выведено сообщение
        try:

            self.cur.execute(
                f'''CREATE TABLE {name_of_new_table} ({name_of_key_column} {type_of_column} PRIMARY KEY{add_autoincrement})''')
            self.db.commit()
            print('\nТаблица успешно создана!\n')
            self.show_tables()

        except:

            print('Такая таблица уже существует!')

    def remove_table(self):
        # Вызов функции отображения всех таблиц
        self.show_tables()

        # Получение от пользователя названия таблицы для удаления
        name_of_table = self.get_name_of_table()

        # Проверка на наличие таблицы, в случае отсуствия таблицы с введенным названием, появится предупреждение
        try:
            self.cur.execute(f'DROP TABLE "{name_of_table}"')
            self.db.commit()
        except:
            print('Такой таблицы не существует!')

        # Вызов функции отображения всех таблиц
        self.show_tables()

    def choose_table(self):
        # Отобажение пронумерованного списка всех таблиц
        tables = self.show_tables()

        # Получения значения номера таблицы, принимается только целочисленное значение
        # Если пользователь введет не целочисленное значение, сработает исключение
        try:
            active_table = int(input('\nВведите номер таблицы: '))

        except:
            print('Введено неверное значение!')

        # 0 является значением для выхода, поэтому условие ограничено неравенством с нулем
        # Также, значение должно быть только положительным
        if active_table > 0:
            # Из введенного пользователем номера вычитается 1, т.к. список значений нумеруется с нуля,
            # А выведенный пользователю список пронумерован с 1
            table_name = tables[active_table - 1][1]

            self.table = Table(table_name, self)
            self.table.choose_action()

        # Если значение не соответствует условию, то ничего не происходит
        else:
            pass

    def get_name_of_table(self):
        return input('\nВведите название таблицы: ')

    def get_name_of_column(self):
        return input('\nВведите название основного столбца: ')

    def add_column(self):

        type_of_column = int(input('Выберите тип данных столбца: \n'
                                   '\t1. Text\n'
                                   '\t2. Integer\n'
                                   '\t3. Real\n'
                                   '\t4. Time\n'))

        add_autoincrement = ''

        if type_of_column == 1:
            type_of_column = 'TEXT'
            print(f'\nВыставлен тип данных {type_of_column}\n')

        elif type_of_column == 2:
            type_of_column = 'INTEGER'
            print(f'\nВыставлен тип данных {type_of_column}\n')
            add_autoincrement = int(input('Добавить автоматическое заполнение?\n1. Да\n2. Нет\n'))

            if add_autoincrement == 1:
                add_autoincrement = ' AUTOINCREMENT'
                print('Добавлено автоматическое заполнение.\n')

            elif add_autoincrement == 2:
                add_autoincrement = ''
                print('Автоматическое заполнение отключено.\n')

            else:
                add_autoincrement = ''
                print('Введено неправильное значение. Автомтическое заполнение отключено.\n')

        elif type_of_column == 3:
            type_of_column = 'REAL'
            print(f'\nВыставлен тип данных {type_of_column}\n')

        elif type_of_column == 4:
            type_of_column = 'TIME'
            print(f'\nВыставлен тип данных {type_of_column}\n')

        else:
            print('Неизвестный формат!')
            type_of_column = 'TEXT'

        return type_of_column, add_autoincrement

    def choose_action(self):
        action = True
        while action != 0:

            # Введенное пользователем значение переводится в целочисленное. Иные значения засчитаны не будут.
            try:
                action = int(input('\nВыберите действие:\n'
                                   '\t1. Список таблиц\n'
                                   '\t2. Добавить таблицу\n'
                                   '\t3. Удалить таблицу\n'
                                   '\t4. Редактировать таблицу\n'
                                   '\t0. Назад\n'))

            except:
                print('Неверное значение!')

            # При вводе пользователем цифры 1, запускается функция show_tables, отображающая список таблиц
            if action == 1:
                self.show_tables()

            # При вводе пользователем цифры 2, запускается функция add_table, позволяющая добавить таблицу
            if action == 2:
                self.add_table()

            # При вводе пользователем цифры 3, запускается функция remove_table, позволяющая удалить таблицу
            if action == 3:
                self.remove_table()

            # При вводе пользователем цифры 4, отображается список таблиц
            # Затем запрашивается номер таблицы из списка для редактирования
            # Введенное число передается в функцию edit_table, позволяющий редактировать таблицу
            if action == 4:
                tables = self.show_tables()

                number_of_table = int(input('Введите номер таблицы: '))
                name_of_table = tables[number_of_table - 1][1]
                self.edit_table(name_of_table)