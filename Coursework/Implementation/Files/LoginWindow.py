from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from MainProgram import *
from ManagerMainProgram import *


class LoginWindow(QMainWindow):
    """A Login Window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Please Login")
        self.setWindowIcon(QIcon("key.png"))
        self.MainLayout()
        

    def MainLayout(self):
        self.horizontal1 = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()
        self.horizontal3 = QHBoxLayout()
        self.horizontal4 = QHBoxLayout()
        self.horizontal_lbl = QHBoxLayout()
        self.verticle = QVBoxLayout()

        LoginLbl = QLabel("PLEASE LOG IN")
        LoginLbl.setFont(QFont("Georgia",18))

        self.usernameLE = QLineEdit()
        self.usernameLE.setPlaceholderText("Username")
        self.usernameLE.setFixedWidth(250)
        self.usernameLE.setFixedHeight(30)
        
        self.passwordLE = QLineEdit()
        self.passwordLE.setPlaceholderText("Password")
        self.passwordLE.setEchoMode(QLineEdit.Password)
        self.passwordLE.setFixedWidth(250)
        self.passwordLE.setFixedHeight(30)
        
        LoginBtn = QPushButton("Log In")
        LoginBtn.setStyleSheet("""QPushButton{
                                color: #333;
                                border: 2px solid #555;
                                border-radius: 11px;
                                padding: 5px;
                                background: qradialgradient(cx: 0.3, cy: -0.4,
                                fx: 0.3, fy: -0.4,
                                radius: 1.35, stop: 0 #fff, stop: 1 #888);
                                min-width: 80px;
                                }"""
                                         
                                """QPushButton:hover{
                                background: qradialgradient(cx: 0.3, cy: -0.4,
                                fx: 0.3, fy: -0.4,
                                radius: 1.35, stop: 0 #fff, stop: 1 #bbb);
                                }"""

                                """QPushButton:pressed {
                                background: qradialgradient(cx: 0.4, cy: -0.1,
                                fx: 0.4, fy: -0.1,
                                radius: 1.35, stop: 0 #fff, stop: 1 #ddd);
                                }""")
        LoginBtn.setFixedWidth(100)
        LoginBtn.setFixedHeight(30)

        self.invalid_lbl = QLabel("Your Username Or Password Is Incorrect")

        self.horizontal1.addStretch(1)
        self.horizontal1.addWidget(LoginLbl)
        self.horizontal1.addStretch(1)

        self.horizontal2.addStretch(1)
        self.horizontal2.addWidget(self.usernameLE)
        self.horizontal2.addStretch(1)
        
        self.horizontal3.addStretch(1)
        self.horizontal3.addWidget(self.passwordLE)
        self.horizontal3.addStretch(1)
        
        self.horizontal_lbl.addStretch(1)
        self.horizontal_lbl.addWidget(self.invalid_lbl)
        self.horizontal_lbl.addStretch(1)

        self.invalid_lbl.setVisible(False)

        
        self.horizontal4.addStretch(1)
        self.horizontal4.addWidget(LoginBtn)
        self.horizontal4.addStretch(1)

        self.verticle.addLayout(self.horizontal1)
        self.verticle.addStretch(1)
        self.verticle.addLayout(self.horizontal2)
        self.verticle.addLayout(self.horizontal3)
        self.verticle.addStretch(1)
        self.verticle.addLayout(self.horizontal_lbl)
        self.verticle.addLayout(self.horizontal4)

        window_widget = QWidget()
        window_widget.setLayout(self.verticle)
        self.setCentralWidget(window_widget)


        LoginBtn.clicked.connect(self.CheckLogin)

    def CheckLogin(self):
        self.username = self.usernameLE.text()
        self.password = self.passwordLE.text()

        with sqlite3.connect("Accounts.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Accounts WHERE Username=? ",(self.username,))
            account = cursor.fetchone()
        try:
            if account[0] == self.username and account[1] == self.password:
                if account[2] == 'Admin':
                    self.OpenSystem = CurrentLayoutAdmin()
                    self.OpenSystem.show()
                    self.hide()
                elif account[2] == 'Manager':
                    self.OpenManagerSystem = CurrentLayoutManager()
                    self.OpenManagerSystem.show()
                    self.hide()
                else:
                    pass
            else:
                self.invalid_lbl.setVisible(True)
                self.passwordLE.setText('')               
        except TypeError:
            self.invalid_lbl.setVisible(True)
            self.passwordLE.setText('')

        
            

        
        
        

def main():
    App = QApplication(sys.argv)
    launcher = LoginWindow()
    launcher.show()
    launcher.raise_()
    launcher.setFixedSize(425,225)
    App.exec_()

if __name__ == "__main__":
    main()
