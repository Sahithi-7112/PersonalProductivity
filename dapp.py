from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("diary.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("diary.db")
    cursor = conn.cursor()

 
    if request.method == "POST" and "title" in request.form:
        title = request.form["title"]
        content = request.form["content"]
        cursor.execute("INSERT INTO diary (title, content) VALUES (?, ?)", (title, content))
        conn.commit()

   
    show_entries = request.form.get("show_entries") == "yes"

    
    entries = []
    if show_entries:
        cursor.execute("SELECT * FROM diary ORDER BY created_at DESC")
        entries = cursor.fetchall()
    
    conn.close()
    
    return render_template("diary.html", entries=entries, show_entries=show_entries)


init_db()

if __name__ == "__main__":
    app.run(debug=True)
