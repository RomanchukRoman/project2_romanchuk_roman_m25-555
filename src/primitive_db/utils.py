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
            return data
    except (FileNotFoundError):
        return {}



def save_metadata(filepath, data):
    '''
    Сохраняет переданные данные в JSON-файл.
    '''
    with open(filepath, 'w') as file:
        json.dump(data, file)

''' 
#Проверка
filepath = 'src/primitive_db/db_meta.json'
data = {"table_2": {"column_3": "value_3"}}

load_metadata(filepath)
save_metadata(filepath, data) # сейчас функция переписывает все данные! нужно научить переписывать по ключам
load_metadata(filepath)
'''