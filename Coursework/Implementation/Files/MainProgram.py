from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from AdminMainMenu import *
from OpenDatabaseWindow import *
from MenuBarAdmin import *
from SearchStaffAdmin import *
from AddDataGUI import *
from LoginWindow import *
from ChangePassword import *
from PopupDialog import *
import sqlite3
import time
import datetime


class CurrentLayoutAdmin(QMainWindow):
    """The purpose of the main program is to import all other python documents
       and run them from the different methods."""
    
    def __init__(self,account_details):
        super().__init__()
        OpenDatabase.Items = [] ##For later use, holds dropdown box values
        self.SearchFirst = False ##Temporary method for choosing which qstackindex comes first
        self.OpenFirst = False

        self.setWindowIcon(QIcon("WindowIcon.png")    )    
        self.stacked_layout = QStackedWidget() #Holds widgets on a stack
        self.setCentralWidget(self.stacked_layout)
        self.setWindowTitle("Volac Database")

        
        self.account_details = account_details 
        self.MainMenu()
        self.OpenDatabaseWidget_Method()
        self.SearchStaff()
        
        self.ToolBar()
        self.CheckExpirationDates()
        self.MenuBar() 
        self.ButtonTriggers()

        self.setStyleSheet("""QMainWindow {
                                   background-color: #ffffff;
                                   color: #cccccc;
                                }
                    QMenuBar{
                                font-family: Calibri;
                                font-size: 12pt;
                                font: bold;
                                background-color: white;}

                    QMenuBar:item{
                                font-size: 12pt;
                                font-family: Calibri;
                                background-color: white;
                                color: green;}
                                
                    QMenuBar:item:pressed{
                                background-color: #96FF70;
                                color: green;}

                    QMenuBar:item:active{
                                background-color: #96FF70;
                                color: green;}
                    QPushButton#OpenGraph,QPushButton#CreateAccounts{
                                padding: 4px;
                                border: none;
                                font: 13px;
                                color: green;
                                background-color: white;
                                }
                             
                    QPushButton#OpenGraph:hover,QPushButton#CreateAccounts:hover {                                
                                font: 1em;
                                color: green;
                                background-color: #F5F5F5;
                            }
                            
                    QPushButton#OpenGraph:pressed,QPushButton#CreateAccounts:pressed {                                
                                font: 1em;
                                border: solid;
                                border-style: outset;
                                color: green;
                                background-color: #BFBFBF;
                            }""")
            



        
    def ButtonTriggers(self):
        self.OpenGraphBtn.clicked.connect(Graph)
        self.CreateAccounts.clicked.connect(self.Create_Account)
        self.menubar.Logout.triggered.connect(self.Log_Out)
        self.menubar.ChangePassword.triggered.connect(self.Change_Password)
        self.MainMenuWindow.OpenDatabaseBtn.clicked.connect(self.SwitchToOpenDatabase)
        self.MainMenuWindow.SearchStaffBtn.clicked.connect(self.SwitchToSearch)
        self.OpenDatabaseWindow.Back_btn.clicked.connect(self.BackToMenu)
        self.OpenDatabaseWindow.AddDatabase.clicked.connect(self.BrowseDatabase)
        self.OpenDatabaseWindow.Add_btn.clicked.connect(self.AddDataGUI)
        self.SearchStaffWindow.Back_btn.clicked.connect(self.BackToMenu)

    def ToolBar(self):
        self.OpenGraphBtn = QPushButton("Generate Hardware Graph")
        self.OpenGraphBtn.setObjectName("OpenGraph")
        self.OpenGraphBtn.setIcon(QIcon("chart_bar.png"))
        self.CreateAccounts = QPushButton("Create User Accounts")
        self.CreateAccounts.setObjectName("CreateAccounts")
        self.CreateAccounts.setIcon(QIcon("accounticon.png"))
        self.toolbar = self.addToolBar("Open")
        self.toolbar.addWidget(self.OpenGraphBtn)
        self.toolbar.addWidget(self.CreateAccounts)
        
    def Create_Account(self):
        CreateAccount = AddUserAccounts()
        CreateAccount.resize(600,300)
        CreateAccount.exec_()
    

    def CheckExpirationDates(self):
        """Function that will check if a device has 90 days before warranty expires"""
        self.currentdate = time.strftime("%d-%m-%y")
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = ("SELECT WarrantyExpirationDate FROM Hardware")
            cursor.execute(sql)
            db.commit()
        WarrantyExpirationDate = [item[0] for item in cursor.fetchall()]


        b = "(', )" 
            
        for count in range (len(WarrantyExpirationDate)):
            if WarrantyExpirationDate[count] == '-':
                continue
            for i in range(0,len(b)):
                WarrantyExpirationDate[count] = str(WarrantyExpirationDate[count]).replace(b[i],"")
                self.expiringitem = WarrantyExpirationDate[count]

            currentdate = datetime.datetime.strptime(self.currentdate,"%d-%m-%y")
            self.WarrantyExpirationDate = datetime.datetime.strptime(WarrantyExpirationDate[count],"%d-%m-%y")
            

            
            daysleft = self.WarrantyExpirationDate - currentdate
            if daysleft.days == 90:
                self.SendExpirationEmail()


    def SendExpirationEmail(self):
        """Sends hardware expiring email"""
        self.WarrantyExpirationDate = self.WarrantyExpirationDate.strftime("%d-%m-%y")
        self.WarrantyExpirationDate =  (self.WarrantyExpirationDate)
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareID FROM Hardware WHERE WarrantyExpirationDate=?",(self.WarrantyExpirationDate,))
            HardwareIDs = list(cursor.fetchone())
            db.commit()

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareModelID FROM Hardware WHERE HardwareID=?",(HardwareIDs[0],))
            ModelID = list(cursor.fetchone())
            db.commit()

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareModelName FROM HardwareModel WHERE HardwareModelID=?",(ModelID[0],))
            HardwareModel = list(cursor.fetchone())
            db.commit()

        
        self.mail = smtplib.SMTP("smtp.live.com",25)
        self.mail.ehlo()
        self.mail.starttls()

        IT_Staff_Email = ('josh-dingri@hotmail.co.uk')
        Email = ('donotreply_volac@hotmail.co.uk')
        try:
            self.mail.login('donotreply_volac@hotmail.co.uk','toffee2015')
        except smtplib.SMTPServerDisconnected:
            print("not valid")

        Content = ("The following item has 90 days left before the warranty will run out:\n\nHardware ID: {0}\nHardware Item: {1}".format(HardwareIDs[0],HardwareModel[0]))
        Subject = ("Warranty Expiration Warning")

        Body = ("Subject: {0}\n\n{1}".format(Subject,Content))

        self.mail.sendmail(Email,IT_Staff_Email,Body)
        self.mail.quit()

    def MenuBar(self):
        self.menubar = AdminMenuBar()
        self.setMenuBar(self.menubar) ##Calls menubar from another python file
        

    def Log_Out(self):
        self.close()

    def Change_Password(self):
        self.ChangePassword_window = ChangePassword(self.account_details)
        self.ChangePassword_window.exec_()
        
        
    def MainMenu(self):
        self.MainMenuWindow = AdminMainMenu()
        self.stacked_layout.addWidget(self.MainMenuWindow)
        self.setMaximumSize(750,400)
        self.setMinimumSize(750,400)
 
        

    def SwitchToOpenDatabase(self):
        self.stacked_layout.setCurrentIndex(1)
        self.setMaximumSize(1500,800)
        self.setMinimumSize(800,500)

    def SwitchToSearch(self):
        self.stacked_layout.setCurrentIndex(2)
        self.setMaximumSize(900,700)
        self.setMinimumSize(750,500)

    def BackToMenu(self):
        self.stacked_layout.setCurrentIndex(0)
        self.setMinimumSize(750,400)
        self.setMaximumSize(750,400)
        

    def OpenDatabaseWidget_Method(self):
        self.OpenDatabaseWindow = OpenDatabase()
        
        self.stacked_layout.addWidget(self.OpenDatabaseWindow)
        
            


    def RemoveData_btnClick(self):
        if self.OpenDatabaseWindow.DeleteRC == True:
            self.resize(765,420)
        else:
            self.resize(635,420)

            

    def BrowseDatabase(self): 
        """This opens the file finder to choose the database"""
        try:
            filename = QFileDialog.getOpenFileName(self,'Open File')
            f = open(filename,'r')
            if "Volac" not in filename:
                BlankFieldsWarning = Presence_Dialog("{0:^50}".format("Incorrect File Opened. Please Try Again."))
                BlankFieldsWarning.exec_()
                return
            with sqlite3.connect(filename) as db:
                cursor = db.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
                items = cursor.fetchall() ### Gets all the table names
                db.commit()
            for count in range(len(items)):
                items[count] = str(items[count])
                items[count] = items[count].strip("()'',")
                self.OpenDatabaseWindow.Database_CB.addItem(items[count]) ## Adds all the tables to the dropdown box

        except FileNotFoundError:
            pass

    


    def SearchStaff(self):
        self.resize(700,500)
        self.SearchStaffWindow = SearchStaff()
        self.stacked_layout.addWidget(self.SearchStaffWindow)
        
        
    def AddDataGUI(self):
        CurrentCBValue = self.OpenDatabaseWindow.Database_CB.currentText()
        AddDataGUI = AddDataWindow(CurrentCBValue)
        AddDataGUI.exec_() ## executes dialog box
        self.OpenDatabaseWindow.ChosenTableMethod()
        

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = CurrentLayoutAdmin(None)
    launcher.show()
    launcher.raise_()
    app.exec_()
        
        
