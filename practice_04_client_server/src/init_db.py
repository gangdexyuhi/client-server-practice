import sqlite3

# Подключаемся к базе. Если файла app.db ещё нет, sqlite3 создаст его сам.
conn = sqlite3.connect('app.db')

# Курсор нужен, чтобы отправлять SQL-запросы
cursor = conn.cursor()

# DDL: создаём таблицу задач.
# IF NOT EXISTS - чтобы повторный запуск скрипта не падал с ошибкой.
#   id     - уникальный номер задачи, SQLite заполняет его сам
#   title  - название задачи, пустым быть не может
#   status - статус, по умолчанию 'new'
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id     INTEGER PRIMARY KEY,
        title  TEXT NOT NULL,
        status TEXT DEFAULT 'new'
    )
""")

# Фиксируем изменения, без commit таблица не сохранится в файле
conn.commit()

# Закрываем соединение, чтобы файл базы не оставался заблокированным
conn.close()

print("База данных и таблица tasks успешно созданы.")
