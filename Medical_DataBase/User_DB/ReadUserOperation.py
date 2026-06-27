import sqlite3
import json
from flask import jsonify


def _user_to_dict(user):
    return {
        "id": user[0],
        "user_id": user[1],
        # password (index 2) intentionally omitted
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


def getAllUsers():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return json.dumps([_user_to_dict(u) for u in users])


def getSpecificUser(userID):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE user_id = ?", (userID,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return jsonify({"status": 404, "message": "User not found"}), 404

    return jsonify(_user_to_dict(user))
