import sqlite3 

def DeleteUser(UserID):
    conn = sqlite3.connect("my_medicalshop.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Users WHERE user_id =?",(UserID,))

    conn.commit()
    conn.close()

    # Check if any rows were affected
    if cursor.rowcount > 0:
        print("Delete User successfully. Rows affected:", cursor.rowcount)
        return 1
    else:
        print("No rows were Deleted. Check if the userId exists.")
        return 0