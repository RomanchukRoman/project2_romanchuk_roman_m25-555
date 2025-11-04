# src/primitive_db/core.py
from prettytable import PrettyTable
from .utils import load_table_data, save_table_data
from .parser import parse_values, parse_where_clause, parse_set_clause

def create_table(metadata, table_name, columns):
    '''
    Функция создания таблицы.
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
    Функция удаляющая таблицу, если она существует. 
    '''
    # Проверки на наличие такой таблицы
    if table_name not in metadata:
        raise ValueError(f'Таблицы "{table_name}" не существует')

    metadata.pop(table_name)
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata):
    '''
    Показать список всех таблиц
    '''
    if metadata != {}:
        for table in metadata:
            print(f'- {table}')
    else:
        print('Список таблиц пуст.')

# CRUD функции
def info_table(metadata, table_name):
    """
    Выводит информацию о таблице.
    """
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует')
    
    table_data = load_table_data(table_name)
    
    print(f"Таблица: {table_name}")
    columns_str = ", ".join([f"{col}:{typ}" for col, typ in metadata[table_name].items()])
    print(f"Столбцы: {columns_str}")
    
    # Подсчет записей
    record_count = len(table_data.get("records", []))
    print(f"Количество записей: {record_count}")

def insert(metadata, table_name, values_str):
    """
    Вставляет новую запись в таблицу.
    """
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует')
    
    values = parse_values(values_str)
    table_schema = metadata[table_name]
    columns = list(table_schema.keys())
    
    if len(values) != len(columns) - 1:
        raise ValueError(f'Неверное количество значений. Ожидается {len(columns)-1}, получено {len(values)}')
    
    table_data = load_table_data(table_name)
    
    # Инициализируем структуру данных если таблица пустая
    if not table_data:
        table_data = {"records": []}
    elif "records" not in table_data:
        table_data["records"] = []
    
    # Генерируем новый ID
    new_id = 1
    if table_data["records"]:
        ids = [record.get('id', 0) for record in table_data["records"]]
        new_id = max(ids) + 1
    
    # Создаем новую запись
    new_record = {'id': new_id}
    
    # Добавляем значения (пропускаем ID столбец)
    for i, column in enumerate(columns[1:], 0):
        value = values[i]
        expected_type = table_schema[column]
        
        # Валидация типов
        if not validate_type(value, expected_type):
            raise TypeError(f'Неверный тип для столбца {column}. Ожидается {expected_type}, получено {type(value).__name__}')
        
        new_record[column] = value
    
    # Добавляем запись и сохраняем
    table_data["records"].append(new_record)
    save_table_data(table_name, table_data)
    
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data

def select(metadata, table_name, where_str=None):
    """
    Выбирает записи из таблицы.
    """
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует')
    
    table_data = load_table_data(table_name)
    where_clause = parse_where_clause(where_str) if where_str else None
    
    # Проверяем наличие записей
    if not table_data or "records" not in table_data or not table_data["records"]:
        print("Записи не найдены.")
        return []
    
    records = table_data["records"]
    
    # Фильтруем данные
    if where_clause:
        filtered_data = []
        for record in records:
            match = True
            for column, value in where_clause.items():
                if record.get(column) != value:
                    match = False
                    break
            if match:
                filtered_data.append(record)
    else:
        filtered_data = records
    
    # Выводим результат
    if filtered_data:
        display_table(filtered_data, list(metadata[table_name].keys()))
    else:
        print("Записи не найдены.")
    
    return filtered_data

def update(metadata, table_name, set_str, where_str):
    """
    Обновляет записи в таблице.
    """
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует')
    
    set_clause = parse_set_clause(set_str)
    where_clause = parse_where_clause(where_str)
    
    table_data = load_table_data(table_name)
    table_schema = metadata[table_name]
    
    # Проверяем наличие записей
    if not table_data or "records" not in table_data:
        print('Записи для обновления не найдены.')
        return table_data
    
    updated_count = 0
    updated_ids = []
    
    # Обновляем записи
    for record in table_data["records"]:
        match = True
        for column, value in where_clause.items():
            if record.get(column) != value:
                match = False
                break
        
        if match:
            # Проверяем и обновляем значения
            for column, new_value in set_clause.items():
                if column not in table_schema:
                    raise ValueError(f'Столбец "{column}" не существует в таблице "{table_name}"')
                
                expected_type = table_schema[column]
                if not validate_type(new_value, expected_type):
                    raise TypeError(f'Неверный тип для столбца {column}. Ожидается {expected_type}, получено {type(new_value).__name__}')
                
                record[column] = new_value
            
            updated_count += 1
            updated_ids.append(record['id'])
    
    if updated_count > 0:
        save_table_data(table_name, table_data)
        print(f'Записи с ID={updated_ids} в таблице "{table_name}" успешно обновлены.')
    else:
        print('Записи для обновления не найдены.')
    
    return table_data

def delete(metadata, table_name, where_str):
    """
    Удаляет записи из таблицы.
    """
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует')
    
    where_clause = parse_where_clause(where_str)
    table_data = load_table_data(table_name)
    
    # Проверяем наличие записей
    if not table_data or "records" not in table_data:
        print('Записи для удаления не найдены.')
        return table_data
    
    records_to_keep = []
    deleted_ids = []
    
    # Фильтруем записи для удаления
    for record in table_data["records"]:
        match = True
        for column, value in where_clause.items():
            if record.get(column) != value:
                match = False
                break
        
        if match:
            deleted_ids.append(record['id'])
        else:
            records_to_keep.append(record)
    
    if deleted_ids:
        table_data["records"] = records_to_keep
        save_table_data(table_name, table_data)
        print(f'Записи с ID={deleted_ids} успешно удалены из таблицы "{table_name}".')
    else:
        print('Записи для удаления не найдены.')
    
    return table_data

# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def validate_type(value, expected_type):
    """
    Проверяет соответствие типа значения ожидаемому типу.
    """
    type_map = {
        'int': int,
        'str': str,
        'bool': bool
    }
    
    expected_python_type = type_map.get(expected_type)
    return isinstance(value, expected_python_type)

def display_table(data, columns):
    """
    Отображает данные в виде красивой таблицы.
    """
    table = PrettyTable()
    table.field_names = columns
    
    for record in data:
        row = [record.get(col, '') for col in columns]
        table.add_row(row)
    
    print(table)