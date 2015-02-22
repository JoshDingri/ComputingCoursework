from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class Staff_Menubar(QMenuBar):
    """Staff Menu Bar"""

    def __init__(self):
        super().__init__()
        
        self.AccountMenu = self.addMenu("Account")
        
        self.Logout = QAction("Log Out",self)
        self.ChangePassword = QAction("Change Password",self)        
        self.AccountMenu.addAction(self.Logout)
        self.AccountMenu.addAction(self.ChangePassword)
        self.Logout.setShortcut("CTRL+W")
        self.ChangePassword.setShortcut("CTRL+C")
        
        self.HelpMenu = self.addMenu("Help")
        self.ReportInformation = QAction("Report Incorrect Information",self)
        self.ReportBug = QAction("Report Bug",self)
        self.HelpMenu.addAction(self.ReportInformation)
        self.HelpMenu.addAction(self.ReportBug)
        

if __name__ == "__main__":

    app = QApplication(sys.argv)
    launcher = Manager_Menubar()
    launcher.show()
    launcher.resize(400,200)
    launcher.raise_()
    app.exec_()
