from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys


class Manager_Main_Menu(QMainWindow):
    """Main Menu for use by managers"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manager Main Menu")
        self.MenuBar()
        self.Buttons()

    def MenuBar(self):
        self.menu_bar = QMenuBar()
        
        self.AccountMenu = self.menu_bar.addMenu("Account")
        
        self.Logout = QAction("Log Out",self)
        self.ChangePassword = QAction("Change Password",self)        
        self.AccountMenu.addAction(self.Logout)
        self.AccountMenu.addAction(self.ChangePassword)
     
        self.ViewMenu = self.menu_bar.addMenu("View")

        self.DepartmentDatabase = QAction("Department Database",self)
        self.YourInformation = QAction("Your Information",self)
        self.ViewMenu.addAction(self.DepartmentDatabase)
        self.ViewMenu.addAction(self.YourInformation)

        self.HelpMenu = self.menu_bar.addMenu("Help")
        
        self.ReportInformation = QAction("Report Incorrect Information",self)
        self.ReportBug = QAction("Report Bug",self)
        self.HelpMenu.addAction(self.ReportInformation)
        self.HelpMenu.addAction(self.ReportBug)

        
        self.setMenuBar(self.menu_bar)
    
    def Buttons(self):
        self.horizontal_layout = QHBoxLayout()

        self.DeparmentInfoBtn = QPushButton("Department Information")
        self.MyInfoBtn = QPushButton("My Information")

        self.horizontal_layout.addWidget(self.DeparmentInfoBtn)
        self.horizontal_layout.addWidget(self.MyInfoBtn)

        self.btnWidget = QWidget()

        self.btnWidget.setLayout(self.horizontal_layout)

        self.setCentralWidget(self.btnWidget)

        



def main():
    app = QApplication(sys.argv)
    launcher = Manager_Main_Menu()
    launcher.show()
    launcher.resize(400,200)
    launcher.raise_()
    app.exec_()
    
if __name__ == "__main__":
    main()
