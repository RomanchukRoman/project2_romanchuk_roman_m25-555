
# Primitive Database

Простая реляционная база данных на Python с поддержкой CRUD-операций и персистентным хранением данных в JSON-формате.

## Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/RomanchukRoman/project2_romanchuk_roman_m25-555.git
cd project2_romanchuk_roman_m25-555

# Установите зависимости и пакет
make install
make build
make package-install
```

## Запуск

После установки выполните команду:
```bash
database
```

## Использование

### Команды управления таблицами

```sql
create_table users name:str age:int is_active:bool  # Создать таблицу
list_tables                                         # Показать список таблиц
drop_table users                                    # Удалить таблицу
info users                                          # Информация о таблице
```

### CRUD-операции

```sql
insert into users values ("Sergei", 28, true)       # Добавить запись
select from users                                   # Выбрать все записи
select from users where age = 28                    # Выбрать с условием
update users set age = 29 where name = "Sergei"     # Обновить запись
delete from users where id = 1                      # Удалить запись
```

### Общие команды

```bash
help    # Справка по командам
exit    # Выход из программы
```

## Демонстрация работы

[![asciicast](https://asciinema.org/a/Kms4q1SES5FitAUD5O9pZMeA9.svg)](https://asciinema.org/a/Kms4q1SES5FitAUD5O9pZMeA9)

## Структура проекта

```
project2_romanchuk_roman_m25-555/
├── src/primitive_db/
│   ├── main.py
│   ├── engine.py
│   ├── core.py
│   ├── utils.py
│   ├── parser.py
│   ├── constants.py
│   └── data/
├── pyproject.toml
├── Makefile
└── README.md
```

## Особенности

- Автоматическое добавление столбца ID:int
- Поддержка типов данных: int, str, bool
- Строгая проверка типов данных
- Регистронезависимые команды
- Хранение данных в JSON-файлах

---

**Автор**: Romanchuk Roman  
**Группа**: M25-555  
**Email**: r.romanchuk@ya.ru

