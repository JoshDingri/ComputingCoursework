import sqlite3

def Add_Logins(values):
    with sqlite3.connect("Accounts.db") as db:
        cursor = db.cursor()
        sql = "insert into Accounts (Username,Password,Access_Level) values (?,?,?)"
        cursor.execute(sql,values)
        db.commit()

if __name__ == "__main__":
    product = ("JoshD","qwerty","Staff")
    Add_Logins(product)
