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

        self.GridLayout = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.horizontallbl = QHBoxLayout()
        self.vertical = QVBoxLayout()

        self.changed_lbl = QLabel()
        self.changed_lbl.setVisible(False)

        self.horizontallbl.addStretch(1)
        self.horizontallbl.addWidget(self.changed_lbl)
        self.horizontallbl.addStretch(1)

        self.old_pw_lbl = QLabel("Old Password:")
        self.old_pw_le = QLineEdit()
        self.old_pw_le.setEchoMode(QLineEdit.Password)
        self.GridLayout.addWidget(self.old_pw_lbl,0,0)
        self.GridLayout.addWidget(self.old_pw_le,0,1)
        
        
        self.new_pw_lbl = QLabel("New Password:")
        self.new_pw_le = QLineEdit()
        self.new_pw_le.setEchoMode(QLineEdit.Password)
        self.GridLayout.addWidget(self.new_pw_lbl,1,0)
        self.GridLayout.addWidget(self.new_pw_le,1,1)
        
        self.new_pw_lbl2 = QLabel("Retype New Password:")
        self.new_pw_le2 = QLineEdit()
        self.new_pw_le2.setEchoMode(QLineEdit.Password)
        self.GridLayout.addWidget(self.new_pw_lbl2,2,0)
        self.GridLayout.addWidget(self.new_pw_le2,2,1)

        self.cancel = QPushButton("Cancel")
        self.change = QPushButton("Change")

        self.horizontal.addWidget(self.cancel)
        self.horizontal.addWidget(self.change)

        self.vertical.addLayout(self.GridLayout)
        self.vertical.addLayout(self.horizontal)
        self.vertical.addLayout(self.horizontallbl)

        self.setLayout(self.vertical)

        self.change.clicked.connect(self.active_change)
        self.cancel.clicked.connect(self.CloseWindow)

    def CloseWindow(self):
        self.reject()

    def active_change(self):
        old_password = self.old_pw_le.text()
        new_password = self.new_pw_le.text()
        confirm_password = self.new_pw_le2.text()
        self.username = self.account_details[0]

        if old_password == self.account_details[1]:
            if new_password == confirm_password:
                with sqlite3.connect("Accounts.db") as db:
                    cursor = db.cursor()
                    cursor.execute("UPDATE Accounts SET Password=? WHERE Username=? ",(new_password,self.username,))
                    cursor.execute("PRAGMA foreign_keys = ON")
                    db.commit()
                self.changed_lbl.setText("Password Has Been Changed")
                self.changed_lbl.setVisible(True)
            else:
                self.changed_lbl.setText("Passwords Do Not Match")
                self.changed_lbl.setVisible(True)
        else:
            self.changed_lbl.setText("Incorrect Password")
            self.changed_lbl.setVisible(True)
            
                
                
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = ChangePassword()
    launcher.show()
    launcher.raise_()
    app.exec_()
