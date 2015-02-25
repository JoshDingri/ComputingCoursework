from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MenuBarAdmin import *
import sqlite3
from MainProgram import *
from PopupDialog import *
from ConfirmDialog import *

class OpenDatabase(QWidget):
    """Provides the GUI needed to add/edit/remove data from the database"""

    def __init__(self):
        super().__init__()
        self.EditDB = False
        self.DeleteRC = False
        self.exists = None #keeps track of if a table exists to ensure only one table is shown at a time
        self.currentcbvalue = None
        self.Grid_Layout = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.Verical_Layout = QVBoxLayout()
        
        self.PushButtonStyles =  ("""QPushButton{
                                min-height: 1.7em;
                                font: 14px;
                                color: black;
                                background-color: #F5F5F5;
                                padding: 1px;
                                border-style: outset;
                                border-radius: 8px;
                                border-width: 2px;
                                border-color: green;}
                             
                            QPushButton:pressed {
                                background-color: #F2E4E4
                            }""")
        
                
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
        self.Back_btn.setStyleSheet(self.PushButtonStyles)

        self.EditDatabase_btn = QPushButton("Edit Database",self)
        self.EditDatabase_btn.setStyleSheet(self.PushButtonStyles)
        self.Add_btn = QPushButton("Add Data",self)
        self.Add_btn.setStyleSheet(self.PushButtonStyles)
        self.Remove_btn = QPushButton("Remove Data",self)
        self.Remove_btn.setStyleSheet(self.PushButtonStyles)

        space = QLabel('                                      ',self)
        self.AddDatabase = QPushButton('Open Database',self)
        self.AddDatabase.setFont(QFont("Calibri",8))
        self.AddDatabase.setFixedWidth(80)
        self.AddDatabase.setFixedHeight(25)



        self.Grid_Layout.addWidget(self.Back_btn,0,0)
        self.Grid_Layout.addWidget(space,1,0)
        self.Grid_Layout.addWidget(DatabaseLbl,1,1)
        self.Grid_Layout.addWidget(self.Database_CB,1,2)
        self.Grid_Layout.addWidget(self.AddDatabase,1,3)
        

        self.Grid_Layout.addWidget(SearchLbl,2,1)
        self.Grid_Layout.addWidget(self.Search_LE,2,2)

        self.Grid_Layout.setVerticalSpacing(20)

        self.iconbutton = QLabel(self)

        pixmap = QPixmap('search.png')
        pixmap = pixmap.scaled(QSize(25,25),Qt.KeepAspectRatio)
        self.iconbutton.setPixmap(pixmap)

        self.horizontal.addWidget(self.EditDatabase_btn)
        self.horizontal.addWidget(self.Add_btn)
        self.horizontal.addWidget(self.Remove_btn)
        self.Grid_Layout.addWidget(self.iconbutton,2,3)

        self.table = QTableWidget()

        self.Verical_Layout.addLayout(self.Grid_Layout)
        self.Verical_Layout.addLayout(self.horizontal)
        self.Verical_Layout.addWidget(self.table)

        self.setLayout(self.Verical_Layout)
        
        self.Database_CB.activated.connect(self.ChosenTableMethod) 
        self.Remove_btn.clicked.connect(self.DeleteRecordsClicked)
        self.Search_LE.textChanged.connect(self.SearchMethod)
        self.EditDatabase_btn.clicked.connect(self.EditDatabaseClicked)

        rspacer = QWidget() # Pushes toolbar buttons into the center
        rspacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        lspacer = QWidget() # Pushes toolbar buttons into the center
        lspacer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        
        self.savechanges = QAction("Save Changes",self)
        self.savechanges.setShortcut("CTRL+S")
        self.cancel = QAction("Cancel",self)
        self.cancel.setShortcut("CTRL+X")
        self.EditDB_ToolBar = QToolBar("Complete Changes")
        self.EditDB_ToolBar.addWidget(lspacer)
        self.EditDB_ToolBar.addAction(self.savechanges)
        self.EditDB_ToolBar.addAction(self.cancel)
        self.EditDB_ToolBar.addWidget(rspacer)
        self.EditDB_ToolBar.setIconSize(QSize(50,50))
        self.Verical_Layout.addWidget(self.EditDB_ToolBar)
        self.EditDB_ToolBar.setFont(QFont('',11))
        self.EditDB_ToolBar.setVisible(False)
        
        self.savechanges.triggered.connect(self.EditDB_SaveChanges)
        self.cancel.triggered.connect(self.EditDB_Cancel)


           

                        
        

    def ChosenTableMethod(self):
        columncount = 0        
        self.CurrentTable = (self.Database_CB.currentText())
        if self.CurrentTable == 'Select Table':
            return

        
        if self.exists == True:
            self.Verical_Layout.removeWidget(self.table)
        try:
            self.table.deleteLater()
            with sqlite3.connect("Volac.db") as db:
                    self.cursor = db.cursor()
                    self.cursor.execute("SELECT * FROM {}".format(self.CurrentTable))
                    db.commit()

            col = [tuple[0] for tuple in self.cursor.description] #Adds column headers to tuple
            self.table = QTableWidget(2,len(col))
                        
            self.table.setHorizontalHeaderLabels(col)
            self.table.setRowCount(0)

            ##If the editdb button is pressed

            if self.EditDB == True:             
                for self.row, form in enumerate(self.cursor): ##Inserts amount of rows needed, gets from database
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form): ##Inserts amount of columns needed
                        self.item = QTableWidgetItem(str(item))
                        self.item.setFont(QFont("Arial",12))
                        self.table.setItem(self.row, self.column,self.item) ##Each item is added to a the table
                        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                
            ##If the deletedb button is pressed
            elif self.DeleteRC == True:
                self.Deletebtn_list = []
                self.counter = 0
                for self.row, form in enumerate(self.cursor):
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form):
                        self.item = QTableWidgetItem(str(item))
                        self.item.setFont(QFont("Arial",12))
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
                        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)


            ##If no buttons are active                      
            else:
                for self.row, form in enumerate(self.cursor):
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form):
                        CurrentHeader = (self.table.horizontalHeaderItem(self.column).text())
                        
                        ## The below if statements provide a user friendly display of foreign keys##
                        
                        if CurrentHeader == 'DepartmentID' and self.column != 0:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute("SELECT DepartmentName from Department WHERE DepartmentID =?",(item,))
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFont(QFont("Arial",12))
                                self.item.setTextAlignment(Qt.AlignCenter)
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                                continue
                        elif CurrentHeader == 'LocationID' and self.column != 0:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute("SELECT AddressLine3 from Location WHERE LocationID =?",(item,))
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFont(QFont("Arial",12))
                                self.item.setTextAlignment(Qt.AlignCenter)
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                                continue
                            
                        elif CurrentHeader == 'DeviceID' and self.column != 0: 
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute("SELECT DeviceName from DeviceType WHERE DeviceID =?",(item,))
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFont(QFont("Arial",12))
                                self.item.setTextAlignment(Qt.AlignCenter)
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                                continue
                                
                        elif CurrentHeader == 'HardwareModelID' and self.column != 0:
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute("SELECT HardwareModelName from HardwareModel WHERE HardwareModelID =?",(item,))
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFont(QFont("Arial",12))
                                self.item.setTextAlignment(Qt.AlignCenter)
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                                continue

                        elif CurrentHeader == 'HardwareMakeID' and self.column != 0: 
                                with sqlite3.connect("Volac.db") as db:
                                    cursor = db.cursor()
                                    cursor.execute("PRAGMA foreign_keys = ON")
                                    cursor.execute("SELECT HardwareMakeName from HardwareMake WHERE HardwareMakeID =?",(item,))
                                    Foreign_Item = list(cursor.fetchone())
                                    db.commit()
                                self.item = QTableWidgetItem(str(Foreign_Item[0]))
                                self.item.setFont(QFont("Arial",12))
                                self.item.setTextAlignment(Qt.AlignCenter)
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                                continue

                        elif CurrentHeader == 'StaffID' and self.column != 0: 
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
                                self.item.setFont(QFont("Arial",12))
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
                                self.item.setFont(QFont("Arial",12))
                                self.item.setTextAlignment(Qt.AlignCenter)
                                self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                                self.table.setItem(self.row, self.column,self.item)
                                self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                                continue


                        






                                
                        self.item = QTableWidgetItem(str(item))
                        self.item.setFont(QFont("Arial",12))
                        self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off)
                        self.item.setTextAlignment(Qt.AlignCenter)
                        self.table.setItem(self.row, self.column,self.item)
                        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)


                            
            self.Verical_Layout.addWidget(self.table)
            
            self.exists = True          ##This is important so table views do not keep being added, they get replaced
            
        except:
            BlankFieldsWarning = Presence_Dialog("{0:^50}".format("Tables could not be made."))
            BlankFieldsWarning.exec_()
        self.currentcbvalue = self.CurrentTable
        self.table.cellChanged.connect(self.cellchanged)
        self.table.cellClicked.connect(self.cellclicked)


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
            
        

    def EditDatabaseClicked(self):   
        self.EditDB = True ## Boolean statements to say whether the button has been clicked  
        self.EditDB_ToolBar.setVisible(True)
        self.ChosenTableMethod()

    def EditDB_SaveChanges(self):
        try:
        
            with sqlite3.connect("Volac.db") as db:
                cursor = db.cursor()
                sql = "update {0} set {1} where {2}={3}".format(self.currentcbvalue,self.Columnname,self.ID,self.IDtoChange)
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute(sql,(self.Edited_data,)) 
                db.commit()

            self.EditDB = False
            self.EditDB_ToolBar.setVisible(False)
            self.ChosenTableMethod()

        except (AttributeError,sqlite3.OperationalError):
            pass
            


    def EditDB_Cancel(self):
        """Resets all changes made"""
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
            self.DeleteRC = False
        else:
            self.DeleteRC = True
            
        
        self.ChosenTableMethod()

    def Delete_btnclicked(self):
        button = qApp.focusWidget()
        index = self.table.indexAt(button.pos())
        if index.isValid():
            self.DeleteRow = index.row()
        self.WarningDialog = Warning_Dialog()
        self.WarningDialog.YesBtn.clicked.connect(self.Confirm_Deletion)
        self.WarningDialog.exec()




    def Confirm_Deletion(self):
        self.WarningDialog.reject()
        self.IDtoChange = (self.table.item(self.DeleteRow,0).text())
        self.ID = (self.table.horizontalHeaderItem(0).text())
        try:
        
            with sqlite3.connect("Volac.db") as db:
                cursor = db.cursor()
                sql = "delete from {0} where {1}={2}".format(self.currentcbvalue,self.ID,self.IDtoChange)
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute(sql)
                db.commit()
        except sqlite3.IntegrityError:
            BlankFieldsWarning = Presence_Dialog("{0:^50}".format("FOREIGN KEY IS REFERENCED SOMEWHERE ELSE.\n                        CANNOT BE DELETED"))
            BlankFieldsWarning.exec_()
        self.ChosenTableMethod()
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = OpenDatabase()
    launcher.show()
    launcher.raise_()
    launcher.resize(550,350)
    app.exec_()
