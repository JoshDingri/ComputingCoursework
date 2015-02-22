from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from DepartmentInformation import *
from ManagerMainMenu import *
from ManagerMenuBar import *
from MyInformation import *
from ChangePassword import *
from Reporterror import *
from BugReport import *

class CurrentLayoutManager(QMainWindow):
    """The main program in charge of switching layouts"""

    def __init__(self,department,account_details):
        super().__init__()
        self.department = department
        self.account_details = account_details
        self.stacked_layout = QStackedWidget()
        self.setCentralWidget(self.stacked_layout)

        self.mainmenu()
        self.MyInformation()
        self.DepartmentInformationWindow()
        self.menubar()
        self.ButtonTriggers()

    def ButtonTriggers(self):
        self.ManagerMenuBar.Logout.triggered.connect(self.log_out)
        self.ManagerMenuBar.ChangePassword.triggered.connect(self.change_password)
        self.ManagerMenuBar.DepartmentDatabase.triggered.connect(self.SwitchToDepartmentInformationWindow)
        self.ManagerMenuBar.YourInformation.triggered.connect(self.SwitchToMyInformation)
        self.ManagerMenuBar.ReportInformation.triggered.connect(self.ReportError)
        self.ManagerMenuBar.ReportBug.triggered.connect(self.BugReport)

        self.InstantiateMainMenu.DeparmentInfoBtn.clicked.connect(self.SwitchToDepartmentInformationWindow)
        self.InstantiateMainMenu.MyInfoBtn.clicked.connect(self.SwitchToMyInformation)

        self.InstantiateDatabaseWindow.Back_btn.clicked.connect(self.BackToMenu)
        
        self.InstantiateMy_Info.Back_btn.clicked.connect(self.BackToMenu)
        

    def menubar(self):
        self.ManagerMenuBar = Manager_Menubar()
        self.setMenuBar(self.ManagerMenuBar)

    def log_out(self):
        self.close()

    def change_password(self):
        self.ChangePassword_window = ChangePassword(self.account_details)
        self.ChangePassword_window.exec_()


    def mainmenu(self):
        self.resize(800,400)
        self.InstantiateMainMenu = Manager_Main_Menu()
        self.stacked_layout.addWidget(self.InstantiateMainMenu)
        

    def DepartmentInformationWindow(self):
        self.resize(800,400)
        self.InstantiateDatabaseWindow = DepartmentInformation(self.department)
        self.stacked_layout.addWidget(self.InstantiateDatabaseWindow)        

    def MyInformation(self):
        self.InstantiateMy_Info = MyInformation(self.account_details)
        self.stacked_layout.addWidget(self.InstantiateMy_Info)

    def SwitchToDepartmentInformationWindow(self):
        self.stacked_layout.setCurrentIndex(2)

    def SwitchToMyInformation(self):
        self.stacked_layout.setCurrentIndex(1)

    def BackToMenu(self):
        self.stacked_layout.setCurrentIndex(0)


    def ReportError(self):
        Report_Error = ReportError()
        Report_Error.exec_()

    def BugReport(self):
        Report_Bug = ReportBug()
        Report_Bug.exec_()

    

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = CurrentLayoutManager()
    launcher.show()
    launcher.raise_()
    app.exec_()
