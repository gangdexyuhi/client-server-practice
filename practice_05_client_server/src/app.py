import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_PATH = 'app.db'


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_tasks():
    """Все задачи из базы. Нужна и для GET, и для показа ошибки после POST."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status FROM tasks ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.route('/', methods=['GET', 'POST'])
def index():
    # ---------- POST: пришла форма ----------
    if request.method == 'POST':
        title = request.form.get('title', '').strip()

        # проверка на сервере: required в HTML можно обойти
        if not title:
            return render_template(
                'index.html',
                items=fetch_all_tasks(),
                error='Название задачи не может быть пустым.'
            )

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()

        # Post/Redirect/Get: после добавления перенаправляем на GET,
        # чтобы F5 не отправлял форму повторно
        return redirect(url_for('index'))

    # ---------- GET: показываем страницу ----------
    return render_template('index.html', items=fetch_all_tasks())


if __name__ == '__main__':
    app.run(debug=True, port=5000)
