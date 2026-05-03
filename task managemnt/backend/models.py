"""
Database models and helper functions for the Task Manager.
Uses SQLite with two tables: users and tasks.
- Users: stores email and bcrypt-hashed password
- Tasks: stores title, completed status, due_date, and references user via user_id
"""

import sqlite3
from config import DATABASE_PATH


def get_db():
    """
    Create and return a database connection.
    Uses Row factory for dict-like access to columns.
    Enables foreign key support for referential integrity.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign key constraints
    return conn


def init_db():
    """
    Initialize the database by creating tables if they don't exist.
    Called once when the application starts.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Users table: stores authentication credentials
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tasks table: stores user tasks with foreign key to users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            due_date TEXT,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("[OK] Database initialized successfully")
