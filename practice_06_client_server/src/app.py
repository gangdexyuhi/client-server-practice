import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_PATH = 'app.db'


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_tasks():
    """Чтение задач. При ошибке БД возвращает пустой список, а не роняет приложение."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, status FROM tasks ORDER BY id")
        return cursor.fetchall()      # finally выполнится до возврата значения
    except sqlite3.Error as e:
        print(f"[DB ERROR] {e}")
        return []
    finally:
        conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()

        if not title:
            return render_template(
                'index.html',
                items=fetch_all_tasks(),
                error='Название задачи не может быть пустым.'
            )

        # соединение открываем ДО try, чтобы в finally было что закрывать
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()           # отменяем незавершённую транзакцию
            print(f"[DB ERROR] {e}")  # пишем ошибку в консоль сервера
            return render_template(
                'index.html',
                items=fetch_all_tasks(),
                error='Не удалось сохранить задачу. Попробуйте ещё раз.'
            )
        finally:
            conn.close()              # закрывается при любом исходе

        return redirect(url_for('index'))

    return render_template('index.html', items=fetch_all_tasks())


if __name__ == '__main__':
    app.run(debug=True, port=5000)
