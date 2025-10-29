# src/primitive_db/engine.py

# надо подключить в зависимости командой poetry add prompt 
import prompt 

def run():
    '''
    Загружайте актуальные метаданные с помощью load_metadata.
    Запрашивайте ввод у пользователя.
    Разбирайте введенную строку на команду и аргументы.
    Подсказка: Для надежного разбора строки используйте библиотеку shlex. args = shlex.split(user_input).
    Используйте if/elif/else или match/case для вызова соответствующей функции из core.py.
    После каждой успешной операции (create_table, drop_table) сохраняйте измененные метаданные с помощью save_metadata.
    '''
    while True:
        print('Первая попытка запустить проект!\n *** \n')
        print(' <command> exit - выйти из программы\n <command> help - справочная информация\n')
        command = prompt.string('Введите команду:')

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")