from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MenuBarAdmin import *
from graph import *
from AddingAccounts import *


class AdminMainMenu(QWidget):
    """The Admin's main menu screen"""

    def __init__(self):
        super().__init__()

        self.Vertical_Layout = QVBoxLayout()
        
        
        self.ButtonStyleSheet =  ("""QPushButton{
                                min-height: 1.7em;
                                font: 1em;
                                margin: 0 1px 0 1px;
                                color: black;
                                background-color: #F5F5F5;
                                border-style: outset;
                                border-radius: 20px;
                                border-width: 3px;
                                border-color: green;}
                             
                            QPushButton:pressed {
                                background-color: #F2E4E4
                            }""")

        self.OpenDatabaseBtn = QPushButton("Open Database")
        self.OpenDatabaseBtn.setFont(QFont("Calibri",20))
        self.SearchStaffBtn = QPushButton("Search Staff")
        self.SearchStaffBtn.setFont(QFont("Calibri",20))
        
        self.OpenDatabaseBtn.setFixedHeight(100)
        self.SearchStaffBtn.setFixedHeight(100)
        self.SearchStaffBtn.setStyleSheet(self.ButtonStyleSheet)
        self.OpenDatabaseBtn.setStyleSheet(self.ButtonStyleSheet)

        self.Vertical_Layout.addWidget(self.OpenDatabaseBtn)
        self.Vertical_Layout.addWidget(self.SearchStaffBtn)

        self.setLayout(self.Vertical_Layout)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = AdminMainMenu()
    launcher.show()
    launcher.raise_()
    app.exec_()
