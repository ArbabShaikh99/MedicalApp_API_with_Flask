import sqlite3

def createBannerTable():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Banners (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            title        TEXT    NOT NULL,
            subtitle     TEXT    NOT NULL,
            image_id     INTEGER NOT NULL,
            color_hex    TEXT    NOT NULL DEFAULT '#1B6CA8',
            is_active    INTEGER NOT NULL DEFAULT 1,
            display_order INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
