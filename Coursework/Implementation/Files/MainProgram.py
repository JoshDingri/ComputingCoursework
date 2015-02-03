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
##        self.stacked_layout = QStackedLayout()
##        self.stacked_layout.addWidget(self.MainMenuWidget)
##        self.central_widget = QWidget()
##        self.central_widget.setLayout(self.stacked_layout)
##        self.setCentralWidget(self.central_widget)
    



    def MenuBar(self):       
        MenuBarAdmin.MenuBar(self) ##Calls menubar from another python file
        
        
    def MainMenu(self):
        self.resize(650,320)
        MainMenuWindow = AdminMainMenu()
        self.setCentralWidget(MainMenuWindow)

            
        MainMenuWindow.OpenDatabaseBtn.clicked.connect(self.OpenDatabaseWidget_Method)
        MainMenuWindow.SearchStaffBtn.clicked.connect(self.SearchStaff)
        

    def OpenDatabaseWidget_Method(self):
        self.OpenDatabaseWindow = OpenDatabase()
        self.setCentralWidget(self.OpenDatabaseWindow)
        self.resize(738,500)
        self.move (500,180)
            
        
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
        self.resize(700,500)
        SearchStaffWindow = SearchStaff()
        self.setCentralWidget(SearchStaffWindow)

        
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
        
        
