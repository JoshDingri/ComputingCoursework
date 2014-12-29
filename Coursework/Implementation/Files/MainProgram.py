from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from AdminMainMenu import *
from OpenDatabase import *
from MenuBarAdmin import *
from SearchStaffAdmin import *
import sqlite3


class CurrentLayoutAdmin(QMainWindow):
    """This will set the current layout"""
    
    def __init__(self):
        super().__init__()
        OpenDatabase.Items = []
        self.SearchFirst = False
        self.OpenFirst = False
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
            
            MainMenuWindow.OpenDatabaseBtn.clicked.connect(self.OpenDatabaseWidget)
            MainMenuWindow.SearchStaffBtn.clicked.connect(self.SearchStaff)
        

    def OpenDatabaseWidget(self):
        self.resize(550,350)
        self.OpenDatabaseWindow = OpenDatabase()
        self.OpenDatabaseWidget = QWidget()
        self.OpenDatabaseWidget.setLayout(self.OpenDatabaseWindow.verticle)
        self.stacked_layout.addWidget(self.OpenDatabaseWidget)
        
        if self.SearchFirst:
            self.stacked_layout.setCurrentIndex(2)
        else:
            self.OpenFirst = True
            self.stacked_layout.setCurrentIndex(1)


            
        
        self.OpenDatabaseWindow.Back_btn.clicked.connect(self.MainMenu)
        self.OpenDatabaseWindow.AddDatabase.clicked.connect(self.BrowseDatabase)

    def BrowseDatabase(self):
        try:
            filename = QFileDialog.getOpenFileName(self,'Open File')
            f = open(filename,'r')
            with sqlite3.connect(filename) as db:
                cursor = db.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
                items = cursor.fetchall()
                for count in range(len(items)):
                    items[count] = str(items[count])
                    items[count] = items[count].strip("()'',")
                    self.OpenDatabaseWindow.Database_CB.addItem(items[count])

        except FileNotFoundError:
            pass



    def SearchStaff(self):
        
        self.resize(550,100)
        SearchStaffWindow = SearchStaff()
        
        self.SearchStaffWidget = QWidget()
        self.SearchStaffWidget.setLayout(SearchStaffWindow.verticle)
        self.stacked_layout.addWidget(self.SearchStaffWidget)
        
        if self.OpenFirst:
            self.stacked_layout.setCurrentIndex(2)
        else:
            self.stacked_layout.setCurrentIndex(1)
            self.SearchFirst = True

        
        SearchStaffWindow.Back_btn.clicked.connect(self.MainMenu)
        
        
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = CurrentLayoutAdmin()
    launcher.show()
    launcher.raise_()
    app.exec_()
        
        
