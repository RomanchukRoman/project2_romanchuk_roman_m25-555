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
    with open(filepath, 'w') as file:
        json.dump(data, file)

''' Проверка
filepath = 'src/primitive_db/db_meta.json'
data = {"table_name": "table_2"}

load_metadata(filepath)
save_metadata(filepath, data)
load_metadata(filepath)
'''