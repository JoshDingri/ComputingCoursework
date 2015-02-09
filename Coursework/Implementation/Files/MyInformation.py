from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class MyInformation(QMainWindow):
    """My information window for managers"""

    def __init__(self):
        self.setWindowTitle("My Information")


    def Display_Information(self):
        with sqlite3.connect("Accounts.db") as db:
            cursor = db.cursor()
            sql = "insert into Accounts(Username,Password,Access_Level,Department,FirstName,LastName) values (?,?,?,?,?,?)"
            cursor.execute(sql,values)
            db.commit()
        
