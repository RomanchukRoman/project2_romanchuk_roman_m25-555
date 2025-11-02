# src/primitive_db/utils.py
import json

def load_metadata(filepath):
    '''
    Загружает данные из JSON-файла. Если файл не найден, возвращает пустой словарь {}. 
    Используйте try...except FileNotFoundError.
    '''
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError):
        return {}

def save_metadata(filepath, data):
    '''
    Сохраняет переданные данные в JSON-файл.
    '''
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)