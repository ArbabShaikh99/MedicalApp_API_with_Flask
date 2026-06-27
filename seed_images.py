"""
Seed img.db with placeholder images for product IDs 3-12.
Run this AFTER stopping Flask, from the project root:
    python3 seed_images.py
"""

import sqlite3
import struct
import zlib

# ── Minimal valid PNG generator ────────────────────────────────────────────────
def make_png(width=200, height=200, r=41, g=128, b=185):
    def chunk(tag, data):
        c = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', c)

    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr = chunk(b'IHDR', ihdr_data)

    raw_rows = b''
    for _ in range(height):
        row = b'\x00' + bytes([r, g, b] * width)
        raw_rows += row
    compressed = zlib.compress(raw_rows)
    idat = chunk(b'IDAT', compressed)
    iend = chunk(b'IEND', b'')

    return signature + ihdr + idat + iend

# ── Product data — must match existing DB rows ─────────────────────────────────
PRODUCTS = [
    (3,  "paracetamol.png",   "Paracetamol",       41,  128, 185),
    (4,  "n95_mask.png",      "N95 Mask",           44,  160, 110),
    (5,  "bp_monitor.png",    "BP Monitor",         192, 57,  43 ),
    (6,  "ali.png",           "Product",            142, 68,  173),
    (7,  "sanitizer.png",     "Hand Sanitizer",     39,  174, 96 ),
    (8,  "ibuprofen.png",     "Ibuprofen",          243, 156, 18 ),
    (9,  "vitamin_c.png",     "Vitamin C",          230, 126, 34 ),
    (10, "thermometer.png",   "Thermometer",        26,  188, 156),
    (11, "amoxicillin.png",   "Amoxicillin",        41,  128, 185),
    (12, "metformin.png",     "Metformin",          192, 57,  43 ),
]

def seed():
    # Init Flask app context to create table via SQLAlchemy
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))

    from main import app, db
    with app.app_context():
        db.create_all()
        print("✅ img table created")

        from Medical_DataBase.uploadImg.models import Img
        from sqlalchemy import text

        # Clear existing
        db.session.execute(text("DELETE FROM img"))
        db.session.commit()

        # Insert with explicit IDs
        for (img_id, filename, label, r, g, b) in PRODUCTS:
            png_bytes = make_png(r=r, g=g, b=b)
            db.session.execute(
                text("INSERT INTO img (id, img, name, mimetype) VALUES (:id, :img, :name, :mime)"),
                {"id": img_id, "img": png_bytes, "name": filename, "mime": "image/png"}
            )
            print(f"  Inserted image ID={img_id}  ({label})")

        db.session.commit()
        print("\n✅ Done! img.db seeded with 10 product images (IDs 3–12)")

if __name__ == "__main__":
    seed()
