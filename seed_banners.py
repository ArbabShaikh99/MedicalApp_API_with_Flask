"""
Seed Banners table with 3 sample banners.
Run once after restarting Flask:
    source venv/bin/activate && python3 seed_banners.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from main import app
from Medical_DataBase.Banner_DB.CreateBannerTable import createBannerTable
from Medical_DataBase.Banner_DB.AddBannerOperation import addBanner
import sqlite3

def seed():
    with app.app_context():
        createBannerTable()

        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Banners")
        conn.commit()
        conn.close()

        banners = [
            ("Quality Medical Supplies",  "Trusted by Healthcare Professionals", 3, "#1B6CA8", 0),
            ("Fresh Stock Every Week",    "100% Verified & Certified Products",   4, "#00897B", 1),
            ("Fast Delivery",             "Order before 5 PM for same-day ship",  5, "#5C6BC0", 2),
        ]

        for title, subtitle, image_id, color_hex, order in banners:
            bid = addBanner(title, subtitle, image_id, color_hex, order)
            print(f"  Banner id={bid}  '{title}'")

        print("\nDone! 3 banners seeded.")

if __name__ == "__main__":
    seed()
