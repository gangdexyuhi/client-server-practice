import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# В служебной таблице sqlite_master хранится список всех таблиц базы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Таблицы в базе:", tables)

# Дополнительно выводим структуру таблицы tasks (имя колонки, тип, NOT NULL, значение по умолчанию)
cursor.execute("PRAGMA table_info(tasks)")
print("\nСтруктура таблицы tasks:")
for col in cursor.fetchall():
    cid, name, col_type, notnull, default, pk = col
    print(f"  {name:<7} {col_type:<8} NOT NULL={notnull}  DEFAULT={default}  PK={pk}")

conn.close()
