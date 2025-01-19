import sqlite3
import uuid
from datetime import date

 
 
 
 
def createUser(name,password,phone_Number , email,pinCode,address):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor =conn.cursor()
  
    user_id = str(uuid.uuid4())
    date_of_Account_Creatrion = date.today()

    cursor.execute("""
INSERT INTO Users(
user_id,password,level,date_of_Account_Creatrion,isApproved,block,name,email,phone,pinCode,address)
               VALUES(?,?,?,?,?,?,?,?,?,?,?)

""",(user_id, password,1, date_of_Account_Creatrion, 0,0,name,email,phone_Number,pinCode, address ))
    
    conn.commit()
    conn.close()

    return user_id



def createProduct (product_Name,stock,price , category,Expire_Date):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    product_id =str(uuid.uuid4)
   

    cursor.execute("""
INSERT INTO Products(
                   product_id,product_Name,stock,price,category,Expire_Date)
                   VALUES(?,?,?,?,?,?)
""",(product_id,product_Name,stock,price , category,Expire_Date))
    conn.commit()
    conn.close()
    return product_id
    
