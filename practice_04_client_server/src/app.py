import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

DB_PATH = 'app.db'


def get_connection():
    """Соединение с базой. row_factory позволяет обращаться к полям по имени: row['title']."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    # 1. подключение
    conn = get_connection()
    cursor = conn.cursor()

    # 2. чтение всех задач
    cursor.execute("SELECT id, title, status FROM tasks ORDER BY id")
    rows = cursor.fetchall()

    # 3. закрываем соединение (commit не нужен - данные не меняются)
    conn.close()

    # 4. передаём данные в шаблон под именем items
    return render_template('index.html', items=rows)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
