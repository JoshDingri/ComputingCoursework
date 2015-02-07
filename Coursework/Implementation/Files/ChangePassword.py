from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class ChangePassword(QDialog):
    """A Dialog Box Allowing The User To Change Password"""

    def __init__(self,account_details):
        super().__init__()
        self.account_details = account_details
        self.setWindowTitle("Change Password")

        self.grid = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.vertical = QVBoxLayout()

        self.old_pw_lbl = QLabel("Old Password:")
        self.old_pw_le = QLineEdit()
        self.grid.addWidget(self.old_pw_lbl,0,0)
        self.grid.addWidget(self.old_pw_le,0,1)
        
        
        self.new_pw_lbl = QLabel("New Password:")
        self.new_pw_le = QLineEdit()
        self.grid.addWidget(self.new_pw_lbl,1,0)
        self.grid.addWidget(self.new_pw_le,1,1)
        
        self.new_pw_lbl2 = QLabel("Retype New Password:")
        self.new_pw_le2 = QLineEdit()
        self.grid.addWidget(self.new_pw_lbl2,2,0)
        self.grid.addWidget(self.new_pw_le2,2,1)

        self.cancel = QPushButton("Cancel")
        self.change = QPushButton("Change")

        self.horizontal.addWidget(self.cancel)
        self.horizontal.addWidget(self.change)

        self.vertical.addLayout(self.grid)
        self.vertical.addLayout(self.horizontal)

        self.setLayout(self.vertical)

        self.change.clicked.connect(self.active_change)

    def active_change(self):
        old_password = self.old_pw_le.text()
        new_password = self.new_pw_le.text()
        confirm_password = self.new_pw_le2.text()
        self.username = self.account_details[0]

        if old_password == self.account_details[1]:
            if new_password == confirm_password:
                with sqlite3.connect("Accounts.db") as db:
                    cursor = db.cursor()
                    cursor.execute("UPDATE Accounts SET Password='{0}' WHERE Username='{1}' ".format(new_password,self.username))
                    db.commit()
                print("Password Updated")
            else:
                print("passwords do not match")
        else:
            print("Invalid Password")
            
                
                
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = ChangePassword()
    launcher.show()
    launcher.raise_()
    app.exec_()
