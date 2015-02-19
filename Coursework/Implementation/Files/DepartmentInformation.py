from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from LoginWindow import *

class DepartmentInformation(QMainWindow):
    """Managers table view"""

    def __init__(self,department):
        super().__init__()
        self.resize(400,500)
        self.grid = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()
        self.verticle = QVBoxLayout()
        self.department = department
        
        
##        DatabaseLbl = QLabel(self)
##        DatabaseLbl.setFont(QFont("Calibri",20))
##        self.Database_CB = QComboBox(self)
##        self.Database_CB.addItem('Select Table')
##        self.Database_CB.setFixedHeight(30)
##        self.Database_CB.setFixedWidth(150)


        self.Search_LE = QLineEdit(self)
        self.Search_LE.setFixedWidth(150)
        self.Search_LE.setFixedHeight(25)
        self.Search_LE.setPlaceholderText("Search Fields")

        self.Back_btn = QPushButton("Back",self)
        self.Back_btn.setFixedWidth(50)

        space = QLabel('                                      ',self)
##        self.AddDatabase = QPushButton('Open Database',self)
##        self.AddDatabase.setFont(QFont("Calibri",8))
##        self.AddDatabase.setFixedWidth(80)
##        self.AddDatabase.setFixedHeight(20)



        self.horizontal.addWidget(self.Back_btn)
        self.horizontal.addStretch(1)
##        self.grid.addWidget(DatabaseLbl,1,1)
##        self.grid.addWidget(self.Database_CB,1,2)
##        self.grid.addWidget(self.AddDatabase,1,3)

        self.horizontal2.addStretch(1)
        
        self.horizontal2.addWidget(self.Search_LE)

        self.grid.setVerticalSpacing(20)

        self.iconbutton = QLabel(self)

        pixmap = QPixmap('search.png')
        pixmap = pixmap.scaled(QSize(25,25),Qt.KeepAspectRatio)
        self.iconbutton.setPixmap(pixmap)

        self.horizontal2.addWidget(self.iconbutton)

        self.table = QTableWidget()

        self.verticle.addLayout(self.horizontal)
        self.verticle.addLayout(self.horizontal2)
        self.verticle.addWidget(self.table)

        window_widget = QWidget()
        window_widget.setLayout(self.verticle)
        self.setCentralWidget(window_widget)

        self.CreateTable()

    def CreateTable(self): 
        print(self.department)


        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT DepartmentID FROM Department WHERE DepartmentName='{0}'".format(self.department)
            self.cursor.execute(sql)
            db.commit()
            
        for self.row, form in enumerate(self.cursor): 
                for self.column, item in enumerate(form):
                    self.DepartmentID = item
                    print(self.DepartmentID)

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT StaffID FROM Staff WHERE DepartmentID='{0}'".format(self.DepartmentID)
            self.cursor.execute(sql)
            db.commit()

        for self.row, form in enumerate(self.cursor): 
                for self.column, item in enumerate(form):
                    self.StaffID = item

        print(self.StaffID)    
            
        self.table.deleteLater()
##        self.CurrentTable = (self.Database_CB.currentText())

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT StaffHardware.* FROM StaffHardware WHERE StaffHardware.StaffID = '{0}'".format(self.StaffID)
            self.cursor.execute(sql)
            
        col = [tuple[0] for tuple in self.cursor.description]
        self.table = QTableWidget(2,len(col))
                        
        self.table.setHorizontalHeaderLabels(col)
        self.table.setRowCount(0)

        for self.row, form in enumerate(self.cursor): ##Inserts amount of rows needed, gets from database
                self.table.insertRow(self.row)
                for self.column, item in enumerate(form): ##Inserts amount of columns needed
                    CurrentHeader = (self.table.horizontalHeaderItem(self.column).text())
                    if CurrentHeader == 'StaffID' and self.column != 0: 
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    sql = "SELECT FirstName,Surname from Staff WHERE StaffID ='{}'".format(item)
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
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
                                    sql = "SELECT HardwareModelID from Hardware WHERE HardwareID ='{}'".format(item)
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
                                    ModelID = list(cursor.fetchone())
                                    db.commit()
                                    
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    sql = "SELECT HardwareMakeID from HardwareModel WHERE HardwareModelID ='{}'".format(ModelID[0])
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
                                    MakeID = list(cursor.fetchone())
                                    db.commit()

                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    sql = "SELECT HardwareMake.HardwareMakeName,HardwareModel.HardwareModelName FROM HardwareModel,HardwareMake WHERE HardwareModel.HardwareModelID ='{}' AND HardwareMake.HardwareMakeID = '{}'".format(ModelID[0],MakeID[0])
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
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

        self.verticle.addWidget(self.table)

        self.Search_LE.textChanged.connect(self.SearchMethod)

            
    def SearchMethod(self):
        for index in range(self.table.rowCount()):
            self.table.setRowHidden(index,True)
        text = self.Search_LE.text()
        if text == '':
            itemlist = self.table.findItems(text,Qt.MatchStartsWith)
            for count in range(len(itemlist)):
                itemlist[count].setBackgroundColor(QColor('White'))
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
