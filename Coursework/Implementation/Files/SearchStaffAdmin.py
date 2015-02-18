from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
import string


class SearchStaff(QMainWindow):
    """Admin search staff window"""

    def __init__(self):
        super().__init__()
        self.resize(700,500)

        self.grid = QGridLayout()
        self.verticle = QVBoxLayout()
                
        DatabaseLbl = QLabel("Select Department:")
        DatabaseLbl.setFont(QFont("Calibri",19))
        self.Database_CB = QComboBox()
        self.Database_CB.setFixedHeight(27)
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
        self.Database_CB.setCurrentIndex(0)
        

        SearchLbl = QLabel("Enter First Name:")
        self.Search_LE = QLineEdit()
        self.Search_LE.setFixedWidth(150)
        self.Search_LE.setFixedHeight(25)
        SearchLbl.setFont(QFont("Calibri",19))

        self.Back_btn = QPushButton("Back")
        self.Back_btn.setFixedWidth(50)


        space = QLabel('')
        self.search_results_table = QTableWidget()

        self.search_button = QPushButton("Search")
        
        self.grid.addWidget(self.Back_btn,0,0)
        self.grid.addWidget(space,1,0)
        self.grid.addWidget(DatabaseLbl,1,1)
        self.grid.addWidget(self.Database_CB,1,2)
        self.grid.addWidget(space,1,3)

        self.grid.addWidget(SearchLbl,2,1)
        self.grid.addWidget(self.Search_LE,2,2)
        self.grid.addWidget(self.search_button)

        self.grid.setVerticalSpacing(20)

        self.verticle.addLayout(self.grid)
        self.verticle.addWidget(self.search_results_table)

        window_widget = QWidget()
        window_widget.setLayout(self.verticle)
        self.setCentralWidget(window_widget)
        self.default_table()
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
        self.default_table()
        
        self.search_button.clicked.connect(self.ShowResults)

    def default_table(self):
        self.department = self.Database_CB.currentText()

        with sqlite3.connect("Volac.db") as db:
            self.cursor = db.cursor()
            sql = "SELECT DepartmentID FROM Department WHERE DepartmentName='{0}'".format(self.department)
            self.cursor.execute(sql)
            db.commit()
            
        for self.row, form in enumerate(self.cursor): 
                for self.column, item in enumerate(form): 
                    self.DepartmentID = item
                    
        with sqlite3.connect("Volac.db") as db:
            self.cursorStaff = db.cursor()
            sql = "SELECT Surname,FirstName FROM Staff WHERE DepartmentID ='{0}'".format(self.DepartmentID)
            self.cursorStaff.execute(sql)
            db.commit()

        self.search_results_table.deleteLater()
        self.search_results_table = QTableWidget(2,1)
                        
        self.search_results_table.setHorizontalHeaderLabels('')
        self.search_results_table.setRowCount(0)

        b = "(',)"

        self.pushbuttons = []
        self.names = []
                
        for self.row, item in enumerate(self.cursorStaff):
            self.search_results_table.insertRow(self.row)
            self.names.append(item)
            self.item = str(item)
            for i in range(0,len(b)):
                self.item = self.item.replace(b[i],"")
            self.item = self.item.replace(" ",", ")
            self.item = "{0}\n{1}                                                                                                              ".format(self.item,self.department)
            self.buttonrow = QPushButton(self.item)

            self.buttonrow.setIcon(QIcon("arrow.png"))
            self.buttonrow.setIconSize(QSize(30,30))
            self.buttonrow.setStyleSheet("font-size: 15px")
            self.buttonrow.setLayoutDirection(Qt.RightToLeft)

            self.pushbuttons.append(self.buttonrow)
            self.pushbuttons[self.row].clicked.connect(self.ButtonClicked)
                
                
            self.search_results_table.setCellWidget(self.row, self.column,self.pushbuttons[self.row])
            self.search_results_table.resizeRowsToContents()
            self.search_results_table.horizontalHeader().setStretchLastSection(True)


                                    

                            
        self.verticle.addWidget(self.search_results_table)





    
    def ShowResults(self):
        self.searched_name = (self.Search_LE.text())
        print(self.searched_name)
        if self.searched_name == '':
            self.default_table()
        

        else:        
                    with sqlite3.connect("Volac.db") as db:
                        self.cursorStaff = db.cursor()
                        sql = "SELECT Surname,FirstName FROM Staff WHERE DepartmentID ='{0}' AND FirstName LIKE '{1}%' ".format(self.DepartmentID,self.searched_name)
                        self.cursorStaff.execute(sql)
                        db.commit()
                                
                        self.search_results_table.deleteLater()
                        self.search_results_table = QTableWidget(2,1)
                                        
                        self.search_results_table.setHorizontalHeaderLabels('')
                        self.search_results_table.setRowCount(0)

                        b = "(',)"

                        self.pushbuttons = []
                        self.names = []
                                
                        for self.row, item in enumerate(self.cursorStaff):
                            self.search_results_table.insertRow(self.row)
                            self.names.append(item)
                            self.item = str(item)
                            for i in range(0,len(b)):
                                self.item = self.item.replace(b[i],"")
                            self.item = self.item.replace(" ",", ")
                            self.item = "{0}\n{1}                                                                                                              ".format(self.item,self.department)
                            self.buttonrow = QPushButton(self.item)
   
                            self.buttonrow.setIcon(QIcon("arrow.png"))
                            self.buttonrow.setIconSize(QSize(30,30))
                            self.buttonrow.setStyleSheet("font-size: 15px")
                            self.buttonrow.setLayoutDirection(Qt.RightToLeft)
            
                            self.pushbuttons.append(self.buttonrow)
                            self.pushbuttons[self.row].clicked.connect(self.ButtonClicked)
                                
                                
                            self.search_results_table.setCellWidget(self.row, self.column,self.pushbuttons[self.row])
                            self.search_results_table.resizeRowsToContents()
                            self.search_results_table.horizontalHeader().setStretchLastSection(True)


                                    

                            
        self.verticle.addWidget(self.search_results_table)
            


    def ButtonClicked(self,rownum):        
        self.dialog = QDialog()
        self.dialog.resize(720,300)

        button = qApp.focusWidget()
        index = self.search_results_table.indexAt(button.pos())
        if index.isValid():
            self.rownum = index.row()

        self.vertical = QVBoxLayout()
        
        Fullname = str(self.names[self.rownum])
        split = [x.strip() for x in Fullname.split(',')]


        Chars = ")'('"

        FirstName = split[1]
        Surname = split[0]
        
        for i in range(0,len(Chars)):
            FirstName = FirstName.replace(Chars[i],"")

        for i in range(0,len(Chars)):
            Surname = Surname.replace(Chars[i],"")
            
        

        with sqlite3.connect("Volac.db") as db:
            self.details_cursor = db.cursor()
            sql = "SELECT StaffID FROM Staff WHERE FirstName = '{0}' AND Surname = '{1}'".format(FirstName,Surname)
            self.details_cursor.execute(sql)
            StaffID = list(self.details_cursor.fetchone())
            db.commit()
            
        with sqlite3.connect("Volac.db") as db:
            self.details_cursor = db.cursor()
            sql = "SELECT * FROM StaffHardware WHERE StaffID = '{0}'".format(StaffID[0])
            self.details_cursor.execute(sql)
            db.commit()


        col = [tuple[0] for tuple in self.details_cursor.description]
        self.staff_details_table = QTableWidget(2,len(col))
                        
        self.staff_details_table.setHorizontalHeaderLabels(col)
        self.staff_details_table.setRowCount(0)

        for self.row, form in enumerate(self.details_cursor): ##Inserts amount of rows needed, gets from databas
            self.staff_details_table.insertRow(self.row)
            for self.column, item in enumerate(form): ##Inserts amount of columns needed
                self.item = QTableWidgetItem(str(item))
                self.staff_details_table.setItem(self.row, self.column,self.item) ##Each item is added to a the table
                self.staff_details_table.horizontalHeader().setStretchLastSection(True)

        self.vertical.addWidget(self.staff_details_table)
        self.dialog.setLayout(self.vertical)
        self.dialog.exec_()              

                       
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = SearchStaff()
    launcher.show()
    launcher.raise_()
    app.exec_()

