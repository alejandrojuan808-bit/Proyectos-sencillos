import os
import sqlite3
from flask import Flask, g, redirect, render_template_string, request, url_for

DATABASE = os.environ.get("DATABASE", "tasks.db")

HTML_TEMPLATE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TaskFlow</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; background: #f4f7fb; color: #1f2937; }
    .card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); margin-bottom: 1rem; }
    input, textarea, select, button { width: 100%; padding: 0.7rem; margin-top: 0.4rem; border-radius: 8px; border: 1px solid #d1d5db; }
    button { background: #2563eb; color: white; border: none; cursor: pointer; }
    .task { padding: 0.8rem 0; border-bottom: 1px solid #e5e7eb; }
    .priority { font-weight: bold; }
    .alta { color: #dc2626; }
    .media { color: #d97706; }
    .baja { color: #16a34a; }
  </style>
</head>
<body>
  <div class="card">
    <h1>TaskFlow</h1>
    <p>Gestor de tareas simple para mostrar habilidades de backend, bases de datos y pruebas.</p>
  </div>

  <div class="card">
    <h2>Nueva tarea</h2>
    <form method="post" action="{{ url_for('create_task') }}">
      <input name="title" placeholder="Título" required>
      <textarea name="description" placeholder="Descripción"></textarea>
      <select name="priority">
        <option value="baja">Baja</option>
        <option value="media">Media</option>
        <option value="alta">Alta</option>
      </select>
      <button type="submit">Guardar tarea</button>
    </form>
  </div>

  <div class="card">
    <h2>Tareas</h2>
    {% for task in tasks %}
      <div class="task">
        <strong>{{ task[1] }}</strong>
        <p>{{ task[2] or 'Sin descripción' }}</p>
        <span class="priority {{ task[3] }}">{{ task[3].capitalize() }}</span>
      </div>
    {% else %}
      <p>Aún no hay tareas registradas.</p>
    {% endfor %}
  </div>
</body>
</html>
"""


def get_db():
    if "db" not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


def close_db(exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT NOT NULL
        )
        """
    )
    db.commit()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=DATABASE,
        SECRET_KEY="dev-secret-key",
    )

    if config:
        app.config.update(config)

    app.teardown_appcontext(close_db)

    @app.route("/")
    def index():
        db = get_db()
        tasks = db.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        return render_template_string(HTML_TEMPLATE, tasks=tasks)

    @app.route("/tasks", methods=["POST"])
    def create_task():
        title = request.form["title"].strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "media").strip()

        db = get_db()
        db.execute(
            "INSERT INTO tasks (title, description, priority) VALUES (?, ?, ?)",
            (title, description, priority),
        )
        db.commit()
        return redirect(url_for("index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
