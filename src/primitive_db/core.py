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
    for table in metadata:
        if table == table_name:
            print('Такая таблица уже существует')
        else:
            print(table)
            columns['ID'] = 'int'
            print(columns)

def drop_table(metadata, table_name):
    '''
    Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
    Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    '''
    pass

# Проверка create_table
metadata = {
    "table_1": 
    {"column_1": "int", "column_2": "str"}, 
    "table_2": 
    {"column_1": "int", "column_2": "bool"}
}
columns = {"column_1": "bool", "column_2": "int"}

create_table(metadata, 'table_3', columns)