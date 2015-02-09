from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class MyInformation(QMainWindow):
    """My information window for managers"""

    def __init__(self,account_details):
        super().__init__()
        self.account_details = account_details
        self.setWindowTitle("My Information")
        self.Display_Information()


    def Display_Information(self):
        self.vertical = QVBoxLayout()
        with sqlite3.connect("Accounts.db") as db:
            cursor = db.cursor()
            sql = "SELECT FirstName,LastName FROM Accounts WHERE Username = '{0}'".format(self.account_details[0])
            cursor.execute(sql)
            values = list(cursor.fetchone())
            db.commit()


        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT * FROM Staff WHERE FirstName = '{0}' AND Surname = '{1}'".format(values[0],values[1])
            self.cursor.execute(sql)

        col = [tuple[0] for tuple in self.cursor.description]
        self.table = QTableWidget(2,len(col))
                        
        self.table.setHorizontalHeaderLabels(col)
        self.table.setRowCount(0)

        for self.row, form in enumerate(self.cursor): ##Inserts amount of rows needed, gets from database
                self.table.insertRow(self.row)
                for self.column, item in enumerate(form): ##Inserts amount of columns needed
                    self.item = QTableWidgetItem(str(item))
                    self.item.setFlags(Qt.ItemIsEnabled)
                    self.table.setItem(self.row, self.column,self.item) ##Each item is added to a the table
                    self.table.horizontalHeader().setStretchLastSection(True)

        self.vertical.addWidget(self.table)
        self.setLayout(self.vertical)
