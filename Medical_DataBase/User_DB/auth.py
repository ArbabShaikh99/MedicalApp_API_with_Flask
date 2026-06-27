import sqlite3
import bcrypt


def user_auth(email, password):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    stored_hash = user[2]
    try:
        password_matches = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    except Exception:
        return None

    if not password_matches:
        return None

    return {
        "user_id": user[1],
        "level": user[3],
        "created_at": str(user[4]),
        "is_approved": user[5],
        "is_blocked": user[6] == "1" or user[6] == 1,
        "name": user[7],
        "email": user[8],
        "phone": user[9],
        "pin_code": user[10],
        "address": user[11]
    }
