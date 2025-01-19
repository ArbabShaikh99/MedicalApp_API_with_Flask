import sqlite3

def createTables():
    conn = sqlite3.connect("my_medicalshop.db")
    cursor =conn.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id VARCHAR(255),
                   password VARCHAR(255),
                   level INT,
                   date_of_Account_Creatrion DATE,
                   isApproved BOOLEAN,
                   block VARCHAR(255),
                   name  VARCHAR(255),
                   email VARCHAR(255),
                   phone VARCHAR(255),
                   pinCode VARCHAR(255),
                   address VARCHAR(255)
                  
);
''')
    
    conn.commit()
    conn.close()