import sqlite3,json
from flask import jsonify


def getAllProducts():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products")

    products = cursor.fetchall()
    conn.close()

    productjson=[]

    for productItem in products:
        tempProducts ={
           
           "id" : productItem[0],
            "product_id" : productItem[1],
            "product_name":productItem[2],
            "product_category":productItem[3],
            "product_price":productItem[4],
            "product_stock":productItem[5],
            "product_expiry_date":productItem[6],
            "product_rating":productItem[7],
            "product_description":productItem[8],
            "product_image_id":productItem[9],
            "product_power":productItem[10]
        }
        productjson.append(tempProducts)

         
    return jsonify(productjson)
         


def searchProducts(query):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    like = f"%{query}%"
    cursor.execute(
        """SELECT * FROM Products WHERE
           product_name LIKE ? OR
           product_category LIKE ? OR
           product_description LIKE ?""",
        (like, like, like)
    )
    products = cursor.fetchall()
    conn.close()

    productjson = []
    for productItem in products:
        productjson.append({
            "id": productItem[0],
            "product_id": productItem[1],
            "product_name": productItem[2],
            "product_category": productItem[3],
            "product_price": productItem[4],
            "product_stock": productItem[5],
            "product_expiry_date": productItem[6],
            "product_rating": productItem[7],
            "product_description": productItem[8],
            "product_image_id": productItem[9],
            "product_power": productItem[10]
        })

    return jsonify(productjson)


def getSpecifiProduct(ProductID):
     conn = sqlite3.connect("my_medicalshop.db")
     cursor = conn.cursor()

     cursor.execute("SELECT * FROM Products WHERE product_id=?",(ProductID,))
     products =cursor.fetchall()
     conn.close()

     productjson=[]

     for productItem in products:
        tempProducts ={
             "id" : productItem[0],
            "product_id" : productItem[1],
            "product_name":productItem[2],
            "product_category":productItem[3],
            "product_price":productItem[4],
            "product_stock":productItem[5],
            "product_expiry_date":productItem[6],
            "product_rating":productItem[7],
            "product_description":productItem[8],
            "product_image_id":productItem[9],
            "product_power":productItem[10]
            
        }
        productjson.append(tempProducts)

         
     return jsonify(productjson) 
