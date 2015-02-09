from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class StaffDatabase(QMainWindow):
    """The staff database"""

    def __init__(self,account_details):
        super().__init__()
        self.setWindowTitle("Staff Database")
        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()
        self.account_details = account_details
        
        self.Back_btn = QPushButton("Back")
        self.horizontal.addWidget(self.Back_btn)
        self.horizontal.addStretch(1)
        self.CreateTable()

        
    def CreateTable(self):
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
            db.commit()

        col = [tuple[0] for tuple in self.cursor.description]
        self.table = QTableWidget(0,len(col))
                        
        self.table.setHorizontalHeaderLabels(col)
        self.table.setRowCount(0)

        for self.row, form in enumerate(self.cursor): ##Inserts amount of rows needed, gets from database
            self.table.insertRow(self.row)
            for self.column, item in enumerate(form): ##Inserts amount of columns needed
                self.item = QTableWidgetItem(str(item))
                self.item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(self.row, self.column,self.item) ##Each item is added to a the table
                self.table.horizontalHeader().setStretchLastSection(True)

        self.vertical.addLayout(self.horizontal)
        self.vertical.addWidget(self.table)

        window_widget = QWidget()
        window_widget.setLayout(self.vertical)
        self.setCentralWidget(window_widget)
