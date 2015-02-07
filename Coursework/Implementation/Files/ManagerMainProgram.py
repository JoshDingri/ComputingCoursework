from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from DepartmentInformation import *
from ManagerMainMenu import *
from ManagerMenuBar import *

class CurrentLayoutManager(QMainWindow):
    """The main program in charge of switching layouts"""

    def __init__(self,department):
        super().__init__()
        self.department = department
        self.menubar()
        self.mainmenu()
        

    def menubar(self):
        ManagerMenu = Manager_Menubar()
        self.setMenuBar(ManagerMenu)

    def mainmenu(self):
        self.resize(800,400)
        MainMenu = Manager_Main_Menu()
        self.setCentralWidget(MainMenu)

        MainMenu.DeparmentInfoBtn.clicked.connect(self.DepartmentInformationWindow)
        #Manager_Main_Menu.MyInfoBtn.clicked.connect(self.SearchStaff)

    def DepartmentInformationWindow(self):
        self.resize(800,400)
        self.databasewindow = DepartmentInformation(self.department)
        self.setCentralWidget(self.databasewindow)
        
        self.databasewindow.Back_btn.clicked.connect(self.mainmenu)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = CurrentLayoutManager()
    launcher.show()
    launcher.raise_()
    app.exec_()
