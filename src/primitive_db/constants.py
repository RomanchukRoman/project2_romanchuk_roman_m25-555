# Константы путей для базы данных
METADATA_FILE = 'src/primitive_db/data/db_meta.json' 
DATA_DIR = 'src/primitive_db/data/'

def get_table_data_path(table_name):
    """Возвращает полный путь к файлу данных таблицы"""
    return f"{DATA_DIR}{table_name}.json"