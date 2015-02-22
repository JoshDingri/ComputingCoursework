from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
import random
import string

class AddUserAccounts(QDialog):
    """This class will allow IT Staff to add user accounts"""

    def __init__(self):
        super().__init__()
        self.ProgramLayout()

    def ProgramLayout(self):
        self.UserInput_GridLayout = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()
        self.horizontal3 = QHBoxLayout()
        self.horizontal4 = QHBoxLayout()
        self.Overall_Layout_Vertical = QVBoxLayout()

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT FirstName FROM Staff"
            cursor.execute(sql)
            db.commit()
        FirstnameList = [item[0] for item in cursor.fetchall()] #List will fetch all items from database

        self.FName_Lbl = QLabel("First Name")
        self.FName_CB = QComboBox()         
        self.FName_CB.addItems(FirstnameList)
        
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT Surname FROM Staff"
            cursor.execute(sql)
            db.commit()
        LastNameList = [item[0] for item in cursor.fetchall()]
        
        self.LName_Lbl = QLabel("Last Name")
        self.LName_CB = QComboBox()
        self.LName_CB.addItems(LastNameList)

        self.AccessLevel_Lbl = QLabel("Access Level")
        self.AccessLevel_CB = QComboBox()
        self.AccessLevel_CB.addItem("Admin")
        self.AccessLevel_CB.addItem("Manager")
        self.AccessLevel_CB.addItem("Staff")

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT DepartmentName FROM Department"
            cursor.execute(sql)
            db.commit()
        DepartmentList = [item[0] for item in cursor.fetchall()]

        self.Department_lbl = QLabel("Department")
        self.Department_CB = QComboBox()
        self.Department_CB.addItems(DepartmentList)
        

        self.UserInput_GridLayout.addWidget(self.FName_Lbl,0,0)
        self.UserInput_GridLayout.addWidget(self.FName_CB,0,1)

        self.UserInput_GridLayout.addWidget(self.LName_Lbl,1,0)
        self.UserInput_GridLayout.addWidget(self.LName_CB,1,1)

        self.UserInput_GridLayout.addWidget(self.AccessLevel_Lbl,2,0)
        self.UserInput_GridLayout.addWidget(self.AccessLevel_CB,2,1)

        self.UserInput_GridLayout.addWidget(self.Department_lbl,3,0)
        self.UserInput_GridLayout.addWidget(self.Department_CB,3,1)


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

        self.Overall_Layout_Vertical.addLayout(self.UserInput_GridLayout)
        self.Overall_Layout_Vertical.addLayout(self.horizontal)
        self.Overall_Layout_Vertical.addStretch(1)
        self.Overall_Layout_Vertical.addLayout(self.horizontal4)
        self.Overall_Layout_Vertical.addLayout(self.horizontal2)
        self.Overall_Layout_Vertical.addLayout(self.horizontal3)


        self.setLayout(self.Overall_Layout_Vertical)



        self.GenerateAccount_btn.clicked.connect(self.GenerateAccount)
        self.AddAccount.clicked.connect(self.AddAccountDBConnection)

    def GenerateAccount(self):
        self.FirstName = self.FName_CB.currentText()
        self.LastName = self.LName_CB.currentText()
        self.GetDepartment = self.Department_CB.currentText()
        self.GetAccessLevel = self.AccessLevel_CB.currentText()

        username = (self.FirstName[0]+self.LastName+str(random.randint(1,100))) #Username will take the first letter of the firstname and the surname. Then add a random integer


        Password_chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        Password_size = 7

        Password = ("".join((random.choice(Password_chars)) for count in range(Password_size))) #A random password will be generated with 7 characters using upper/lowercase and integers. 

        ##The admin can change the username/password if they would like by editing the line edits. Or they can simply generate new ones.

        self.UsernameResult.setText(username)
        self.RandomPassword.setText(Password)
        self.AccessLevel.setText(self.GetAccessLevel)
        self.DepartmentLE.setText(self.GetDepartment)

    def AddAccountDBConnection(self):
        values = (self.UsernameResult.text(),self.RandomPassword.text(),self.AccessLevel.text(),self.DepartmentLE.text(),self.FirstName,self.LastName)
        print(values)
        with sqlite3.connect("Accounts.db") as db:
            cursor = db.cursor()
            sql = "insert into Accounts(Username,Password,Access_Level,Department,FirstName,LastName) values (?,?,?,?,?,?)"
            cursor.execute(sql,values)
            db.commit()
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = AddUserAccounts()
    launcher.resize(500,300)
    launcher.show()
    launcher.raise_()
    app.exec_()
        
        

