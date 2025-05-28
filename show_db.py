import sqlite3

conn = sqlite3.connect("app.db")
c = conn.cursor()

print("=== USERS jadvali ===")
for row in c.execute("SELECT * FROM users"):
    print(row)

print("\n=== USTA_SKILLS jadvali ===")
for row in c.execute("SELECT * FROM usta_skills"):
    print(row)

conn.close()