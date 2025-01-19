import sqlite3

def deleteProduct(productId):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Products WHERE product_id=?",(productId,))        
    conn.commit()
    conn.close()