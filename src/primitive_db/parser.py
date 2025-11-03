import shlex

def parse_where_clause(where_str):
    """
    Парсит условие WHERE в формате "столбец = значение"
    Возвращает словарь {column: value}
    """
    if not where_str:
        return None
    
    try:
        parts = shlex.split(where_str)
        if len(parts) != 3 or parts[1] != '=':
            raise ValueError(f"Некорректный формат условия WHERE: {where_str}")
        
        # Приводим имя столбца к нижнему регистру для единообразия
        column = parts[0].lower()
        value = parse_value(parts[2])
        
        return {column: value}
    except Exception as e:
        raise ValueError(f"Ошибка разбора условия WHERE: {e}")

def parse_set_clause(set_str):
    """
    Парсит условие SET в формате "столбец = значение"
    Возвращает словарь {column: value}
    """
    try:
        parts = shlex.split(set_str)
        if len(parts) != 3 or parts[1] != '=':
            raise ValueError(f"Некорректный формат условия SET: {set_str}")
        
        # Приводим имя столбца к нижнему регистру для единообразия
        column = parts[0].lower()
        value = parse_value(parts[2])
        
        return {column: value}
    except Exception as e:
        raise ValueError(f"Ошибка разбора условия SET: {e}")

def parse_value(value_str):
    """
    Парсит строковое значение в соответствующий тип данных.
    """
    value_str = value_str.strip()
    
    # Булевы значения (регистронезависимые)
    if value_str.lower() == 'true':
        return True
    elif value_str.lower() == 'false':
        return False
    
    # Числа
    try:
        return int(value_str)
    except ValueError:
        pass
    
    # Строки - shlex уже убрал кавычки, так что это строка
    return value_str

def parse_values(values_str):
    """
    Парсит значения в формате "(value1, value2, ...)"
    """
    values_str = values_str.strip()
    
    # Проверяем наличие скобок
    if not (values_str.startswith('(') and values_str.endswith(')')):
        raise ValueError('Значения должны быть заключены в скобки: (value1, value2, ...)')
    
    # Убираем внешние скобки
    values_str = values_str[1:-1].strip()
    
    # Если строка пустая после скобок
    if not values_str:
        return []
    
    try:
        # Используем shlex.split для корректного разбора значений
        values = shlex.split(values_str)
        
        # Парсим каждое значение
        parsed_values = []
        for value in values:
            # Убираем запятые если они остались
            if value.endswith(','):
                value = value[:-1].strip()
            if value:  # Игнорируем пустые значения
                parsed_values.append(parse_value(value))
        
        return parsed_values
        
    except Exception as e:
        raise ValueError(f"Ошибка разбора значений: {e}. Используйте формат: (\"строка\", число, true/false)")