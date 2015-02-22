from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from MainProgram import *
from ManagerMainProgram import *
from StaffProgram import *
from ForgottenAccount import *
import time


class LoginWindow(QDialog):
    """A Login Window"""

    def __init__(self):
        super().__init__()
        self.SplashScreen()

        self.setWindowTitle("Please Login")
        self.setWindowIcon(QIcon("key.png"))
        self.setFixedSize(425,225)
        self.MainLayout()

    def SplashScreen(self):
        pixmap = QPixmap("splashscreen.png")
        Spashscreen = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        Spashscreen.setMask(pixmap.mask())
        Spashscreen.show()
        time.sleep(2)
        Spashscreen.finish(Spashscreen)

    def MainLayout(self):
        self.horizontal1 = QHBoxLayout()
        self.horizontal2 = QHBoxLayout()
        self.horizontal3 = QHBoxLayout()
        self.horizontal4 = QHBoxLayout()
        self.horizontal5 = QHBoxLayout()
        self.horizontal_lbl = QHBoxLayout()
        self.Vertical_Layout = QVBoxLayout()

        LoginLbl = QLabel("PLEASE LOG IN")
        LoginLbl.setFont(QFont("Calibri",18))

        self.usernameLE = QLineEdit()
        self.usernameLE.setPlaceholderText("Username")
        self.usernameLE.setFixedWidth(250)
        self.usernameLE.setFixedHeight(30)

        self.passwordLE = QLineEdit()
        self.passwordLE.setPlaceholderText("Password")
        self.passwordLE.setEchoMode(QLineEdit.Password)
        self.passwordLE.setFixedWidth(250)
        self.passwordLE.setFixedHeight(30)

        self.TextFormat = QFont("Calibri",11)
        self.TextFormat.setUnderline(True)
        self.ForgotAccount = QLabel("Forgot Username or Password?")
        self.ForgotAccount.setFont(self.TextFormat)
        self.ForgotAccount.mousePressEvent = self.ForgottenAccount

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

        self.horizontal5.addStretch(1)
        self.horizontal5.addWidget(self.ForgotAccount)
        self.horizontal5.addStretch(1)

        self.horizontal_lbl.addStretch(1)
        self.horizontal_lbl.addWidget(self.invalid_lbl)
        self.horizontal_lbl.addStretch(1)

        self.invalid_lbl.setVisible(False)


        self.horizontal4.addStretch(1)
        self.horizontal4.addWidget(LoginBtn)
        self.horizontal4.addStretch(1)

        self.Vertical_Layout.addLayout(self.horizontal1)
        self.Vertical_Layout.addStretch(1)
        self.Vertical_Layout.addLayout(self.horizontal2)
        self.Vertical_Layout.addLayout(self.horizontal3)
        self.Vertical_Layout.addLayout(self.horizontal5)
        self.Vertical_Layout.addStretch(1)
        self.Vertical_Layout.addLayout(self.horizontal_lbl)
        self.Vertical_Layout.addLayout(self.horizontal4)


        self.setLayout(self.Vertical_Layout)


        LoginBtn.clicked.connect(self.CheckLogin)

    def CheckLogin(self):
        self.username = self.usernameLE.text()
        self.password = self.passwordLE.text()

        with sqlite3.connect("Accounts.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Accounts WHERE Username=? ",(self.username,)) #gets account details from username input
            self.account = cursor.fetchone()

    #The try and except statement will catch any invalid usernames entered
    
        if self.account[0] == self.username and self.account[1] == self.password:
            if self.account[2] == 'Admin':
                account_details = self.account
                self.OpenSystem = CurrentLayoutAdmin(account_details)
                self.OpenSystem.show()
                self.hide()
            elif self.account[2] == 'Manager':
                self.departmentsave = self.account[3]
                account_details = self.account
                self.OpenManagerSystem = CurrentLayoutManager(self.departmentsave,account_details)
                self.OpenManagerSystem.show()
                self.hide()
            elif self.account[2] == 'Staff':
                account_details = self.account
                self.StaffProgram_Window = StaffDatabase(account_details)
                self.StaffProgram_Window.show()
                self.hide()
        else:
            self.invalid_lbl.setVisible(True)
            self.passwordLE.setText('')



    def ForgottenAccount(self,event):
        Account_Recovery = ForgottenAccount()
        Account_Recovery.exec_()








def main():
    App = QApplication(sys.argv)
    launcher = LoginWindow()
    launcher.show()
    launcher.raise_()
    App.exec_()

if __name__ == "__main__":
    main()
