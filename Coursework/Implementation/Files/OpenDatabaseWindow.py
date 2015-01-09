from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MenuBarAdmin import *
import sqlite3
from MainProgram import *

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
        
        
        DatabaseLbl = QLabel("Table")
        DatabaseLbl.setFont(QFont("Calibri",20))
        self.Database_CB = QComboBox()
        self.Database_CB.addItem('-')
        self.Database_CB.setFixedHeight(30)
        self.Database_CB.setFixedWidth(150)



        SearchLbl = QLabel("Search Fields")
        self.Search_LE = QLineEdit()
        self.Search_LE.setFixedWidth(150)
        self.Search_LE.setFixedHeight(25)
        SearchLbl.setFont(QFont("Calibri",20))

        self.Back_btn = QPushButton("Back")
        self.Back_btn.setFixedWidth(50)

        self.EditDatabase_btn = QPushButton("Edit Database")
        self.Add_btn = QPushButton("Add Data")
        self.Remove_btn = QPushButton("Remove Data")

        space = QLabel('')
        self.AddDatabase = QPushButton('Open Database')
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

        self.iconbutton = QPushButton()
        pixmap = QPixmap('search.png')
        ButtonIcon = QIcon(pixmap)
        self.iconbutton.setIcon(ButtonIcon)
        self.iconbutton.setIconSize(QSize(25,25))

        self.horizontal.addWidget(self.EditDatabase_btn)
        self.horizontal.addWidget(self.Add_btn)
        self.horizontal.addWidget(self.Remove_btn)
        self.grid.addWidget(self.iconbutton,2,3)

        self.verticle.addLayout(self.grid)
        self.verticle.addLayout(self.horizontal)
        self.Database_CB.activated.connect(self.ChosenTableMethod)
        self.EditDatabase_btn.clicked.connect(self.EditDatabaseClicked)
        self.Remove_btn.clicked.connect(self.DeleteRecordsClicked)
        self.iconbutton.clicked.connect(self.SearchMethod)
        

    def ChosenTableMethod(self):
        self.CurrentTable = (self.Database_CB.currentText())
        if self.exists == True:
            self.verticle.removeWidget(self.table)
        try:

            with sqlite3.connect("Volac.db") as db:
                    self.cursor = db.cursor()
                    sql = "SELECT * FROM {0}".format(self.CurrentTable)
                    self.cursor.execute(sql)

            col = [tuple[0] for tuple in self.cursor.description]
            self.table = QTableWidget(2,len(col))
                        
            self.table.setHorizontalHeaderLabels(col)
            self.table.setRowCount(0)

            ##If the editdb button is active

            if self.EditDB == True:             
                for self.row, form in enumerate(self.cursor): ##Inserts amount of rows needed, gets from database
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form): ##Inserts amount of columns needed
                        self.item = QTableWidgetItem(str(item)) 
                        self.table.setItem(self.row, self.column,self.item) ##Each item is added to a the table

            elif self.DeleteRC == True:
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
                        self.table.setCellWidget(count,last_column-1,self.delete_btn)   ##Adds a button to every row (count) and to the last column


            ##If the editdb is not active

                        
            else:
                for self.row, form in enumerate(self.cursor):
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form):
                        self.item = QTableWidgetItem(str(item))
                        self.item.setFlags(Qt.ItemIsEnabled) ##Item is no longer enabled (Toggled off) 
                        self.table.setItem(self.row, self.column,self.item)

                            
            self.verticle.addWidget(self.table)
            
            self.exists = True          ##This is important so table views do not keep being added, they get replaced
            
        except sqlite3.OperationalError:
            print('Table Could Not Be Made')
        self.currentcbvalue = self.CurrentTable

    def SearchMethod(self):
        text = self.Search_LE.text()
        if text == '':
            itemlist = self.table.findItems(text,Qt.MatchStartsWith)
            for count in range(len(itemlist)):
                itemlist[count].setBackgroundColor(QColor('White'))
        else:
            itemlist = self.table.findItems(text,Qt.MatchStartsWith)
            for count in range(len(itemlist)):
                itemlist[count].setBackgroundColor(QColor('Yellow'))

    def EditDatabaseClicked(self): ## Boolean statements to say whether the button has been clicked
        if self.EditDB == True:
            self.EditDB = False
        else:
            self.EditDB = True
            self.savechanges = QAction("Save Changes",self)
            self.tool_bar = QToolBar("Complete Changes")
            self.tool_bar.addAction(self.savechanges)
            self.addToolBar(self.tool_bar)
            
        self.ChosenTableMethod()

    def DeleteRecordsClicked(self):
        """Allows deletion of records in QTableWidget and Database"""
        if self.DeleteRC == True:
            self.DeleteRC = False
        else:
            self.DeleteRC = True
        
        self.ChosenTableMethod()
        
        
        
        

        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = OpenDatabase()
    launcher.show()
    launcher.raise_()
    launcher.resize(550,350)
    app.exec_()
