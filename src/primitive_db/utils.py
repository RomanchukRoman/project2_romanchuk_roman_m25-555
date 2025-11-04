# src/primitive_db/utils.py
import json

from .constants import METADATA_FILE, get_table_data_path

def load_metadata(filepath = METADATA_FILE):
    '''
    Загружает данные из JSON-файла. Если файл не найден, возвращает пустой словарь {}. 
    '''
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError):
        return {}

def save_metadata(data, filepath = METADATA_FILE):
    '''
    Сохраняет переданные данные в JSON-файл.
    '''
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_table_data(table_name):
    """
    Загружает данные таблицы из JSON-файла
    """
    filepath = get_table_data_path(table_name)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_table_data(table_name, data):
    """
    Сохраняет данные таблицы в JSON-файл
    """
    filepath = get_table_data_path(table_name)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, default=str)