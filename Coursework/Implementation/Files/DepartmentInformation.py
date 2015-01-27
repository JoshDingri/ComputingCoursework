from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class DepartmentInformation(QMainWindow):
    """Managers table view"""

    def __init__(self):
        super().__init__()
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

        self.table = QTableWidget()

        self.verticle.addLayout(self.grid)
        self.verticle.addLayout(self.horizontal)
        self.verticle.addWidget(self.table)

        window_widget = QWidget()
        window_widget.setLayout(self.verticle)
        self.setCentralWidget(window_widget)

        self.Database_CB.activated.connect(self.CreateTable) 

    def CreateTable(self):
        self.table.deleteLater()
        self.CurrentTable = (self.Database_CB.currentText())

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT * FROM {0}".format(self.CurrentTable)
            self.cursor.execute(sql)
            
        col = [tuple[0] for tuple in self.cursor.description]
        self.table = QTableWidget(2,len(col))
                        
        self.table.setHorizontalHeaderLabels(col)
        self.table.setRowCount(0)

        for self.row, form in enumerate(self.cursor): ##Inserts amount of rows needed, gets from database
                self.table.insertRow(self.row)
                for self.column, item in enumerate(form): ##Inserts amount of columns needed
                    self.item = QTableWidgetItem(str(item))
                    self.item.setFlags(Qt.ItemIsEnabled)
                    self.table.setItem(self.row, self.column,self.item) ##Each item is added to a the table
                    self.table.horizontalHeader().setStretchLastSection(True)

        self.verticle.addWidget(self.table)
            
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = DepartmentInformation()
    launcher.show()
    launcher.raise_()
    app.exec_()
