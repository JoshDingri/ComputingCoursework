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
        self.MainMenu()
        self.MenuBar()
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.MainMenuWidget)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
    



    def MenuBar(self):       
        MenuBarAdmin.MenuBar(self)
        
        
    def MainMenu(self):
        try:
            self.stacked_layout.setCurrentIndex(0)
            
        except AttributeError:
            
            self.resize(550,270)
            MainMenuWindow = AdminMainMenu()
            self.MainMenuWidget = QWidget()

            self.MainMenuWidget.setLayout(MainMenuWindow.horizontal_layout)
            
            MainMenuWindow.OpenDatabaseBtn.clicked.connect(self.OpenDatabase)
            MainMenuWindow.SearchStaffBtn.clicked.connect(self.SearchStaff)
        

    def OpenDatabase(self):
        self.resize(550,350)
        OpenDatabaseWindow = OpenDatabase()
        
        self.OpenDatabaseWidget = QWidget()
        self.OpenDatabaseWidget.setLayout(OpenDatabaseWindow.verticle)
        self.stacked_layout.addWidget(self.OpenDatabaseWidget)
        self.stacked_layout.setCurrentIndex(1)
        
        OpenDatabaseWindow.Back_btn.clicked.connect(self.MainMenu)
        OpenDatabaseWindow.AddDatabase.clicked.connect(self.BrowseDatabase)

    def BrowseDatabase(self):
        try:
            filename = QFileDialog.getOpenFileName(self,'Open File')
            f = open(filename,'r')
        
        except FileNotFoundError:
            pass



    def SearchStaff(self):
        self.resize(550,100)
        SearchStaffWindow = SearchStaff()
        
        self.SearchStaffWidget = QWidget()
        self.SearchStaffWidget.setLayout(SearchStaffWindow.verticle)
        self.stacked_layout.addWidget(self.SearchStaffWidget)
        self.stacked_layout.setCurrentIndex(2)
        
        SearchStaffWindow.Back_btn.clicked.connect(self.MainMenu)
        
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = CurrentLayoutAdmin()
    launcher.show()
    launcher.raise_()
    app.exec_()
        
        
