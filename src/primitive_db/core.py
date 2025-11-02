# src/primitive_db/core.py

def create_table(metadata, table_name, columns):
    '''
    Функция должна принимать текущие метаданные, имя таблицы и список столбцов.
    Автоматически добавлять столбец ID:int в начало списка столбцов.
    Проверять, не существует ли уже таблица с таким именем. Если да, выводить ошибку.
    Проверять корректность типов данных (только int, str, bool).
    В случае успеха, обновлять словарь metadata и возвращать его.
    '''
    # Проверки на наличие такой таблицы и типы данных
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует')

    allowed_types = {"int", "str", "bool"}
    parsed_columns = {}
    id_present = False

    for col in columns:
        if ":" not in col:
            raise ValueError(f'Некорректное значение: {col}. Попробуйте снова.')
        col_name, col_type_str = col.split(":", 1)
        col_name = col_name.strip()
        col_type_str = col_type_str.strip()
        if col_type_str not in allowed_types:
            raise TypeError(f'Тип данных может быть только: int, str, bool (ошибка в {col})')
        parsed_columns[col_name] = col_type_str
        if col_name.lower() == "id":
            id_present = True

    if not id_present:
        parsed_columns = {"id": "int", **parsed_columns}

    metadata[table_name] = parsed_columns
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(metadata[table_name].keys())}')
    return metadata

def drop_table(metadata, table_name):
    '''
    Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
    Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    '''
    # Проверки на наличие такой таблицы
    if table_name not in metadata:
        raise ValueError(f'Таблицы "{table_name}" не существует')

    metadata.pop(table_name)
    return metadata