import sqlite3

def create_table(db_name,sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

if __name__ == "__main__":
    db_name = "Accounts.db"
    sql = """create table Accounts
          (Username text,
          Password text,
          Access_Level text,
          Department text,
          FirstName text,
          LastName text,
          primary key(Username))"""
    create_table(db_name,sql)
