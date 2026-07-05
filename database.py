import sqlite3

DATABASE_NAME = "placement.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        date_applied TEXT,
        company TEXT,
        cgpa REAL,
        status TEXT           
    )
    """)

    conn.commit()
    conn.close()