from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from MainProgram import *
from Calender import *
import string

class AddDataWindow(QDialog):
    """The new window for entering data"""

    def __init__(self,CurrentCBValue):  ##CurrentCBValue is the table selected from dropdown box. Passed in from main program
            
            self.linelist = []
            self.dateclicked = False
            
            super().__init__()

            self.resize(500,180)
        
            self.grid = QGridLayout()
            self.verticle = QVBoxLayout()
            self.horizontal = QHBoxLayout()

                
            with sqlite3.connect("Volac.db") as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM {}".format(CurrentCBValue))
                    db.commit()
            self.col = [tuple[0] for tuple in cursor.description]   ##Gets the column names and adds the to a tuple

            positions = [(i,j) for i in range (int(round(len(self.col)/2,1)+1)) for j in range(4)]     ##works out how many rows down and how many rows accross the grid needs
            self.col = sum([[i,''] for i in self.col],[])   ## adds a space in between each item in self.col tuple
            ##The code below will work out where the different labels and line edits need to go
                    
            count = 0
            PurchaseDateExist = False
            WarrantyDateExists = False
            DepartmentID_CB = False
            self.CurrentLineEditExists = False
            LocationID_CB = False
            HardwareModelID_CB = False
            HardwareMakeID_CB = False
            StaffID_CB = False
            HardwareID_CB = False
            DeviceID_CB = False
            
            for position, name in zip(positions,self.col):
                if name == '':   ##This replaces all the spaces with line edits
                    self.LE = QLineEdit()
                    self.LE.setFixedHeight(22)
                    self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                    self.linelist[count].setStyleSheet("background-color: White; border-radius: 3px; border: 2px solid black; background-image: url('icons_trick.png')")
                    self.linelist[count].textChanged.connect(self.PresenceValid)
                    self.grid.addWidget(self.linelist[count],*position) 
                    count+=1
                    self.linelist[0].setText('Autonumber')   ##The first label/line edit will always be a ID, since IDs are autoupdated the line edit has default text
                    self.linelist[0].setReadOnly(True)   ## Line edit is read only
                    if PurchaseDateExist == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.CurrentLineEdit = count
                            self.LE = QLineEdit()
                            self.calander_btn = QPushButton()
                            self.calander_btn.setFixedWidth(50)

                            pixmap = QPixmap('calendar-icon.png')
                            ButtonIcon = QIcon(pixmap)
                            self.calander_btn.setIcon(ButtonIcon)
                            self.calander_btn.setIconSize(QSize(13,13))

                            
                            self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.grid.addWidget(self.linelist[count],*position)
                            self.grid.addWidget(self.calander_btn,*position)
                            self.calander_btn.clicked.connect(self.OpenCalander)
                            count+=1
                            PurchaseDateExist = False
                            
                    if DepartmentID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.DepartmentLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT DepartmentName FROM Department"
                                cursor.execute(sql)
                            Departments = [item[0] for item in cursor.fetchall()]
                            self.departmentCB = QComboBox()
                            self.departmentCB.setFixedHeight(25)
                            self.departmentCB.setFixedWidth(200)
                            self.departmentCB.addItems(Departments)
                            self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.grid.addWidget(self.linelist[count],*position)
                            self.grid.addWidget(self.departmentCB,*position)
                            count+=1
                            self.departmentCB.activated[str].connect(self.DepartmentComboBox_Activated)
                            DepartmentID_CB = False
                            

                    if LocationID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.LocationLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT AddressLine3 FROM Location"
                                cursor.execute(sql)
                            Locations = [item[0] for item in cursor.fetchall()]
                            self.LocationCB = QComboBox()
                            self.LocationCB.setFixedHeight(25)
                            self.LocationCB.setFixedWidth(200)
                            self.LocationCB.addItems(Locations)
                            self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.grid.addWidget(self.linelist[count],*position)
                            self.grid.addWidget(self.LocationCB,*position)
                            count+=1
                            self.LocationCB.activated[str].connect(self.LocationComboBox_Activated)
                            LocationID_CB = False

                    if HardwareModelID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.HardwareModelLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT HardwareModelName FROM HardwareModel"
                                cursor.execute(sql)
                            HardwareModels = [item[0] for item in cursor.fetchall()]
                            self.HardwareModelCB = QComboBox()
                            self.HardwareModelCB.setFixedHeight(30)
                            self.HardwareModelCB.addItems(HardwareModels)
                            self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.grid.addWidget(self.linelist[count],*position)
                            self.grid.addWidget(self.HardwareModelCB,*position)
                            count+=1
                            self.HardwareModelCB.activated[str].connect(self.HardwareModelComboBox_Activated)
                            HardwareModelID_CB = False

                    if HardwareMakeID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.HardwarMakeLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT HardwareMakeName FROM HardwareMake"
                                cursor.execute(sql)
                            HardwareMakes = [item[0] for item in cursor.fetchall()]
                            self.HardwareMakeCB = QComboBox()
                            self.HardwareMakeCB.setFixedHeight(30)
                            self.HardwareMakeCB.addItems(HardwareMakes)
                            self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.grid.addWidget(self.linelist[count],*position)
                            self.grid.addWidget(self.HardwareMakeCB,*position)
                            count+=1
                            self.HardwareMakeCB.activated[str].connect(self.HardwareMakeComboBox_Activated)
                            HardwareMakeID_CB = False

                    if StaffID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.StaffLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT FirstName,Surname FROM Staff"
                                cursor.execute(sql)
                            self.Staff = [item[0] + ', ' + item[1] for item in cursor.fetchall()] #device and model
                            self.StaffCB = QComboBox()
                            self.StaffCB.setFixedHeight(30)
                            self.StaffCB.addItems(self.Staff)
                            self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.grid.addWidget(self.linelist[count],*position)
                            self.grid.addWidget(self.StaffCB,*position)
                            count+=1
                            self.StaffCB.activated[str].connect(self.StaffComboBox_Activated)
                            StaffID_CB = False

                    if HardwareID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.HardwareLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT HardwareMake.HardwareMakeName,HardwareModel.HardwareModelName FROM HardwareMake,HardwareModel"
                                cursor.execute(sql)
                            self.Hardware = [item[0] + ', ' + item[1] for item in cursor.fetchall()]
                            print(self.Hardware)
                            self.HardwareCB = QComboBox()
                            self.HardwareCB.setFixedHeight(30)
                            self.HardwareCB.addItems(self.Hardware)
                            self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.grid.addWidget(self.linelist[count],*position)
                            self.grid.addWidget(self.HardwareCB,*position)
                            count+=1
                            self.HardwareCB.activated[str].connect(self.HardwareComboBox_Activated)
                            StaffID_CB = False

                    if DeviceID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.DeviceLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT DeviceName FROM DeviceType"
                                cursor.execute(sql)
                            Devices = [item[0] for item in cursor.fetchall()]
                            self.DeviceCB = QComboBox()
                            self.DeviceCB.setFixedHeight(30)
                            self.DeviceCB.addItems(Devices)
                            self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.grid.addWidget(self.linelist[count],*position)
                            self.grid.addWidget(self.Devices,*position)
                            count+=1
                            self.DeviceCB.activated[str].connect(self.DeviceComboBox_Activated)
                            DeviceID_CB = False


                    
                            
                    
                elif name == 'PurchaseDate' or name == 'WarrantyExpirationDate':
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)
                    PurchaseDateExist = True

                elif name == 'DepartmentID':# or name == 'LocationID' or name == 'HardwareModelID' or name == 'HardwareMakeID' or name == 'StaffID' or name == 'HardwareID':
                    if count == 0:
                        label = QLabel(name)
                        self.grid.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)
                    DepartmentID_CB = True

                elif name == 'LocationID':
                    if count == 0:
                        label = QLabel(name)
                        self.grid.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)
                    LocationID_CB = True
                    
                elif name == 'HardwareModelID':
                    if count == 0:
                        label = QLabel(name)
                        self.grid.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)
                    HardwareModelID_CB = True
                    
                elif name == 'HardwareMakeID':
                    if count == 0:
                        label = QLabel(name)
                        self.grid.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)
                    HardwareMakeID_CB = True
                    
                elif name == 'StaffID':
                    if count == 0:
                        label = QLabel(name)
                        self.grid.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)
                    StaffID_CB = True
                    
                elif name == 'HardwareID':
                    if count == 0:
                        label = QLabel(name)
                        self.grid.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)
                    HardwareID_CB = True

                elif name == 'DeviceID':
                    if count == 0:
                        label = QLabel(name)
                        self.grid.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)
                    DeviceID_CB = True
                    
                else:
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)

            self.AddData_Choice = QPushButton("Add Data")
            self.Cancel_Choice = QPushButton("Cancel")
            
            self.verticle.addLayout(self.grid)  ## Layouts are all added, the grid is added to a verticle layout along with the push buttons
            
            self.horizontal.addWidget(self.AddData_Choice)
            self.horizontal.addWidget(self.Cancel_Choice)

            self.verticle.addLayout(self.horizontal)


            ### The code below (in this method) will make lists/tuples into strings that work with SQL statements


            ID = str(self.col[0])   ##The xxID will be replaced since it is not needed for SQL

            for n,i in enumerate(self.col):
                if i == ID:
                    self.col[n] = (CurrentCBValue+'(') ##The xxID is replaced with the table name in the format TableName(xx, xx, xx)

            self.col[-1] = self.col[-1]+')' ##The last item in the column list will need a bracket at the end

        
            b = "[]'',"     ## b holds all chracters that need replacing when converting to a string
            
            
            self.col = str(self.col)


            for i in range(0,len(b)):
                self.col = self.col.replace(b[i],"")    ## replaces chracters with a space



            self.col = ", ".join(self.col.split())  ## addes a comma in between each item in the string

            self.col = self.col.replace("(, ","(")  ##Ignores the first comma and space
            self.col = self.col.replace(", )",")")  ##Ignores the last comma and space


    
            self.setLayout(self.verticle)

            self.CurrentCBValue = CurrentCBValue ##makes the current selected table available for other methods


            self.AddData_Choice.clicked.connect(self.Commit_Changes) ## Button click will run chosen method
            self.Cancel_Choice.clicked.connect(self.Close_window) ## Closes the Add data GUI
            
    def PresenceValid(self):
        for count in range(len(self.linelist)):
            text = self.linelist[count].text()
            if text == '':
                self.linelist[count].setStyleSheet("background-color: White; border-radius: 3px; border: 2px solid black")
            else:
                self.linelist[count].setStyleSheet("background-color: #C7DE43; border-radius: 3px; border: 2px solid black")
        


    def Close_window(self):
        self.reject()
        

    def OpenCalander(self):
        CalenderWidget = Calendar()
        CalenderWidget.exec_()
        self.linelist[self.CurrentLineEdit].setText('    '+CalenderWidget.date)
        self.linelist[self.CurrentLineEdit].setAlignment(Qt.AlignCenter)

    def DepartmentComboBox_Activated(self,text):
        print(text)
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT DepartmentID FROM Department WHERE DepartmentName='{}'".format(text)
            cursor.execute(sql)
            department = list(cursor.fetchone())
        self.linelist[self.DepartmentLineEdit].setText(str(department[0]))

    def LocationComboBox_Activated(self,text):
        print(text)    
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT LocationID FROM Location WHERE AddressLine3='{}'".format(text)
            cursor.execute(sql)
            location = list(cursor.fetchone())
            
        self.linelist[self.LocationLineEdit].setText(str(location[0]))

    def HardwareModelComboBox_Activated(self,text):
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT HardwareModelID FROM HardwareModel WHERE HardwareModelName='{}'".format(text)
            cursor.execute(sql)
            hardwaremodel = list(cursor.fetchone())
        self.linelist[self.HardwareModelLineEdit].setText(str(hardwaremodel[0]))


    def HardwareMakeComboBox_Activated(self,text):            
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT HardwareMakeID FROM HardwareMake WHERE HardwareMakeName='{}'".format(text)
            cursor.execute(sql)
            HardwareMake = list(cursor.fetchone())
            db.commit()
        self.linelist[self.HardwarMakeLineEdit].setText(str(HardwareMake[0]))

    def StaffComboBox_Activated(self,text):
        FullStaff = str(self.Staff[0])
        split = [x.strip() for x in FullStaff.split(',')]
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT StaffID FROM Staff WHERE Surname ='{}' AND FirstName ='{}'".format(split[1],split[0])
            cursor.execute(sql)
            StaffsID = list(cursor.fetchone())
        self.linelist[self.StaffLineEdit].setText(str(StaffsID[0]))
        

    def HardwareComboBox_Activated(self,text):
        FullHardware = str(self.Hardware[0])
        split = [x.strip() for x in FullHardware.split(',')]
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT HardwareMake.HardwareMakeID,HardwareModel.HardwareModelID FROM HardwareMake,HardwareModel WHERE HardwareMake.HardwareMakeName ='{}' AND HardwareModel.HardwareModelName ='{}'".format(split[0],split[1])
            cursor.execute(sql)
            HardwareIDs = list(cursor.fetchone())
        self.linelist[self.HardwareLineEdit].setText(str(HardwareIDs[0]))

    def DeviceComboBox_Activated(self,text):            
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT DeviceID FROM DeviceType WHERE DeviceName='{}'".format(text)
            cursor.execute(sql)
            Device = list(cursor.fetchone())
            db.commit()
        self.linelist[self.DeviceLineEdit].setText(str(Device[0]))
            

    def Commit_Changes(self):
        data = []
        values = []
        for count in range(len(self.linelist)):
            data.append(self.linelist[count].text())
            if 'Autonumber' in data:
                data.remove('Autonumber')   ## Removes the autonumber field from the list.
            elif '' in data:
                data.remove('')
                
        for count in range(len(data)):
            values.append('?')      ## creats specific amount of placeholders

        ## Converts placeholders to a string
            
        values = (str(values).replace('[','('))
        values = (str(values).replace(']',')'))
        values = values.replace("'","")


        ## Adds entered data into database

        with sqlite3.connect("Volac.db") as db:
                cursor = db.cursor()
                sql = "insert into {0} values {1}".format(self.col,values)
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.execute(sql,data)
                db.commit()
        self.reject()
    
            


            

       
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = AddDataWindow('StaffHardware')
    launcher.show()
    launcher.raise_()
    app.exec_()
