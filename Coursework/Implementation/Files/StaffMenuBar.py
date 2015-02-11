from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class Staff_Menubar(QMainWindow):
    """Staff Menu Bar"""

    def __init__(self):
        super().__init__()
        self.MenuBar()

    def MenuBar(self):

        self.menu_bar = QMenuBar()
        
        self.AccountMenu = self.menu_bar.addMenu("Account")
        
        self.Logout = QAction("Log Out",self)
        self.ChangePassword = QAction("Change Password",self)        
        self.AccountMenu.addAction(self.Logout)
        self.AccountMenu.addAction(self.ChangePassword)
        
        self.HelpMenu = self.menu_bar .addMenu("Help")
        self.ReportInformation = QAction("Report Incorrect Information",self)
        self.ReportBug = QAction("Report Bug",self)
        self.HelpMenu.addAction(self.ReportInformation)
        self.HelpMenu.addAction(self.ReportBug)

        self.setMenuBar(self.menu_bar)

        self.Logout.triggered.connect(self.log_out)
        self.ChangePassword.triggered.connect(self.change_password)

        self.ReportInformation.triggered.connect(self.ReportError)
        self.ReportBug.triggered.connect(self.BugReport)
        

if __name__ == "__main__":

    app = QApplication(sys.argv)
    launcher = Manager_Menubar()
    launcher.show()
    launcher.resize(400,200)
    launcher.raise_()
    app.exec_()
