# src/primitive_db/engine.py
import prompt
import shlex
from .utils import load_metadata, save_metadata
from .core import create_table, drop_table, list_tables
from .constants import METADATA_FILE, get_table_data_path

def run():
    '''
    Загружайте актуальные метаданные с помощью load_metadata.
    Запрашивайте ввод у пользователя.
    Разбирайте введенную строку на команду и аргументы.
    Подсказка: Для надежного разбора строки используйте библиотеку shlex. args = shlex.split(user_input).
    Используйте if/elif/else или match/case для вызова соответствующей функции из core.py.
    После каждой успешной операции (create_table, drop_table) сохраняйте измененные метаданные с помощью save_metadata.
    '''
    print('\n***База данных***')
    print('\nФункции:\n<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу\n<command> list_tables - показать список всех таблиц\n<command> drop_table <имя_таблицы> - удалить таблицу\n<command> exit - выход из программы\n<command> help - справочная информация')
   
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
                case 'exit':
                    print('\nВыход из программы')
                    break
                case 'help':
                    print_help()
        except Exception as e:
            print(f'Ошибка: {e}. Попробуйте снова.')

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