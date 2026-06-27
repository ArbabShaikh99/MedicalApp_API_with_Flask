import sqlite3
import uuid
import bcrypt
from datetime import date


def createUser(name, password, phone_Number, email, pinCode, address):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    user_id = str(uuid.uuid4())
    created_at = date.today()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cursor.execute("""
        INSERT INTO Users(user_id, password, level, date_of_Account_Creatrion, isApproved, block, name, email, phone, pinCode, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, hashed_password, 1, created_at, 0, 0, name, email, phone_Number, pinCode, address))

    conn.commit()
    conn.close()
    return user_id
