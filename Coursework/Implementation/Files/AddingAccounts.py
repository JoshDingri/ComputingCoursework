from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
import random
import string

class AddUserAccounts(QMainWindow):
    """Program will allow IT Staff to add user accounts"""

    def __init__(self):
        super().__init__()
        self.ProgramLayout()

    def ProgramLayout(self):
        self.grid = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()
        self.horizontal3 = QHBoxLayout()
        self.horizontal4 = QHBoxLayout()
        self.vertical = QVBoxLayout()

        self.FName_Lbl = QLabel("First Name")
        self.FName_LE = QLineEdit()
        
        self.LName_Lbl = QLabel("Last Name")
        self.LName_LE = QLineEdit()

        self.AccessLevel_Lbl = QLabel("Access Level")
        self.AccessLevel_CB = QComboBox()
        self.AccessLevel_CB.addItem("Admin")
        self.AccessLevel_CB.addItem("Manager")
        self.AccessLevel_CB.addItem("Staff")

        self.Department_lbl = QLabel("Department")
        self.Department_LE = QLineEdit()

        self.grid.addWidget(self.FName_Lbl,0,0)
        self.grid.addWidget(self.FName_LE,0,1)

        self.grid.addWidget(self.LName_Lbl,1,0)
        self.grid.addWidget(self.LName_LE,1,1)

        self.grid.addWidget(self.AccessLevel_Lbl,2,0)
        self.grid.addWidget(self.AccessLevel_CB,2,1)

        self.grid.addWidget(self.Department_lbl,3,0)
        self.grid.addWidget(self.Department_LE,3,1)

        self.UsernameResult  = QLineEdit()
        self.RandomPassword = QLineEdit()
        self.AccessLevel = QLineEdit()
        self.DepartmentLE = QLineEdit()

        self.GenerateAccount_btn = QPushButton("Create Account")
        self.GenerateAccount_btn.setFixedWidth(300)

        self.AddAccount = QPushButton("Add Account")

        self.horizontal.addWidget(self.GenerateAccount_btn)

        self.Usernamelbl = QLabel("Username")
        self.Usernamelbl.setAlignment(Qt.AlignCenter)
        self.Passwordlbl = QLabel("Password")
        self.Passwordlbl.setAlignment(Qt.AlignCenter)
        self.AccessLevl = QLabel("Access Level")
        self.AccessLevl.setAlignment(Qt.AlignCenter)
        self.Department = QLabel("Department")
        self.Department.setAlignment(Qt.AlignCenter)

        self.horizontal4.addWidget(self.Usernamelbl)
        self.horizontal4.addWidget(self.Passwordlbl)
        self.horizontal4.addWidget(self.AccessLevl)
        self.horizontal4.addWidget(self.Department)

        self.horizontal2.addWidget(self.UsernameResult)
        self.horizontal2.addWidget(self.RandomPassword)
        self.horizontal2.addWidget(self.AccessLevel)
        self.horizontal2.addWidget(self.DepartmentLE)

        self.horizontal3.addWidget(self.AddAccount)

        self.vertical.addLayout(self.grid)
        self.vertical.addLayout(self.horizontal)
        self.vertical.addStretch(1)
        self.vertical.addLayout(self.horizontal4)
        self.vertical.addLayout(self.horizontal2)
        self.vertical.addLayout(self.horizontal3)

        self.horizontal4.setSpacing(0)


        self.window = QWidget()
        self.window.setLayout(self.vertical)
        self.setCentralWidget(self.window)

        self.GenerateAccount_btn.clicked.connect(self.GenerateAccount)
        self.AddAccount.clicked.connect(self.AddAccountDBConnection)

    def GenerateAccount(self):
        self.FirstName = self.FName_LE.text()
        self.LastName = self.LName_LE.text()
        self.GetDepartment = self.Department_LE.text()
        self.GetAccessLevel = self.AccessLevel_CB.currentText()

        username = (self.FirstName[0]+self.LastName+str(random.randint(1,10)))


        Password_chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        Password_size = 7

        Password = ("".join((random.choice(Password_chars)) for count in range(Password_size)))

        self.UsernameResult.setText(username)
        self.RandomPassword.setText(Password)
        self.AccessLevel.setText(self.GetAccessLevel)
        self.DepartmentLE.setText(self.GetDepartment)

    def AddAccountDBConnection(self):
        values = (self.UsernameResult.text(),self.RandomPassword.text(),self.AccessLevel.text(),self.DepartmentLE.text())
        print(values)
        with sqlite3.connect("Accounts.db") as db:
            cursor = db.cursor()
            sql = "insert into Accounts(Username,Password,Access_Level,Department) values (?,?,?,?)"
            cursor.execute(sql,values)
            db.commit()
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = AddUserAccounts()
    launcher.resize(500,300)
    launcher.show()
    launcher.raise_()
    app.exec_()
        
        

