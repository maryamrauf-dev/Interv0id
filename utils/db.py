import sqlite3
import os
from datetime import datetime

DB_PATH = "interview_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            score INTEGER,
            target_role TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_history(score, target_role):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO history (date, score, target_role) VALUES (?, ?, ?)", (date_str, score, target_role))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT date, score, target_role FROM history ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    history = []
    for row in rows:
        history.append({
            "date": row[0],
            "score": row[1],
            "target_role": row[2]
        })
    return history
