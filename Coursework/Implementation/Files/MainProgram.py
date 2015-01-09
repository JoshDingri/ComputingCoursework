from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from AdminMainMenu import *
from OpenDatabaseWindow import *
from MenuBarAdmin import *
from SearchStaffAdmin import *
from AddDataGUI import *
import sqlite3


class CurrentLayoutAdmin(QMainWindow):
    """The purpose of the main program is to import all other python documents
       and run them from the different methods."""
    
    def __init__(self):
        super().__init__()
        OpenDatabase.Items = [] ##For later use, holds dropdown box values
        self.SearchFirst = False ##Temporary method for choosing which qstackindex comes first
        self.OpenFirst = False
        self.MainMenu()
        self.MenuBar() ## Calls menubar definition
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.MainMenuWidget)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.central_widget)
    



    def MenuBar(self):       
        MenuBarAdmin.MenuBar(self) ##Calls menubar from another python file
        
        
    def MainMenu(self):
        self.resize(650,320)
        try:
            self.stacked_layout.setCurrentIndex(0) ##Temporary check to see if qstackindex is being used already
            
        except AttributeError:
            
            MainMenuWindow = AdminMainMenu()
            self.MainMenuWidget = QWidget()

            self.MainMenuWidget.setLayout(MainMenuWindow.horizontal_layout)
            
            MainMenuWindow.OpenDatabaseBtn.clicked.connect(self.OpenDatabaseWidget_Method)
            MainMenuWindow.SearchStaffBtn.clicked.connect(self.SearchStaff)
        

    def OpenDatabaseWidget_Method(self):
        self.resize(770,500)
        self.move (230,100)
        self.OpenDatabaseWindow = OpenDatabase()
        self.OpenDatabaseWidget = QWidget()
        self.OpenDatabaseWidget.setLayout(self.OpenDatabaseWindow.verticle)
        self.stacked_layout.addWidget(self.OpenDatabaseWidget)
        
        if self.SearchFirst:
            self.stacked_layout.setCurrentIndex(2) ##Temporary check to see if qstackindex is being used already
        else:
            self.OpenFirst = True
            self.stacked_layout.setCurrentIndex(1)

            
        
        self.OpenDatabaseWindow.Back_btn.clicked.connect(self.MainMenu)
        self.OpenDatabaseWindow.AddDatabase.clicked.connect(self.BrowseDatabase)
        self.OpenDatabaseWindow.Add_btn.clicked.connect(self.AddDataGUI)
 #       self.OpenDatabaseWindow.Remove_btn.clicked.connect(self.RemoveData_btnClick)


    def RemoveData_btnClick(self):
        if self.OpenDatabaseWindow.DeleteRC == True:
            self.resize(765,420)
        else:
            self.resize(635,420)

            

    def BrowseDatabase(self): ###### This opens the file finder to choose the database
        try:
            filename = QFileDialog.getOpenFileName(self,'Open File')
            f = open(filename,'r')
            with sqlite3.connect(filename) as db:
                cursor = db.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
                items = cursor.fetchall() ### Gets all the table names
                for count in range(len(items)):
                    items[count] = str(items[count])
                    items[count] = items[count].strip("()'',")
                    self.OpenDatabaseWindow.Database_CB.addItem(items[count]) ## Adds all the tables to the dropdown box

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
            self.SearchFirst = True ##Temporary check to see if qstackindex is being used already

        
        SearchStaffWindow.Back_btn.clicked.connect(self.MainMenu)
        
    def AddDataGUI(self):
        CurrentCBValue = self.OpenDatabaseWindow.Database_CB.currentText()
        AddDataGUI = AddDataWindow(CurrentCBValue)
        AddDataGUI.exec_() ## executes dialog box
        
        

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = CurrentLayoutAdmin()
    launcher.show()
    launcher.raise_()
    app.exec_()
        
        
