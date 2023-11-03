from database import Database

'''
Класс Container (в дальейшем "контейнер")является наследником класса Database. 
Данный класс нужен для управления БД, которая является хранилищем остальных БД.
При инициализации создает внутри себя таблицу с двумя столбцами: путь - ключевой (path), название (name). 
Сразу же добавляет себя в эту таблицу.
'''
class Container(Database):

    def __init__(self, path):
        super().__init__(path)
        self.cur.execute('CREATE TABLE IF NOT EXISTS db(path PRIMARY KEY ON CONFLICT REPLACE, name)')
        self.db.commit()
        self.add_db_to_db(self.name, self.path)

    # Функция для приведения текса к нужному формату
    def format_data(self):
        formated_string = ''
        formated_list = [0]
        list_of_dbs = self.cur.execute('SELECT name, path FROM db').fetchall()
        for index, db in enumerate(list_of_dbs):
            formated_string += (f'{index + 1}. {db[0]} - {db[1]}\n')
            formated_list.append(db[1])
        formated_string += (f'{len(list_of_dbs) + 1}. Добавить БД\n'
                            f'{len(list_of_dbs) + 2}. Создать БД\n')
        return formated_list, formated_string

    # Добавляет внутрь "контейнера" имя и путь БД
    def add_db_to_db(self, name, path):
        self.cur.execute(f'INSERT INTO db("name", "path") VALUES("{name}", "{path}")')
        self.db.commit()

    # Получение списка добавленных БД
    def get_list_of_dbs(self):
        return self.cur.execute('SELECT name, path FROM db').fetchall()

    # Создание новой БД с внесением её в "контейнер"
    def create_new_db(self, name, path):
        new_db = Database(path)
        new_db.disconnect()
        self.add_db_to_db(name, path)
