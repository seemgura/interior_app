
from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Crear la base de datos si no existe
conn = sqlite3.connect('opiniones.db')
conn.execute('''CREATE TABLE IF NOT EXISTS opiniones
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              nombre TEXT NOT NULL,
              comentario TEXT NOT NULL)''')
conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/opiniones", methods=["GET", "POST"])
def opiniones():
    conn = sqlite3.connect("opiniones.db")
    c = conn.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        comentario = request.form["comentario"]
        c.execute("INSERT INTO opiniones (nombre, comentario) VALUES (?, ?)", (nombre, comentario))
        conn.commit()

    c.execute("SELECT nombre, comentario FROM opiniones ORDER BY id DESC")
    opiniones = c.fetchall()
    conn.close()
    return render_template("opiniones.html", opiniones=opiniones)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
