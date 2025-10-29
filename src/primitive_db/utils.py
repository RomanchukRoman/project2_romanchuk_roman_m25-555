# src/primitive_db/utils.py
import json

def load_metadata(filepath):
    '''
    Загружает данные из JSON-файла. Если файл не найден, возвращает пустой словарь {}. 
    Используйте try...except FileNotFoundError.
    '''
    try:
        with open(filepath) as file:
            data = json.load(file)
            print(data) # тут изменить на return
    except (FileNotFoundError):
        print({}) # тут изменить на return



def save_metadata(filepath, data):
    '''
    Сохраняет переданные данные в JSON-файл.
    '''
    pass

load_metadata('src/primitive_db/db_meta.json')