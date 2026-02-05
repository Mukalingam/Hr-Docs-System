import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "data/resumeforge.db")


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            candidate_name TEXT,
            resume_filename TEXT,
            format_filename TEXT,
            extracted_json TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Seed default users if empty
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        default_users = [
            ("admin", "admin@123", "Admin User", "admin"),
            ("recruiter", "recruit@123", "HR Recruiter", "user"),
            ("manager", "manage@123", "Hiring Manager", "user"),
        ]
        c.executemany(
            "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
            default_users
        )

    conn.commit()
    conn.close()


def authenticate(username, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id, username, full_name, role FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None


def save_extraction(user_id, candidate_name, resume_filename, format_filename, extracted_json):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """INSERT INTO extractions (user_id, candidate_name, resume_filename, format_filename, extracted_json)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, candidate_name, resume_filename, format_filename, json.dumps(extracted_json))
    )
    conn.commit()
    conn.close()


def get_user_extractions(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM extractions WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_extraction_by_id(extraction_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM extractions WHERE id = ?", (extraction_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_extraction(extraction_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM extractions WHERE id = ?", (extraction_id,))
    conn.commit()
    conn.close()


def get_all_users():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, username, full_name, role, created_at FROM users ORDER BY created_at")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_user(username, password, full_name, role="user"):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
            (username, password, full_name, role)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False


def delete_user(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM extractions WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()