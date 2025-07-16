
from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_FILE = 'opiniones.db'

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS opiniones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                opinion TEXT NOT NULL
            );
        ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/opiniones', methods=['GET', 'POST'])
def opiniones():
    if request.method == 'POST':
        nombre = request.form['nombre']
        opinion = request.form['opinion']
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO opiniones (nombre, opinion) VALUES (?, ?)", (nombre, opinion))
        return redirect('/opiniones')
    else:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.execute("SELECT nombre, opinion FROM opiniones")
            opiniones = [{"nombre": row[0], "opinion": row[1]} for row in cursor.fetchall()]
        return render_template('opiniones.html', opiniones=opiniones)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
