import sqlite3
'''
Класс для таблиц
1. add_row() - добавление записи (строка). Аргументов не принимает.
2. remove_row() - удаление записи (строка). Аргументов не принимает.
3. edit_row() - редактирование записи (строка). Аргументов не принимает.
4. show_single_row() - Функция, которая полностью отображает данные одной конкретной записи (строки).
                           Требует аргумент key_value - значение ключевого столбца в строке.
5. show_all_rows() - Функция, которая отображает все записи (строки) в таблице. Записи ограничены в 20 символов.
                         Аргументов не принимает.
6. get_key_column() - Функция, которая передает название ключевого столбца в таблице.
                          Аргументов не принимает.
7. get_key_value() - Функция, которая передает значение в ключевом столбце.
                         Аргументов не принимает.
8. get_list_of_columns() - Функция, которая передает список стобцов в таблице.
                               Аргументов не принимает.
'''
class Table:
    def __init__(self, name, database):
        self.name = name
        self.database = database
        self.db = database.db
        self.cur = database.cur
        self.list_of_columns = self.get_list_of_columns()
        self.key_column = self.get_key_column()


    def add_row(self, list_of_values=None):

            if list_of_values == None:
                # Получение значения ключевого столбца
                key_value = self.get_key_value()

            else:
                key_value = list_of_values[0]

            # Запись новой строки с отслеживанием возможных ошибок
            try:
                # Внесение в активную таблицу () в ключевой столбец (key_column) введенного пользователем значения (key_value)
                self.cur.execute(f'INSERT INTO {self.name}("{self.key_column}") VALUES("{key_value}")')
                self.db.commit()
    
            # В случае, если такое значение первичного ключа уже существует, сработает данное исключение. Строка добавлена не будет
            # Работа функции будет завершена
            except sqlite3.IntegrityError:
                print('Запись с таким первичным ключом уже существует!')
                return
    
            # В случае других возможных ошибок сработает данное исключение. Строка добавлена не будет
            # Работа функции будет завершена
            except sqlite3.OperationalError:
                print("Не удалось ввести значение!")
    
                return
    
            # Если строка была успешно создана, запустится процесс её заполнения, в случае если количество столбцов > 1
            if len(self.list_of_columns) > 1:
    
                # Заполнение будет происходить без учета ключевого столбца
                for i in range(1, len(self.list_of_columns)):
                    # Для каждого столбца будет запрашиваться значение
                    column_name = self.list_of_columns[i][1]
                    new_value = input(f'\nВведите значение для столбца "{column_name}": ')
    
                    # Обновление таблицы, при котором вносятся введенные значения
                    self.cur.execute(
                        f'UPDATE {self.name} SET "{column_name}"="{new_value}" WHERE "{self.key_column}" == "{key_value}"')
                    self.db.commit()
    
            print('\nЗапись успешно добавлена!\n')

    def remove_row(self):

        # Отобажение списка всех строк
        self.show_all_rows()

        # Получение значения ключевого столбца
        key_value = self.get_key_value()

        # Удаление происходит с отслеживанием каких-либо ошибок
        try:
            # Удаление из активной таблицы () строки,
            # В которой ключевое значение (key_column) соответствует введенному пользователем (key_value)
            self.cur.execute(f'DELETE FROM {self.name} WHERE "{self.key_column}" = "{key_value}"')
            self.db.commit()
            print('Запись удалена!')

        # Исключение, которое сработает на любую ошибку
        except:
            print('Возникла ошибка!')

    def edit_row(self):

        # Отобажение списка всех строк
        self.show_all_rows()

        # Получение значения ключевого столбца
        key_value = self.get_key_value()

        # Полный вывод строки, которую необходимо отредактировать
        # Столбцы пронумерованы
        self.show_single_row(key_value)

        # Попытка редактирования строки в отслеживанием каких-либо ошибок
        try:
            # Получение номера столбца, который необходимо отредактировать
            column_to_edit = int(input('Введи номер столбца, который необходимо отредактировать: '))
            # Получение значения, которое будет внесено в выбранный ранее столбец
            new_value = input('Введите новое значение: ')

            ''' 
            Обновление таблицы, при котором в строке, у которой значение из ключевого столбца(key_column) равно введенному пользователем (key_value)
            Будет изменен столбец, номер которого (column_to_edit) был выбран пользователем.
            Номер (column_to_edit), уменьшенный на 1 (из-за разной нумерации) является индексом для списка столбцов (list_of_columns)
            '''
            self.cur.execute(
                f'UPDATE {self.name} SET "{self.list_of_columns[column_to_edit - 1][1]}" = "{new_value}" WHERE "{self.key_column}" = "{key_value}"')
            self.db.commit()
            print('Значение успешно изменено!')

            # Полный вывод отредактированной строки
            self.show_single_row(key_value)

        except:
            print('Введено неверное значение')

    def show_single_row(self, key_value):

        # Получение всех значений из строки, значение ключевого столбца (key_column) соответствует введенному пользователем (key_value)
        list_of_values = self.cur.execute(
            f'SELECT * FROM {self.name} WHERE "{self.key_column}" == "{key_value}"').fetchone()
        # Вывод списка с отслеживанием ошибок
        try:
            # Выводится пронумерованный список, отсчет начинается с 1
            for i in range(len(list_of_values)):
                # Вывод в формате: <Номер>. <Название строки>: <Содержимое строки>
                print(f'\n{i + 1}. {self.list_of_columns[i][1]}: {list_of_values[i]}\n')

        except:
            print('Возникла ошибка!')

    def show_all_rows(self):

        # Вывод название активной таблицы
        print(f'\nТаблица: {self.name}\n')

        # Получения списка всех значений из активной таблицы
        all_rows = self.cur.execute(f'SELECT * FROM {self.name}').fetchall()

        # Функция форматирования вывода таблицы
        def make_formatting(column):
            if len(str(column)) > 23:
                column = str(column)[:20] + '...'
            elif 23 == len(str(column)):
                column = str(column) + ''
            elif 23 > len(str(column)) >= 15:
                column = str(column) + '\t'
            elif 15 > len(str(column)) >= 7:
                column = str(column) + '\t\t'
            elif 7 > len(str(column)) >= 4:
                column = str(column) + '\t\t\t'
            elif 4 > len(str(column)) >= 1:
                column = str(column) + '\t\t\t'
            elif len(str(column)) == 0:
                column = str(column) + '\t\t\t\t'

            print(f'{column}', end='|')

        # Для каждого столбца из списка столбцов (list_of_columns) производится форматирование и вывод
        for column in self.list_of_columns:
            make_formatting(column[1])

            # Для каждой строки из списка всех строк (all_rows) производится форматирование и вывод
        for row in all_rows:
            print('\n')
            for column in row:
                make_formatting(column)

        print('\n')

    def get_key_column(self):
        # Название ключевого столбца является первое значение (название) из нулевого элемента списка (информация о ключевом столбце)
        return self.list_of_columns[0][1]

    def get_key_value(self):
        # Получение нужного значения из ключевого столбца
        return input(f'Введите "{self.key_column}" нужной записи: ')

    # Получение списка столбцов активной таблицы
    def get_list_of_columns(self):
        return list(self.cur.execute(f'PRAGMA table_info({self.name})').fetchall())

    def choose_action(self):
        action = True
        # Цикл работает, пока значение переменной действия (action) не равно 0
        while action != False:
            # У пользователя запрашивается номер пункта, который является целым числом
            try:
                action = int(input(f'\nТекущая таблица - {self.name}\n'
                                   'Выберите действие:\n'
                                   '\t1. Добавить запись\n'
                                   '\t2. Удалить запись\n'
                                   '\t3. Изменить запись\n'
                                   '\t4. Показать одну запись\n'
                                   '\t5. Показать все записи\n'
                                   '\t6. Сменить таблицу\n'
                                   '\t0. Назад\n'))

            # Если пользователь введет не целое число, сработает исключение и цикл сработает заново
            except:
                print('Введено неверное значение! table')

            if action == 1:
                self.add_row()

            elif action == 2:
                self.remove_row()

            elif action == 3:
                self.edit_row()

            elif action == 4:
                self.show_all_rows()
                key_value = self.get_key_value()
                self.show_single_row(key_value)

            elif action == 5:
                self.show_all_rows()

            elif action == 6:
                self.database.choose_table()

            elif action == 0:
                pass
