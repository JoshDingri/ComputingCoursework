from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from DepartmentInformation import *
from ManagerMainMenu import *
from ManagerMenuBar import *

class CurrentLayoutManager(QMainWindow):
    """The main program in charge of switching layouts"""

    def __init__(self):
        super().__init__()
        self.menubar()
        self.mainmenu()

    def menubar(self):
        ManagerMenu = Manager_Menubar()
        self.setMenuBar(ManagerMenu)

    def mainmenu(self):
        MainMenu = Manager_Main_Menu()
        self.setCentralWidget(MainMenu)

        MainMenu.DeparmentInfoBtn.clicked.connect(self.DepartmentInformationWindow)
        #Manager_Main_Menu.MyInfoBtn.clicked.connect(self.SearchStaff)

    def DepartmentInformationWindow(self):
        self.databasewindow = DepartmentInformation()
        self.setCentralWidget(self.databasewindow)
        
        self.databasewindow.Back_btn.clicked.connect(self.mainmenu)
        self.databasewindow.AddDatabase.clicked.connect(self.BrowseDatabase)

    def BrowseDatabase(self): ###### This opens the file finder to choose the database
        try:
            filename = QFileDialog.getOpenFileName(self,'Open File')
            f = open(filename,'r')
            with sqlite3.connect(filename) as db:
                cursor = db.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
                self.databasewindow.Database_CB.addItem("Staff") ## Adds all the tables to the dropdown box        
        except FileNotFoundError:
            pass
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = CurrentLayoutManager()
    launcher.show()
    launcher.raise_()
    app.exec_()
