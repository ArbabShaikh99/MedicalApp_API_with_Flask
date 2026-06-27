import sqlite3

def addBanner(title, subtitle, image_id, color_hex='#1B6CA8', display_order=0):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Banners (title, subtitle, image_id, color_hex, display_order)
        VALUES (?, ?, ?, ?, ?)
    """, (title, subtitle, image_id, color_hex, display_order))
    conn.commit()
    banner_id = cursor.lastrowid
    conn.close()
    return banner_id
