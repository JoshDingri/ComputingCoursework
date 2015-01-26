from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys


class LoginWindow(QWidget):
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
        self.verticle = QVBoxLayout()

        LoginLbl = QLabel("PLEASE LOG IN")
        LoginLbl.setFont(QFont("Georgia",18))

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedWidth(250)
        self.username.setFixedHeight(30)
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedWidth(250)
        self.password.setFixedHeight(30)
        
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

        self.horizontal1.addStretch(1)
        self.horizontal1.addWidget(LoginLbl)
        self.horizontal1.addStretch(1)

        self.horizontal2.addStretch(1)
        self.horizontal2.addWidget(self.username)
        self.horizontal2.addStretch(1)
        
        self.horizontal3.addStretch(1)
        self.horizontal3.addWidget(self.password)
        self.horizontal3.addStretch(1)
        
        self.horizontal4.addStretch(1)
        self.horizontal4.addWidget(LoginBtn)
        self.horizontal4.addStretch(1)

        self.verticle.addLayout(self.horizontal1)
        self.verticle.addStretch(1)
        self.verticle.addLayout(self.horizontal2)
        self.verticle.addLayout(self.horizontal3)
        self.verticle.addStretch(1)
        self.verticle.addLayout(self.horizontal4)

        self.setLayout(self.verticle)

        LoginBtn.clicked.connect(self.CheckLogin)

    def CheckLogin(self):
        self.username = self.username.text()
        print(self.username)
        self.password = self.password.text()
        print(self.password)
        
        

def main():
    App = QApplication(sys.argv)
    launcher = LoginWindow()
    launcher.show()
    launcher.raise_()
    launcher.setFixedSize(425,225)
    App.exec_()

if __name__ == "__main__":
    main()
