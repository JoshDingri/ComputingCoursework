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
        self.setMaximumSize(1000,500)
        self.setMinimumSize(750,400)
        
        self.setWindowTitle("Staff Database")
        self.horizontal_layout = QHBoxLayout()
        self.vertical_layout = QVBoxLayout()
        self.account_details = account_details

        SearchLbl = QLabel(self)
        self.Search_LE = QLineEdit(self)
        self.Search_LE.setFixedWidth(150)
        self.Search_LE.setFixedHeight(25)
        self.Search_LE.setPlaceholderText("Search Fields")
        SearchLbl.setFont(QFont("Calibri",20))
        
        self.iconbutton = QLabel(self)

        with sqlite3.connect("Accounts.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT FirstName,LastName FROM Accounts WHERE Username =?",(self.account_details[0],))
            self.values = list(cursor.fetchone())
            db.commit()

        name_lbl = QLabel("        Welcome {0}! These Are Your Current Hardware Devices".format(self.values[0]))
        name_lbl.setFont(QFont("Arial",14))
        self.horizontal_layout.addWidget(name_lbl)
        self.horizontal_layout.addStretch(1)



        pixmap = QPixmap('search.png')
        pixmap = pixmap.scaled(QSize(25,25),Qt.KeepAspectRatio)
        self.iconbutton.setPixmap(pixmap)


        self.horizontal_layout.addWidget(self.iconbutton)
        self.horizontal_layout.addWidget(self.Search_LE)

        self.Search_LE.textChanged.connect(self.SearchMethod)
        self.MenuBar()
        self.CreateTable()

    def MenuBar(self):
        StaffMenuBar = Staff_Menubar()
        self.setMenuBar(StaffMenuBar)
        StaffMenuBar.Logout.triggered.connect(self.log_out)
        StaffMenuBar.ChangePassword.triggered.connect(self.change_password)

        StaffMenuBar.ReportInformation.triggered.connect(self.ReportError)
        StaffMenuBar.ReportBug.triggered.connect(self.BugReport)

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



        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT StaffID FROM Staff WHERE FirstName =? AND Surname =?",(self.values[0],self.values[1],))
            staffids = list(cursor.fetchone())
            db.commit()

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            self.cursor.execute("SELECT * FROM StaffHardware WHERE StaffID =?",(staffids[0],))
            db.commit()
        

        col = [tuple[0] for tuple in self.cursor.description] #Adds column headers to tuple
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

        self.vertical_layout.addLayout(self.horizontal_layout)
        self.vertical_layout.addWidget(self.table)

        window_widget = QWidget()
        window_widget.setLayout(self.vertical_layout)
        self.setCentralWidget(window_widget)
        
    def SearchMethod(self):
        """Hides rows that do not match the search input"""
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
