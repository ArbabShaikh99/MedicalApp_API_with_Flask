import sqlite3

def updateUserName(userId , name):
     conn = sqlite3.connect("my_medicalshop.db")
     cursor =conn.cursor()
     cursor.execute("UPDATE Users SET name =? WHERE user_id =?",(name ,userId))

     conn.commit()
     conn.close()

     if cursor.rowcount > 0:
          print("Update successful. Rows affected:", cursor.rowcount)
          return 1
     else:
          print("   No Update , connnection check   . Check if the userId exists.")



def upDate_User_All_Fields(userID, **keyword):
    try:
        conn = sqlite3.connect("my_medicalshop.db")
        cursor = conn.cursor()

        for key, value in keyword.items():
            if key == "name":
                cursor.execute("UPDATE Users SET name = ? WHERE user_id = ?", (value, userID))
            elif key == "password":
                cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (value, userID))
            elif key == "email":
                cursor.execute("UPDATE Users SET email = ? WHERE user_id = ?", (value, userID))
            elif key == "phone":
                cursor.execute("UPDATE Users SET phone = ? WHERE user_id = ?", (value, userID))
            elif key == "address":
                cursor.execute("UPDATE Users SET address = ? WHERE user_id = ?", (value, userID))
            elif key == "isApproved":
                cursor.execute("UPDATE Users SET isApproved = ? WHERE user_id = ?", (value, userID))
            elif key == "block":
                cursor.execute("UPDATE Users SET block = ? WHERE user_id = ?", (value, userID))
            elif key == "level":
                cursor.execute("UPDATE Users SET level = ? WHERE user_id = ?", (value, userID))


        conn.commit()

        if cursor.rowcount > 0:
            print("Update successful. Rows affected:", cursor.rowcount)
            return 1
        else:
            print("No rows were updated. Check if the userID exists.")
            return 0
    except sqlite3.OperationalError as e:
        print("OperationalError:", e)
        return 0
    except Exception as e:
        print("Error:", e)
        return 0
    finally:
        conn.close()
