import sqlite3
import json


def getAllUsers():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users")

    users = cursor.fetchall()
    conn.close()

    userJson=[]
    for user in users:
        tempUser ={
            "id": user[0],
            "user_id": user[1],
            "password": user[2],
            "level": user[3],
            "date_of_Account_Creatrion": user[4],
            "isApproved": user[5],
            "block": user[6],
            "name": user[7],
            "email": user[8],
            "phone": user[9],
            "pinCode": user[10],
             "address": user[11]
        }
        userJson.append(tempUser)

         
    return(json.dumps(userJson)) 



def getSpecificUser(userID):
     conn = sqlite3.connect("my_medicalshop.db")
     cursor = conn.cursor()

     cursor.execute("SELECT * FROM Users WHERE user_id=? ",(userID,))
     users =cursor.fetchall()
     conn.close()


     userJson=[]

    
     for user in users:
        tempUser ={
            "id": user[0],
            "user_id": user[1],
            "password": user[2],
            "level": user[3],
            "date_of_Account_Creatrion": user[4],
            "isApproved": user[5],
            "block": user[6],
            "name": user[7],
            "email": user[8],
            "phone": user[9],
            "pinCode": user[10],
             "address": user[11]
        }
        userJson.append(tempUser)

         
     return(json.dumps(tempUser)) 



