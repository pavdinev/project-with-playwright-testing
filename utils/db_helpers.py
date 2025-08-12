import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).parent.parent / "db" / "test_data.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_booking(name, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (name, date) VALUES (?, ?)", (name, date))
    conn.commit()
    conn.close()

def fetch_booking(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE name=?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result
