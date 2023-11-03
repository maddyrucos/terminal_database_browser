from subprocess import check_output
import os
# Данная функция будет переделана
def add_db():

    action = True
    while action:
        output = list((check_output(args =['ls'], encoding='UTF8')).split('\n'))
        for index, el in enumerate(output[:-1]):
            print(f'{index+1}. {el}')

        try:
            action = int(input(f'0. Назад\n'
                           f'Для выхода напишите exit\n'
                           f'Выберите директорию или файл: '))
        except:
            return 0

        if action == 0:
            os.chdir('..')
            action = True

        else:
            name = output[action-1]
            try:
                os.chdir(f'{name}')

            except NotADirectoryError:
                path = f'{os.getcwd()}/{name}'
                return name, path


def create_db():
    action = True
    while action:
        output = list((check_output(args=['ls'], encoding='UTF8')).split('\n'))
        for index, el in enumerate(output[:-1]):
            print(f'{index + 1}. {el}')


        action = input( f'0. Назад\n'
                        f'Для создания базы данных в каталоге "{os.getcwd()}" введите название новой'
                        f'базы данных (кроме exit)\n'
                        f'Для выхода напишите exit\n'
                        f'Выберите директорию или файл: ')

        print(action)
        if type(action) == int:
            if action == 0:
                os.chdir('..')
                action = True

            else:
                name = output[action - 1]
                try:
                    os.chdir(f'{name}')

                except NotADirectoryError:
                    print('Это не директория!')

        else:
            if action != 'exit':
                return action, f'{os.getcwd()}/{action}.db'

            else:
                return 0

if __name__ == '__main__':
    add_db()
    create_db()