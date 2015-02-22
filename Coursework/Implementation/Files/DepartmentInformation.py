from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from LoginWindow import *

class DepartmentInformation(QWidget):
    """Managers Department Information"""

    def __init__(self,department):
        super().__init__()
        self.resize(400,500)
        self.Grid_Layout = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()
        self.vertical = QVBoxLayout()
        self.department = department #gets department and adds to object


        self.Search_LE = QLineEdit(self)
        self.Search_LE.setFixedWidth(150)
        self.Search_LE.setFixedHeight(25)
        self.Search_LE.setPlaceholderText("Search Fields")

        self.Back_btn = QPushButton("Back")
        self.Back_btn.setFixedWidth(50)

        space = QLabel('                                      ',self)



        self.horizontal.addWidget(self.Back_btn)
        self.horizontal.addStretch(1)

        self.horizontal2.addStretch(1)
        
        self.horizontal2.addWidget(self.Search_LE)

        self.Grid_Layout.setVerticalSpacing(20)

        self.iconbutton = QLabel(self)

        pixmap = QPixmap('search.png')
        pixmap = pixmap.scaled(QSize(25,25),Qt.KeepAspectRatio)
        self.iconbutton.setPixmap(pixmap)

        self.horizontal2.addWidget(self.iconbutton)

        self.table = QTableWidget()

        self.vertical.addLayout(self.horizontal)
        self.vertical.addLayout(self.horizontal2)
        self.vertical.addWidget(self.table)

        self.setLayout(self.vertical)

        self.CreateTable()

    def CreateTable(self): 

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            self.cursor.execute("SELECT DepartmentID FROM Department WHERE DepartmentName=?",(self.department,))
            db.commit()
            
        for self.row, form in enumerate(self.cursor): #adds counter to for loop with iterable
                for self.column, item in enumerate(form):
                    self.DepartmentID = item
                    print(self.DepartmentID)

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            self.cursor.execute("SELECT StaffID FROM Staff WHERE DepartmentID=?",(self.DepartmentID,))
            db.commit()

        for self.row, form in enumerate(self.cursor): 
                for self.column, item in enumerate(form):
                    self.StaffID = item

        print(self.StaffID)    
            
        self.table.deleteLater()

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            self.cursor.execute("SELECT StaffHardware.* FROM StaffHardware WHERE StaffHardware.StaffID =?",(self.StaffID,))
            
        col = [tuple[0] for tuple in self.cursor.description]
        self.table = QTableWidget(2,len(col))
                        
        self.table.setHorizontalHeaderLabels(col)
        self.table.setRowCount(0)

        for self.row, form in enumerate(self.cursor): ##Inserts amount of rows needed, gets from database
                self.table.insertRow(self.row)
                for self.column, item in enumerate(form): ##Inserts amount of columns needed
                    CurrentHeader = (self.table.horizontalHeaderItem(self.column).text())
                    if CurrentHeader == 'StaffID' and self.column != 0: ##Wont run if statement if the header is primary key
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

        self.vertical.addWidget(self.table)

        self.Search_LE.textChanged.connect(self.SearchMethod)

            
    def SearchMethod(self):
        for index in range(self.table.rowCount()):
            self.table.setRowHidden(index,True)
        text = self.Search_LE.text()
        if text == '':
            for index in range(self.table.rowCount()):
                self.table.setRowHidden(index,False)
        else:
            itemlist = self.table.findItems(text,Qt.MatchStartsWith)
            for count in range(len(itemlist)):
                rownum = (itemlist[count].row())
                self.table.setRowHidden(rownum,False)       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = DepartmentInformation()
    launcher.show()
    launcher.raise_()
    app.exec_()
