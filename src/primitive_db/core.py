# src/primitive_db/core.py
from utils import load_metadata

def create_table(metadata, table_name, columns):
    '''
    Функция должна принимать текущие метаданные, имя таблицы и список столбцов.
    Автоматически добавлять столбец ID:int в начало списка столбцов.
    Проверять, не существует ли уже таблица с таким именем. Если да, выводить ошибку.
    Проверять корректность типов данных (только int, str, bool).
    В случае успеха, обновлять словарь metadata и возвращать его.
    '''
    # Проверки на наличие такой таблицы и типы данных
    for table in metadata:
        if table == table_name:
            raise ValueError("Такая таблица уже существует")
    for column in columns:
        if isinstance(columns[column], (int, str, bool)):
            raise TypeError("Тип данных может быть только int, str, bool")

    metadata[table_name] = {"ID": int}
    metadata[table_name].update(columns)
    print(metadata) # тут заменить на return и возможно перезаписать json

def drop_table(metadata, table_name):
    '''
    Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
    Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    '''
    flag_del = False
    # Проверки на наличие такой таблицы
    for table in metadata:
            if table == table_name:
                metadata.pop(table_name)
                flag_del = True
                break
    if not flag_del:
        raise ValueError("Такой таблицы не существует")
    print(metadata)
            
''' 
# Проверка create_table
filepath = 'src/primitive_db/db_meta.json'
metadata = load_metadata(filepath)
columns = {"column_1": bool, "column_2": int}
create_table(metadata, 'table_3', columns)
'''
''' 
# Проверка drop_table
filepath = 'src/primitive_db/db_meta.json'
metadata = load_metadata(filepath)
drop_table(metadata, 'table_1')
'''