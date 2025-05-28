import sqlite3

def get_conn():
    return sqlite3.connect("app.db")

def init_db():
    conn = get_conn()
    c = conn.cursor()
    # Foydalanuvchilar jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            full_name TEXT,
            phone TEXT,
            username TEXT,
            is_usta BOOLEAN DEFAULT 0
        )
    """)
    # Usta malakalari jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS usta_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            skill TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user(telegram_id, full_name, phone, username, is_usta):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (telegram_id, full_name, phone, username, is_usta)
        VALUES (?, ?, ?, ?, ?)
    """, (telegram_id, full_name, phone, username, is_usta))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id

def save_usta_skill(user_id, skill):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO usta_skills (user_id, skill) VALUES (?, ?)", (user_id, skill))
    conn.commit()
    conn.close()

def find_ustalar_by_skill(skill):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT users.full_name, users.phone, users.username
        FROM users
        JOIN usta_skills ON users.user_id = usta_skills.user_id
        WHERE usta_skills.skill = ?
    """, (skill,))
    result = c.fetchall()
    conn.close()
    return result