from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class MyInformation(QWidget):
    """My information window for managers so they may see their own hardware"""

    def __init__(self,account_details):
        super().__init__()
        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()
        
        self.account_details = account_details
        self.Back_btn = QPushButton("Back")
        self.setWindowTitle("My Information")
        self.horizontal.addWidget(self.Back_btn)
        self.horizontal.addStretch(1)
        self.Display_Information()
        


    def Display_Information(self):
        
        with sqlite3.connect("Accounts.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT FirstName,LastName FROM Accounts WHERE Username =?",(self.account_details[0],))
            values = list(cursor.fetchone())
            db.commit()

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT StaffID FROM Staff WHERE FirstName =? AND Surname =?",(values[0],values[1],))
            staffids = list(cursor.fetchone())
            db.commit()

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            self.cursor.execute("SELECT * FROM StaffHardware WHERE StaffID =?",(staffids[0],))
            db.commit()

        name_lbl = QLabel("Welcome {0}! These Are Your Current Hardware Devices".format(values[0]))
        name_lbl.setFont(QFont("Arial",14))
        self.horizontal.addWidget(name_lbl)
        self.horizontal.addStretch(1)
        

        col = [tuple[0] for tuple in self.cursor.description] #Gets column headers and stores into tuple
        self.table = QTableWidget(2,len(col))
                        
        self.table.setHorizontalHeaderLabels(col)
        self.table.setRowCount(0)

        for self.row, form in enumerate(self.cursor): ##Inserts amount of rows needed, gets from database
                self.table.insertRow(self.row)
                for self.column, item in enumerate(form): ##Inserts amount of columns needed
                    CurrentHeader = (self.table.horizontalHeaderItem(self.column).text())
                    
                        ## The below if statements provide a user friendly display of foreign keys##
                    
                    if CurrentHeader == 'StaffID' and self.column != 0: 
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute("SELECT FirstName,Surname from Staff WHERE StaffID =?",(item,))
                                    db.commit()
                                Foreign_Item = str([item[0] + ', ' + item[1] for item in cursor.fetchall()])
                                
                                b = "[]'',"
                                for i in range(0,len(b)):
                                    Foreign_Item = Foreign_Item.replace(b[i],"") 
                                
                                self.item = QTableWidgetItem(Foreign_Item)
                                self.item.setTextAlignment(Qt.AlignCenter)
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                                continue
                                
                    elif CurrentHeader == 'HardwareID' and self.column != 0:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute("SELECT HardwareModelID from Hardware WHERE HardwareID =?",(item,))
                                    ModelID = list(cursor.fetchone())
                                    db.commit()
                                    
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute("SELECT HardwareMakeID from HardwareModel WHERE HardwareModelID =?",(ModelID[0],))
                                    MakeID = list(cursor.fetchone())
                                    db.commit()

                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute("SELECT HardwareMake.HardwareMakeName,HardwareModel.HardwareModelName FROM HardwareModel,HardwareMake WHERE HardwareModel.HardwareModelID =? AND HardwareMake.HardwareMakeID =?",(ModelID[0],MakeID[0],))
                                    db.commit()

                                HardwareForeignKey = str([item[0] + ', ' + item[1] for item in cursor.fetchall()])

                                
                                b = "[]'',"
                                for i in range(0,len(b)):
                                    HardwareForeignKey = HardwareForeignKey.replace(b[i],"") 
                                    
                                self.item = QTableWidgetItem(HardwareForeignKey)
                                self.item.setTextAlignment(Qt.AlignCenter)
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                                continue
                    self.item = QTableWidgetItem(str(item))
                    self.item.setFlags(Qt.ItemIsEnabled)
                    self.table.setItem(self.row, self.column,self.item) ##Each item is added to a the table
                    self.table.horizontalHeader().setStretchLastSection(True)

        self.vertical.addLayout(self.horizontal)
        self.vertical.addWidget(self.table)

        self.setLayout(self.vertical)

