import sqlite3 ,uuid


def addProductOperation(name,category,price,stock,expiry_date,rating,description,image,power):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    product_id  = str(uuid.uuid4())

    cursor.execute("""
                INSERT INTO Products(
                  product_id,
                  product_name,
                  product_category,
                  product_price,
                  product_stock,
                  product_expiry_date,
                  product_rating,
                  product_description,
                  product_image_id,
                  product_power
                  ) VALUES (?,?,?,?,?,?,?,?,?,?)
            """,(product_id,name,category,price,stock,expiry_date,rating,description,image,power))
         
    conn.commit()
    conn.close()

    return product_id