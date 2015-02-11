from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class Manager_Menubar(QMainWindow):
    """Manager Menu Bar"""

    def __init__(self,account_details):
        super().__init__()
        self.MenuBar()

    def MenuBar(self):

        self.menu_bar = QMenuBar()
        
        self.AccountMenu = self.menu_bar.addMenu("Account")
        
        self.Logout = QAction("Log Out",self)
        self.ChangePassword = QAction("Change Password",self)        
        self.AccountMenu.addAction(self.Logout)
        self.AccountMenu.addAction(self.ChangePassword)
        
        self.ViewMenu = self.menu_bar .addMenu("View")
        self.DepartmentDatabase = QAction("Department Database",self)
        self.YourInformation = QAction("Your Information",self)
        self.ViewMenu.addAction(self.DepartmentDatabase)
        self.ViewMenu.addAction(self.YourInformation)

        self.HelpMenu = self.menu_bar .addMenu("Help")
        self.ReportInformation = QAction("Report Incorrect Information",self)
        self.ReportBug = QAction("Report Bug",self)
        self.HelpMenu.addAction(self.ReportInformation)
        self.HelpMenu.addAction(self.ReportBug)

        self.Logout.triggered.connect(self.log_out)
        self.ChangePassword.triggered.connect(self.change_password)

        self.DepartmentDatabase.triggered.connect(self.DepartmentInformationWindow)
        self.YourInformation.triggered.connect(self.MyInformation)

        self.ReportInformation.triggered.connect(self.ReportError)

        

if __name__ == "__main__":

    app = QApplication(sys.argv)
    launcher = Manager_Menubar()
    launcher.show()
    launcher.resize(400,200)
    launcher.raise_()
    app.exec_()
