"""
Compress banner images in img.db
1.5MB PNG → ~150KB JPEG (banner size 800x300)
"""
import sqlite3
import io
from PIL import Image

DB_PATH = "instance/img.db"
BANNER_IDS = [14, 15, 16]
TARGET_W, TARGET_H = 800, 300  # landscape banner dimensions
JPEG_QUALITY = 85

conn = sqlite3.connect(DB_PATH)

for img_id in BANNER_IDS:
    row = conn.execute("SELECT img, mimetype FROM img WHERE id=?", (img_id,)).fetchone()
    if not row:
        print(f"ID {img_id} not found")
        continue

    original_bytes, mimetype = row
    original_size = len(original_bytes)

    img = Image.open(io.BytesIO(original_bytes)).convert("RGB")
    img = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)

    out = io.BytesIO()
    img.save(out, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    compressed = out.getvalue()
    compressed_size = len(compressed)

    conn.execute(
        "UPDATE img SET img=?, mimetype=? WHERE id=?",
        (compressed, "image/jpeg", img_id)
    )
    print(f"ID {img_id}: {original_size//1024}KB → {compressed_size//1024}KB ({mimetype} → image/jpeg)")

conn.commit()
conn.close()
print("Done.")
