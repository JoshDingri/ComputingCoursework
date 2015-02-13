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
        self.account_details = account_details
        self.MainMenu()
        self.CheckExpirationDates()
        self.MenuBar() ## Calls menubar definition
##        self.stacked_layout = QStackedLayout()
##        self.stacked_layout.addWidget(self.MainMenuWidget)
##        self.central_widget = QWidget()
##        self.central_widget.setLayout(self.stacked_layout)
##        self.setCentralWidget(self.central_widget)
    

    def CheckExpirationDates(self):
        self.currentdate = time.strftime("%d-%m-%y")
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = ("SELECT PurchaseDate FROM StaffHardware")
            cursor.execute(sql)
        purchasedates = [item[0] for item in cursor.fetchall()]


        b = "(', )" 
            
        for count in range (len(purchasedates)):
            for i in range(0,len(b)):
                purchasedates[count] = str(purchasedates[count]).replace(b[i],"")
                self.expiringitem = purchasedates[count]

            currentdate = datetime.datetime.strptime(self.currentdate,"%d-%m-%y")
            self.purchasedate = datetime.datetime.strptime(purchasedates[count],"%d-%m-%y")

            
            daysleft = self.purchasedate - currentdate
            if daysleft.days == 6:
                self.SendExpirationEmail()

    def SendExpirationEmail(self):
        self.purchasedate = self.purchasedate.strftime("%d-%m-%y")
        self.purchasedate =  ("    " + self.purchasedate)
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = ("SELECT HardwareID FROM StaffHardware WHERE PurchaseDate='{}'".format(self.purchasedate))
            cursor.execute(sql)
            HardwareIDs = list(cursor.fetchone())
            db.commit()

        print(HardwareIDs[0])

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = ("SELECT HardwareModelID FROM Hardware WHERE HardwareID='{}'".format(HardwareIDs[0]))
            cursor.execute(sql)
            ModelID = list(cursor.fetchone())
            db.commit()

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = ("SELECT HardwareModelName FROM HardwareModel WHERE HardwareModelID='{}'".format(ModelID[0]))
            cursor.execute(sql)
            HardwareModel = list(cursor.fetchone())
            db.commit()

        print(HardwareModel[0])
        
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
        print(Body)

        self.mail.sendmail(Email,IT_Staff_Email,Body)
        self.mail.quit()

    def MenuBar(self):       
        MenuBarAdmin.MenuBar(self) ##Calls menubar from another python file

    def Log_Out(self):
        self.close()

    def Change_Password(self):
        self.ChangePassword_window = ChangePassword(self.account_details)
        self.ChangePassword_window.exec_()
        
        
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
    launcher = CurrentLayoutAdmin(None)
    launcher.show()
    launcher.raise_()
    app.exec_()
        
        
