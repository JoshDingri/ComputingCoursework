from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MenuBarAdmin import *
import sqlite3
from MainProgram import *
from ConfirmDialog import *

class OpenDatabase(QMainWindow):
    """Opening database to add, edit and remove"""

    def __init__(self):
        super().__init__()
        self.EditDB = False
        self.DeleteRC = False
        self.exists = None
        self.currentcbvalue = None
        self.grid = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.verticle = QVBoxLayout()
        
        
        DatabaseLbl = QLabel(self)
        DatabaseLbl.setFont(QFont("Calibri",20))
        self.Database_CB = QComboBox(self)
        self.Database_CB.addItem('Select Table')
        self.Database_CB.setFixedHeight(30)
        self.Database_CB.setFixedWidth(150)


        SearchLbl = QLabel(self)
        self.Search_LE = QLineEdit(self)
        self.Search_LE.setFixedWidth(150)
        self.Search_LE.setFixedHeight(25)
        self.Search_LE.setPlaceholderText("Search Fields")
        SearchLbl.setFont(QFont("Calibri",20))

        self.Back_btn = QPushButton("Back",self)
        self.Back_btn.setFixedWidth(50)

        self.EditDatabase_btn = QPushButton("Edit Database",self)
        self.Add_btn = QPushButton("Add Data",self)
        self.Remove_btn = QPushButton("Remove Data",self)

        space = QLabel('                                      ',self)
        self.AddDatabase = QPushButton('Open Database',self)
        self.AddDatabase.setFont(QFont("Calibri",8))
        self.AddDatabase.setFixedWidth(80)
        self.AddDatabase.setFixedHeight(20)



        self.grid.addWidget(self.Back_btn,0,0)
        self.grid.addWidget(space,1,0)
        self.grid.addWidget(DatabaseLbl,1,1)
        self.grid.addWidget(self.Database_CB,1,2)
        self.grid.addWidget(self.AddDatabase,1,3)
        

        self.grid.addWidget(SearchLbl,2,1)
        self.grid.addWidget(self.Search_LE,2,2)

        self.grid.setVerticalSpacing(20)

        self.iconbutton = QLabel(self)

        pixmap = QPixmap('search.png')
        pixmap = pixmap.scaled(QSize(25,25),Qt.KeepAspectRatio)
        self.iconbutton.setPixmap(pixmap)

        self.horizontal.addWidget(self.EditDatabase_btn)
        self.horizontal.addWidget(self.Add_btn)
        self.horizontal.addWidget(self.Remove_btn)
        self.grid.addWidget(self.iconbutton,2,3)

        self.table = QTableView()

        self.verticle.addLayout(self.grid)
        self.verticle.addLayout(self.horizontal)
        self.verticle.addWidget(self.table)

        window_widget = QWidget()
        window_widget.setLayout(self.verticle)
        self.setCentralWidget(window_widget)
        
        self.Database_CB.activated.connect(self.ChosenTableMethod) 
        self.Remove_btn.clicked.connect(self.DeleteRecordsClicked)
        self.Search_LE.textChanged.connect(self.SearchMethod)
        self.EditDatabase_btn.clicked.connect(self.EditDatabaseClicked)

        rspacer = QWidget()
        rspacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        lspacer = QWidget()
        lspacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        
        self.savechanges = QAction("Save Changes",self)
        self.cancel = QAction("Cancel",self)
        self.EditDB_ToolBar = QToolBar("Complete Changes")
        self.EditDB_ToolBar.addWidget(lspacer)
        self.EditDB_ToolBar.addAction(self.savechanges)
        self.EditDB_ToolBar.addAction(self.cancel)
        self.EditDB_ToolBar.addWidget(rspacer)
        self.EditDB_ToolBar.setIconSize(QSize(50,50))
        self.addToolBar(Qt.BottomToolBarArea,self.EditDB_ToolBar)
        self.EditDB_ToolBar.setFont(QFont('',11))
        self.EditDB_ToolBar.setVisible(False)
        
        self.savechanges.triggered.connect(self.EditDB_SaveChanges)
        self.cancel.triggered.connect(self.EditDB_Cancel)

        self.ButtonStyleSheet =  ("""QPushButton{
                    color: #333;
                    border: 2px solid #555;
                    border-radius: 11px;
                    padding: 5px;
                    background: qradialgradient(cx: 0.3, cy: -0.4,
                    fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #fff, stop: 1 #888);
                    min-width: 80px;
                    }"""
                             
                    """QPushButton:hover{
                    background: qradialgradient(cx: 0.3, cy: -0.4,
                    fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #fff, stop: 1 #bbb);
                    }"""

                    """QPushButton:pressed {
                    background: qradialgradient(cx: 0.4, cy: -0.1,
                    fx: 0.4, fy: -0.1,
                    radius: 1.35, stop: 0 #fff, stop: 1 #ddd);
                    }""")

                    
        self.EditDatabase_btn.setStyleSheet(self.ButtonStyleSheet)
        self.Add_btn.setStyleSheet(self.ButtonStyleSheet)
        self.Remove_btn.setStyleSheet(self.ButtonStyleSheet)
                        

                        
        

    def ChosenTableMethod(self):
        columncount = 0
        self.table.deleteLater()
        
        self.CurrentTable = (self.Database_CB.currentText())
        if self.exists == True:
            self.verticle.removeWidget(self.table)
        try:

            with sqlite3.connect("Volac.db") as db:
                    self.cursor = db.cursor()
                    sql = "SELECT * FROM {0}".format(self.CurrentTable)
                    self.cursor.execute(sql)

            col = [tuple[0] for tuple in self.cursor.description]
            self.table = QTableView()
            self.table.addDatabase("Volac.db")
                        
            self.table.setHorizontalHeader(col)
            self.table.setRowCount(0)

            ##If the editdb button is active

            if self.EditDB == True:             
                for self.row, form in enumerate(self.cursor): ##Inserts amount of rows needed, gets from database
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form): ##Inserts amount of columns needed
                        self.item = QTableWidgetItem(str(item))
                        self.table.setItem(self.row, self.column,self.item) ##Each item is added to a the table
                        self.table.horizontalHeader().setStretchLastSection(True)
                

            elif self.DeleteRC == True:
                self.Deletebtn_list = []
                self.counter = 0
                for self.row, form in enumerate(self.cursor):
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form):
                        self.item = QTableWidgetItem(str(item))
                        self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                        self.table.setItem(self.row, self.column,self.item)
                self.table.insertColumn(self.column+1)
                last_column = self.table.columnCount()
                for count in range(self.table.rowCount()): 
                        self.delete_btn = QPushButton('Delete')
                        self.Deletebtn_list.append(self.delete_btn)
                        self.table.setCellWidget(count,last_column-1,self.delete_btn)   ##Adds a button to every row (count) and to the last column
                        self.delete_btn.clicked.connect(self.Delete_btnclicked)
                        self.counter +=1
                        self.table.horizontalHeader().setStretchLastSection(True)


            ##If the editdb is not active

                        
            else:
                for self.row, form in enumerate(self.cursor):
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form):
                        
                        if self.CurrentTable == 'Staff':
                            if self.column == 4:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    sql = "SELECT DepartmentName from Department WHERE DepartmentID ='{}'".format(item)
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setStretchLastSection(True)
                                continue
                            if self.column == 5:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    sql = "SELECT AddressLine3 from Location WHERE LocationID ='{}'".format(item)
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setStretchLastSection(True)
                                continue
                            
                        elif self.CurrentTable == 'Department': 
                            if self.column == 7:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    sql = "SELECT DeviceName from DeviceType WHERE DeviceID ='{}'".format(item)
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setStretchLastSection(True)
                                continue
                                
                            if self.column == 8:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    sql = "SELECT HardwareModelName from HardwareModel WHERE HardwareModelID ='{}'".format(item)
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setStretchLastSection(True)
                                continue

                        elif self.CurrentTable == 'HardwareModel': 
                            if self.column == 2:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    sql = "SELECT HardwareMakeName from HardwareMake WHERE HardwareMakeID ='{}'".format(item)
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setStretchLastSection(True)
                                continue

                        elif self.CurrentTable == 'StaffHardware': 
                            if self.column == 2:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    sql = "SELECT Surname,FirstName from Staff WHERE StaffID ='{}'".format(item)
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute(sql)
                                    Foreign_Item = list(cursor.fetchall())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setStretchLastSection(True)
                                continue
                                
##                            if self.column == 3:
##                                with sqlite3.connect("Volac.db") as db:
##                                    cursor = db.cursor()
##                                    sql = "SELECT FirstName from Hardware WHERE HardwareID ='{}'".format(item)
##                                    cursor.execute("PRAGMA foreign_keys = ON")
##                                    cursor.execute(sql)
##                                    Foreign_Item = list(cursor.fetchall())
##                                    db.commit()
##                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
##                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
##                                self.table.setItem(self.row, self.column,self.item)
##                                self.table.horizontalHeader().setStretchLastSection(True)


                        






                                
                        self.item = QTableWidgetItem(str(item))
                        self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                        self.table.setItem(self.row, self.column,self.item)
                        self.table.horizontalHeader().setStretchLastSection(True)

                            
            self.verticle.addWidget(self.table)
            
            self.exists = True          ##This is important so table views do not keep being added, they get replaced
            
        except sqlite3.OperationalError:
            print('Table Could Not Be Made')
        self.currentcbvalue = self.CurrentTable
        self.table.cellChanged.connect(self.cellchanged)
        self.table.cellClicked.connect(self.cellclicked)

    def FilterTable(self):
        pass



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

    def cellchanged(self):
        try:
            self.Edited_data = self.table.currentItem().text()
            self.IDtoChange = (self.table.item(self.table.currentRow(),0).text())
            self.colnumber = int(self.table.currentColumn())
            self.Columnname = (self.table.horizontalHeaderItem(self.colnumber).text())
            self.Columnname = (self.Columnname + '=?')
        except AttributeError:
            pass
        
        

    def cellclicked(self):
        self.CurrentCell = (self.table.currentItem().text())
        self.ID = (self.table.horizontalHeaderItem(0).text())
            
        

    def EditDatabaseClicked(self): ## Boolean statements to say whether the button has been clicked
        self.EditDatabase_btn.setStyleSheet("""
                                            color: #333;
                                            background-color: #E6CCCC;
                                            border: 2px solid #555;
                                            border-radius: 11px;
                                            padding: 5px;
                                            min-width: 80px;
                                            """)
        
        self.EditDB = True
        self.EditDB_ToolBar.setVisible(True)
        self.ChosenTableMethod()

    def EditDB_SaveChanges(self):
        self.EditDatabase_btn.setStyleSheet(self.ButtonStyleSheet)
        try:
        
            with sqlite3.connect("Volac.db") as db:
                cursor = db.cursor()
                sql = "update {0} set {1} where {2}={3}".format(self.currentcbvalue,self.Columnname,self.ID,self.IDtoChange)
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute(sql,(self.Edited_data,)) ################ FIX FOR sqlite3.ProgrammingError: Incorrect number of bindings supplied
                db.commit()

            self.EditDB = False
            self.EditDB_ToolBar.setVisible(False)
            self.ChosenTableMethod()

        except (AttributeError,sqlite3.OperationalError):
            pass
            


    def EditDB_Cancel(self):
        self.EditDatabase_btn.setStyleSheet(self.ButtonStyleSheet)
        self.EditDB = False
        self.EditDB_ToolBar.setVisible(False)

        self.Edited_data = None
        self.IDtoChange = None
        self.colnumber = None
        self.Columnname = None
        self.Columnname = None
        
        self.ChosenTableMethod()

    def DeleteRecordsClicked(self):
        """Allows deletion of records in QTableWidget and Database"""
        if self.DeleteRC == True:
            self.Remove_btn.setStyleSheet(self.ButtonStyleSheet)
            self.DeleteRC = False
        else:
            self.DeleteRC = True
            self.Remove_btn.setStyleSheet("""
                                        color: #333;
                                        background-color: #E6CCCC;
                                        border: 2px solid #555;
                                        border-radius: 11px;
                                        padding: 5px;
                                        min-width: 80px;
                                            """)
            
        
        self.ChosenTableMethod()

    def Delete_btnclicked(self):
        button = qApp.focusWidget()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            self.DeleteRow = index.row()
        self.WarningDialog = Warning_Dialog()
        self.WarningDialog.YesBtn.clicked.connect(self.Confirm_Deletion)
        self.WarningDialog.NoBtn.clicked.connect(self.Cancel_Deletion)
        self.WarningDialog.exec()




    def Confirm_Deletion(self):
        self.WarningDialog.reject()
        self.IDtoChange = (self.table.item(self.DeleteRow,0).text())
        self.ID = (self.table.horizontalHeaderItem(0).text())
        
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "delete from {0} where {1}={2}".format(self.currentcbvalue,self.ID,self.IDtoChange)
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(sql)
            db.commit()
        self.ChosenTableMethod()
        
    def Cancel_Deletion(self):
        self.WarningDialog()
        
        
        
        

        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = OpenDatabase()
    launcher.show()
    launcher.raise_()
    launcher.resize(550,350)
    app.exec_()
