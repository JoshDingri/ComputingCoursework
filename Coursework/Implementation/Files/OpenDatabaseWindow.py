from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MenuBarAdmin import *
import sqlite3


class OpenDatabase(QMainWindow):
    """Opening database to add, edit and remove"""

    def __init__(self):
        super().__init__()
        self.EditDB = False
        self.exists = None
        self.currentcbvalue = None
        self.grid = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.verticle = QVBoxLayout()
        
        
        DatabaseLbl = QLabel("Table")
        DatabaseLbl.setFont(QFont("Calibri",20))
        self.Database_CB = QComboBox()
        self.Database_CB.setFixedHeight(30)
        self.Database_CB.setFixedWidth(150)
        self.Database_CB.addItems(self.Items)



        SearchLbl = QLabel("Search Fields")
        Search_LE = QLineEdit()
        Search_LE.setFixedWidth(150)
        Search_LE.setFixedHeight(25)
        SearchLbl.setFont(QFont("Calibri",20))

        self.Back_btn = QPushButton("Back")
        self.Back_btn.setFixedWidth(50)

        self.EditDatabase_btn = QPushButton("Edit Database")
        self.Add_btn = QPushButton("Add Data")
        Remove_btn = QPushButton("Remove Data")

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
        self.grid.addWidget(Search_LE,2,2)

        self.grid.setVerticalSpacing(20)

        self.horizontal.addWidget(self.EditDatabase_btn)
        self.horizontal.addWidget(self.Add_btn)
        self.horizontal.addWidget(Remove_btn)

        self.verticle.addLayout(self.grid)
        self.verticle.addLayout(self.horizontal)
        self.Database_CB.activated.connect(self.ChosenTableMethod)
        self.EditDatabase_btn.clicked.connect(self.EditDatabaseClicked)

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

            if self.EditDB == True:
                for self.row, form in enumerate(self.cursor):
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form):
                        self.item = QTableWidgetItem(str(item))
                        self.table.setItem(self.row, self.column,self.item)

            else:            
                for self.row, form in enumerate(self.cursor):
                    self.table.insertRow(self.row)
                    for self.column, item in enumerate(form):
                        self.item = QTableWidgetItem(str(item))
                        self.item.setFlags(Qt.ItemIsEnabled)
                        self.table.setItem(self.row, self.column,self.item)
                            
            self.verticle.addWidget(self.table)
            self.exists = True
        except sqlite3.OperationalError:
            print('Table Could Not Be Made')
        self.currentcbvalue = self.CurrentTable

    def EditDatabaseClicked(self):
        if self.EditDB == True:
            self.EditDB = False
        else:
            self.EditDB = True
        self.ChosenTableMethod()
 

        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = OpenDatabase()
    launcher.show()
    launcher.raise_()
    launcher.resize(550,350)
    app.exec_()
