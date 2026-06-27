import sqlite3
from flask import jsonify

def getAllBanners():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, subtitle, image_id, color_hex, is_active, display_order
        FROM Banners
        WHERE is_active = 1
        ORDER BY display_order ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "id":            row[0],
            "title":         row[1],
            "subtitle":      row[2],
            "image_id":      row[3],
            "color_hex":     row[4],
            "is_active":     row[5],
            "display_order": row[6]
        }
        for row in rows
    ])
