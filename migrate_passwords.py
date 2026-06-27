"""
One-time script: hash all existing plain-text passwords in the database.
Run once: python migrate_passwords.py
Safe to run multiple times — skips already-hashed passwords.
"""
import sqlite3
import bcrypt

conn = sqlite3.connect("my_medicalshop.db")
cursor = conn.cursor()
cursor.execute("SELECT user_id, password FROM Users")
users = cursor.fetchall()

updated = 0
skipped = 0

for user_id, password in users:
    # Already hashed passwords start with $2b$ (bcrypt prefix)
    if password.startswith("$2b$") or password.startswith("$2a$"):
        skipped += 1
        continue

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (hashed, user_id))
    updated += 1

conn.commit()
conn.close()
print(f"Done. Updated: {updated} users | Skipped (already hashed): {skipped}")
