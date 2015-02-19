from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from StaffMenuBar import *
from ChangePassword import *
from Reporterror import *
from BugReport import *

class StaffDatabase(QMainWindow):
    """The staff database"""

    def __init__(self,account_details):
        super().__init__()
        self.resize(800,400)
        
        self.setWindowTitle("Staff Database")
        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()
        self.account_details = account_details

        SearchLbl = QLabel(self)
        self.Search_LE = QLineEdit(self)
        self.Search_LE.setFixedWidth(150)
        self.Search_LE.setFixedHeight(25)
        self.Search_LE.setPlaceholderText("Search Fields")
        SearchLbl.setFont(QFont("Calibri",20))
        
        self.iconbutton = QLabel(self)


        pixmap = QPixmap('search.png')
        pixmap = pixmap.scaled(QSize(25,25),Qt.KeepAspectRatio)
        self.iconbutton.setPixmap(pixmap)

        self.horizontal.addStretch(1)

        self.horizontal.addWidget(self.iconbutton)
        self.horizontal.addWidget(self.Search_LE)

        self.Search_LE.textChanged.connect(self.SearchMethod)
        self.MenuBar()
        self.CreateTable()

    def MenuBar(self):
        Staff_Menubar.MenuBar(self)

    def log_out(self):
        self.close()

    def change_password(self):
        self.ChangePassword_window = ChangePassword(self.account_details)
        self.ChangePassword_window.exec_()

    def ReportError(self):
        Report_Error = ReportError()
        Report_Error.exec_()

    def BugReport(self):
        Report_Bug = ReportBug()
        Report_Bug.exec_()

        
        
    def CreateTable(self):
        with sqlite3.connect("Accounts.db") as db:
            cursor = db.cursor()
            sql = "SELECT FirstName,LastName FROM Accounts WHERE Username = '{0}'".format(self.account_details[0])
            cursor.execute(sql)
            values = list(cursor.fetchone())
            db.commit()



        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT StaffID FROM Staff WHERE FirstName = '{0}' AND Surname = '{1}'".format(values[0],values[1])
            cursor.execute(sql)
            staffids = list(cursor.fetchone())
            db.commit()

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT * FROM StaffHardware WHERE StaffID = '{0}' ".format(staffids[0])
            self.cursor.execute(sql)
            db.commit()
        

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

        self.vertical.addLayout(self.horizontal)
        self.vertical.addWidget(self.table)

        window_widget = QWidget()
        window_widget.setLayout(self.vertical)
        self.setCentralWidget(window_widget)
        
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
