# src/primitive_db/engine.py
import prompt
import shlex
from .utils import load_metadata, save_metadata
from .core import (
    create_table, drop_table, list_tables, 
    insert, select, update, delete, info_table 
)

def print_help():
    """Печатает справку по помощи."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию")
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись")
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    '''
    Основная функция управления командами базы данных.
    '''
    print('\n***База данных***')
    print_help()

    while True:
        try:
            metadata = load_metadata()
            commands = prompt.string('\nВведите команду:')
            args = shlex.split(commands)
            # Первое слово команда, далее аргументы
            command = args[0]
            table_name = args[1] if len(args) > 1 else None
            columns = args[2:] if len(args) > 2 else []

            match command:
                case 'create_table':
                        data = create_table(metadata, table_name, columns)
                        save_metadata(data)
                case 'list_tables':
                    list_tables(metadata)
                case 'drop_table':
                    data = drop_table(metadata, table_name)
                    save_metadata(data)
                case 'insert':
                    if len(args) < 5 or args[1].lower() != 'into' or args[3].lower() != 'values':
                        print("Ошибка: Неверный формат команды insert")
                        print("Использование: insert into <таблица> values (<значения>)")
                        continue
                    table_name = args[2]
                    values_str = ' '.join(args[4:])
                    insert(metadata, table_name, values_str) 
                case 'select':
                    if len(args) < 3 or args[1].lower() != 'from':
                        print("Ошибка: Неверный формат команды select")
                        print("Использование: select from <таблица> [where <условие>]")
                        continue
                    table_name = args[2]
                    where_str = ' '.join(args[4:]) if len(args) > 4 and args[3].lower() == 'where' else None
                    select(metadata, table_name, where_str)          
                case 'update':
                    if len(args) < 6:
                        print("Ошибка: Неверный формат команды update")
                        print("Использование: update <таблица> set <столбец>=<значение> where <условие>")
                        continue
                    
                    try:
                        # Приводим к нижнему регистру для поиска ключевых слов
                        args_lower = [arg.lower() for arg in args]
                        set_index = args_lower.index('set')
                        where_index = args_lower.index('where')
                    except ValueError:
                        print("Ошибка: Неверный формат команды update")
                        print("Использование: update <таблица> set <столбец>=<значение> where <условие>")
                        continue
                    
                    # Проверяем порядок
                    if not (1 < set_index < where_index < len(args) - 1):
                        print("Ошибка: Неверный формат команды update")
                        print("Использование: update <таблица> set <столбец>=<значение> where <условие>")
                        continue
                    
                    table_name = args[1]
                    set_str = ' '.join(args[set_index + 1:where_index])
                    where_str = ' '.join(args[where_index + 1:])
                    
                    update(metadata, table_name, set_str, where_str)             
                case 'delete':
                    if len(args) < 5:
                        print("Ошибка: Неверный формат команды delete")
                        print("Использование: delete from <таблица> where <условие>")
                        continue
                    
                    # Приводим к нижнему регистру для поиска ключевых слов
                    args_lower = [arg.lower() for arg in args]
                    if args_lower[1] != 'from' or args_lower[3] != 'where':
                        print("Ошибка: Неверный формат команды delete")
                        print("Использование: delete from <таблица> where <условие>")
                        continue
                    
                    table_name = args[2]
                    where_str = ' '.join(args[4:])
                    delete(metadata, table_name, where_str)                
                case 'info':
                    if len(args) < 2:
                        print("Ошибка: Недостаточно аргументов")
                        continue
                    info_table(metadata, args[1])
                case 'exit':
                    print('\nВыход из программы')
                    break
                case 'help':
                    print_help()
                case _:
                    print(f'Команды "{command}" не существует. Попробуйте снова или воспользуйтесь справкой (команда "help")')
        except Exception as e:
            print(f'Ошибка: {e}. Попробуйте снова.')