from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from AdminMainMenu import *
from OpenDatabase import *
from MenuBarAdmin import *
from SearchStaffAdmin import *


class CurrentLayoutAdmin(QMainWindow):
    """This will set the current layout"""
    
    def __init__(self):
        super().__init__()
        self.MenuBar()
        self.MainMenu()


    def MenuBar(self):       
        MenuBarAdmin.MenuBar(self)
        
        
    def MainMenu(self):
        self.resize(550,270)
        MainMenuWindow = AdminMainMenu()
        self.btnWidget = QWidget()

        self.btnWidget.setLayout(MainMenuWindow.horizontal_layout)

        self.setCentralWidget(self.btnWidget)
        
        MainMenuWindow.OpenDatabaseBtn.clicked.connect(self.OpenDatabase)
        MainMenuWindow.SearchStaffBtn.clicked.connect(self.SearchStaff)


    def OpenDatabase(self):
        self.resize(550,350)
        OpenDatabaseWindow = OpenDatabase()
        self.LayoutWidget = QWidget()

        self.LayoutWidget.setLayout(OpenDatabaseWindow.verticle)

        self.setCentralWidget(self.LayoutWidget)
        
        OpenDatabaseWindow.Back_btn.clicked.connect(self.MainMenu)


    def SearchStaff(self):
        self.resize(550,100)
        SearchStaffWindow = SearchStaff()
        
        self.layoutWidget = QWidget()
        self.layoutWidget.setLayout(SearchStaffWindow.verticle)
        self.setCentralWidget(self.layoutWidget)
        SearchStaffWindow.Back_btn.clicked.connect(self.MainMenu)
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = CurrentLayoutAdmin()
    launcher.show()
    launcher.raise_()
    app.exec_()
        
        
