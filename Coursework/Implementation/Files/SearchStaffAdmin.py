from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3


class SearchStaff(QMainWindow):
    """Admin search staff window"""

    def __init__(self):
        super().__init__()

        self.grid = QGridLayout()
        self.verticle = QVBoxLayout()
                
        DatabaseLbl = QLabel("Department")
        DatabaseLbl.setFont(QFont("Calibri",20))
        self.Database_CB = QComboBox()
        self.Database_CB.setFixedHeight(30)
        self.Database_CB.setFixedWidth(150)
        
        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT DepartmentName FROM Department"
            self.cursor.execute(sql)
            db.commit()
            
        field_names = []
        
        for self.row, form in enumerate(self.cursor): 
                for self.column, item in enumerate(form): 
                    field_names.append(item)

        self.Database_CB.addItems(field_names)
        

        SearchLbl = QLabel("Name")
        self.Search_LE = QLineEdit()
        self.Search_LE.setFixedWidth(150)
        self.Search_LE.setFixedHeight(25)
        SearchLbl.setFont(QFont("Calibri",20))

        self.Back_btn = QPushButton("Back")
        self.Back_btn.setFixedWidth(50)


        space = QLabel('')
        
        self.grid.addWidget(self.Back_btn,0,0)
        self.grid.addWidget(space,1,0)
        self.grid.addWidget(DatabaseLbl,1,1)
        self.grid.addWidget(self.Database_CB,1,2)
        self.grid.addWidget(space,1,3)

        self.grid.addWidget(SearchLbl,2,1)
        self.grid.addWidget(self.Search_LE,2,2)

        self.grid.setVerticalSpacing(20)

        self.verticle.addLayout(self.grid)

        window_widget = QWidget()
        window_widget.setLayout(self.verticle)
        self.setCentralWidget(window_widget)
        self.Database_CB.activated.connect(self.ChosenDepartment)

    def ChosenDepartment(self):
        self.department = self.Database_CB.currentText()

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT DepartmentID FROM Department WHERE DepartmentName='{0}'".format(self.department)
            self.cursor.execute(sql)
            db.commit()
            
        for self.row, form in enumerate(self.cursor): 
                for self.column, item in enumerate(form): 
                    self.DepartmentID = item

        print(self.DepartmentID)
        
        self.Search_LE.textChanged.connect(self.ShowResults)

    
    def ShowResults(self):
        self.searched_name = (self.Search_LE.text())
        self.search_results_table = QTableView()
        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT * FROM Staff WHERE FirstName ={0}".format(self.searched_name)
            
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = SearchStaff()
    launcher.show()
    launcher.raise_()
    app.exec_()

