import sqlite3
from datetime import datetime
import os

DB_NAME = "attendance_system.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table for users (registered faces)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            department TEXT,
            role TEXT,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for attendance logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            type TEXT DEFAULT 'masuk',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_name) REFERENCES users(name)
        )
    ''')
    
    # Migrate existing database if type column doesn't exist
    try:
        cursor.execute("ALTER TABLE attendance ADD COLUMN type TEXT DEFAULT 'masuk'")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    conn.commit()
    conn.close()

def add_user(name, department="Umum", role="Karyawan"):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (name, department, role) VALUES (?, ?, ?)", (name, department, role))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

def mark_attendance(name, att_type="masuk"):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO attendance (user_name, type) VALUES (?, ?)", (name, att_type))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error marking attendance: {e}")
        return False

def get_recent_attendance(limit=5):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_name, timestamp, type 
            FROM attendance 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error getting recent attendance: {e}")
        return []

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
