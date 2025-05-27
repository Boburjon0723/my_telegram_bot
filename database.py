import sqlite3

def init_db():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    # Foydalanuvchilar jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            full_name TEXT,
            phone TEXT,
            username TEXT,
            is_usta BOOLEAN DEFAULT FALSE
        )
    """)
    # Soha (skills) jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)
    # Usta-soha bog‘lovchi jadval
    c.execute("""
        CREATE TABLE IF NOT EXISTS usta_skills (
            user_id INTEGER,
            skill_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
        )
    """)
    # Buyurtmalar jadvali
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            usta_id INTEGER,
            skill_id INTEGER,
            status TEXT DEFAULT 'new',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(client_id) REFERENCES users(user_id),
            FOREIGN KEY(usta_id) REFERENCES users(user_id),
            FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
        )
    """)
    # Asosiy sohalarni kiritish (agar yo‘q bo‘lsa)
    skills = ["Santexnik", "Elektrik", "Malyarkachi", "Betonchi", "G'isht quyish", "Quruvchi"]
    for skill in skills:
        c.execute("INSERT OR IGNORE INTO skills (name) VALUES (?)", (skill,))
    conn.commit()
    conn.close()

def save_user(telegram_id, full_name, phone, username, is_usta):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (telegram_id, full_name, phone, username, is_usta)
        VALUES (?, ?, ?, ?, ?)
    """, (telegram_id, full_name, phone, username, is_usta))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    return user_id

def get_skill_id(skill_name):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT skill_id FROM skills WHERE name = ?", (skill_name,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def save_usta_skill(user_id, skill_name):
    skill_id = get_skill_id(skill_name)
    if skill_id:
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute("INSERT INTO usta_skills (user_id, skill_id) VALUES (?, ?)", (user_id, skill_id))
        conn.commit()
        conn.close()

def find_ustalar_by_skill(skill_name):
    skill_id = get_skill_id(skill_name)
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("""
        SELECT u.full_name, u.phone, u.username
        FROM users u
        JOIN usta_skills us ON u.user_id = us.user_id
        WHERE us.skill_id = ?
    """, (skill_id,))
    ustalar = c.fetchall()
    conn.close()
    return ustalar