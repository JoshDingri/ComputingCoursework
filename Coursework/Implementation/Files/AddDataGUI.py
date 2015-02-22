from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from Calender import *
import string

class AddDataWindow(QDialog):
    """The new window for entering data"""

    def __init__(self,CurrentCBValue):  ##CurrentCBValue is the table selected from dropdown box. Passed in from main program
            
            self.LineEditList = []      ##This list holds all the line edits for the window
            self.dateclicked = False
            
            super().__init__()

            self.resize(500,180)
        
            self.MainGridLayout = QGridLayout() ## The layouts of the window.
            self.VerticalLayout = QVBoxLayout()
            self.HorizontalLayout = QHBoxLayout()

                
            with sqlite3.connect("Volac.db") as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM {}".format(CurrentCBValue))
                    db.commit()
            self.col = [tuple[0] for tuple in cursor.description]   ##Gets the column names and adds them to a tuple

            positions = [(i,j) for i in range (int(round(len(self.col)/2,1)+1)) for j in range(4)]     ##works out how many rows down and how many rows accross the grid needs
            
            self.col = sum([[i,''] for i in self.col],[])   ## adds a space in between each item in self.col tuple
            
                    
            count = 0 # Holds the index number of the line edit list

            ## The below boolean variables are set to false and will later be changed if needed
            
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
            WarrantyCB = False
            CostValidation = False
            PhoneNumberValidation = False
            self.CostExists = False
            SerialValidation = False
            IMEIValidation = False
            WarrantyDate = False

            self.MainGridLayout.setHorizontalSpacing(20)
            self.MainGridLayout.setVerticalSpacing(10)
            

            ##The code below will work out where the different labels and line edits need to go ##
            
            
            for position, name in zip(positions,self.col):
                if name == '':   ##This replaces all the spaces with line edits
                    self.LE = QLineEdit()
                    self.LineEditList.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                    self.LineEditList[count].setStyleSheet("background-color: White; border-radius: 3px; border: 2px solid black; background-image: url('icons_trick.png')")
                    self.LineEditList[count].textChanged.connect(self.PresenceValid)
                    self.LineEditList[count].setFixedHeight(25)
                    self.MainGridLayout.addWidget(self.LineEditList[count],*position) 
                    count+=1
                    self.LineEditList[0].setText('Autonumber')   ##The first label/line edit will always be a Primary Key, since IDs are autoupdated the line edit has default text
                    self.LineEditList[0].setReadOnly(True)   ## Line edit is read only
                    
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


                            self.MainGridLayout.addWidget(self.LineEditList[count-1],*position)
                            self.MainGridLayout.addWidget(self.calander_btn,*position)
                            self.calander_btn.clicked.connect(self.OpenCalander)
                            PurchaseDateExist = False
                            
                    if WarrantyDate == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.CurrentLineEdit = count
                            self.calander_btn = QPushButton()
                            self.calander_btn.setFixedWidth(50)

                            pixmap = QPixmap('calendar-icon.png')
                            ButtonIcon = QIcon(pixmap)
                            self.calander_btn.setIcon(ButtonIcon)
                            self.calander_btn.setIconSize(QSize(13,13))

                            self.LineEditList[count-1].setText('-')
                            self.LineEditList[count-1].setEnabled(False)
                            self.calander_btn.hide()
                            self.MainGridLayout.addWidget(self.LineEditList[count-1],*position)
                            self.MainGridLayout.addWidget(self.calander_btn,*position)
                            self.calander_btn.clicked.connect(self.OpenCalander)
                            WarrantyDate = False
                            
                    if DepartmentID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.DepartmentLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT DepartmentName FROM Department"
                                cursor.execute(sql)
                                db.commit()
                            Departments = [item[0] for item in cursor.fetchall()]
                            self.departmentCB = QComboBox()
                            self.departmentCB.setFixedHeight(25)
                            self.departmentCB.setFixedWidth(200)
                            self.departmentCB.addItems(Departments)
                            self.LineEditList.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.MainGridLayout.addWidget(self.LineEditList[count],*position)
                            self.MainGridLayout.addWidget(self.departmentCB,*position)
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
                                db.commit()
                            Locations = [item[0] for item in cursor.fetchall()]
                            self.LocationCB = QComboBox()
                            self.LocationCB.setFixedHeight(25)
                            self.LocationCB.setFixedWidth(200)
                            self.LocationCB.addItems(Locations)
                            self.LineEditList.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.MainGridLayout.addWidget(self.LineEditList[count],*position)
                            self.MainGridLayout.addWidget(self.LocationCB,*position)
                            count+=1
                            self.LocationCB.activated[str].connect(self.LocationComboBox_Activated)
                            LocationID_CB = False



                    if HardwareMakeID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.HardwarMakeLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT HardwareMakeName FROM HardwareMake"
                                cursor.execute(sql)
                                db.commit()
                            HardwareMakes = [item[0] for item in cursor.fetchall()]
                            self.HardwareMakeCB = QComboBox()
                            self.HardwareMakeCB.setFixedHeight(30)
                            self.HardwareMakeCB.addItems(HardwareMakes)
                            self.LineEditList.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.MainGridLayout.addWidget(self.LineEditList[count],*position)
                            self.MainGridLayout.addWidget(self.HardwareMakeCB,*position)
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
                                db.commit()
                            self.Staff = [item[0] + ', ' + item[1] for item in cursor.fetchall()] #device and model
                            print(self.Staff)
                            self.StaffCB = QComboBox()
                            self.StaffCB.setFixedHeight(25)
                            self.StaffCB.addItems(self.Staff)
                            self.LineEditList.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.MainGridLayout.addWidget(self.LineEditList[count],*position)
                            self.MainGridLayout.addWidget(self.StaffCB,*position)
                            count+=1
                            self.StaffCB.activated[str].connect(self.StaffComboBox_Activated)
                            StaffID_CB = False

                    if HardwareModelID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.HardwareLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT HardwareMakeName FROM HardwareMake"
                                cursor.execute(sql)
                                db.commit()
                            self.Hardware = [item[0] for item in cursor.fetchall()]
                            print(self.Hardware)
                            self.HardwareCB = QComboBox()
                            self.HardwareCB.setFixedHeight(30)
                            self.HardwareCB.addItems(self.Hardware)
                            self.LineEditList.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.MainGridLayout.addWidget(self.LineEditList[count],*position)
                            self.MainGridLayout.addWidget(self.HardwareCB,*position)
                            count+=1
                            self.HardwareCB.activated[str].connect(self.SelectModel)
                            
                            HardwareModelID_CB = False

                    if HardwareID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.HardwareLineEdit = count
                            self.LE = QLineEdit()
                            
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT HardwareModelID FROM Hardware"
                                cursor.execute(sql)
                                db.commit()
                            hardwaremodelid = [item[0] for item in cursor.fetchall()]
                            hardwaremodelid = str(hardwaremodelid).replace("[","(")
                            self.hardwaremodelid = hardwaremodelid.replace("]",")")
                            print(self.hardwaremodelid)
                            
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT HardwareMakeID FROM HardwareModel WHERE HardwareModelID IN {}".format(self.hardwaremodelid)
                                cursor.execute(sql)
                                db.commit()
                                
                            self.MakeID = [item[0] for item in cursor.fetchall()]
                            self.MakeID = str(self.MakeID).replace("[","(")
                            self.MakeID = self.MakeID.replace("]",")")
                            
                            
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT HardwareMakeName FROM HardwareMake WHERE HardwareMakeID IN {}".format(self.MakeID)
                                cursor.execute(sql)
                                db.commit()
                            self.Hardware = [item[0] for item in cursor.fetchall()]
                                
                            self.HardwareCB = QComboBox()
                            self.HardwareCB.setFixedHeight(30)
                            self.HardwareCB.addItems(self.Hardware)
                            self.LineEditList.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.MainGridLayout.addWidget(self.LineEditList[count],*position)
                            self.MainGridLayout.addWidget(self.HardwareCB,*position)
                            count+=1
                            self.HardwareCB.activated[str].connect(self.SelectModelFromHardware)
                            
                            HardwareID_CB = False



                    if DeviceID_CB == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            if self.CurrentLineEditExists == False:
                                self.DeviceLineEdit = count
                            self.LE = QLineEdit()
                            with sqlite3.connect("Volac.db") as db:
                                cursor = db.cursor()
                                sql = "SELECT DeviceName FROM DeviceType"
                                cursor.execute(sql)
                                db.commit()
                            Devices = [item[0] for item in cursor.fetchall()]
                            self.DeviceCB = QComboBox()
                            self.DeviceCB.setFixedHeight(30)
                            self.DeviceCB.addItems(Devices)
                            self.LineEditList.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                            self.MainGridLayout.addWidget(self.LineEditList[count],*position)
                            self.MainGridLayout.addWidget(self.DeviceCB,*position)
                            count+=1
                            self.DeviceCB.activated[str].connect(self.DeviceComboBox_Activated)
                            DeviceID_CB = False

                    if WarrantyCB == True:
                            self.CheckBoxLineEdit = count
                            self.CostSB = QCheckBox()
                            self.LineEditList[count-1].setText('False')
                            self.LineEditList[count-1].hide()
                            

                            self.MainGridLayout.addWidget(self.CostSB,*position)
                            self.CostSB.toggled.connect(self.CheckBox)
                            WarrantyCB = False

                    if CostValidation == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            self.LineEditList[count-1].setValidator(QIntValidator())
                            CostValidation = False

                    if PhoneNumberValidation == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            PhoneNumberRegExp = QRegExp("/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/")
                            self.PhoneNumberLineEdit = count-1
                            self.LineEditList[count-1].setText('-')
                            self.LineEditList[count-1].setEnabled(False)
                            self.LineEditList[count-1].setValidator(QRegExpValidator(PhoneNumberRegExp))
                            self.LineEditList[count-1].setMaxLength(12)
                            PhoneNumberValidation = False

                    if SerialValidation == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            Regexp = QRegExp("[A-Z0-9]{1,20}")
                            self.LineEditList[count-1].setValidator(QRegExpValidator(Regexp))
                            self.LineEditList[count-1].setPlaceholderText("Must Be In Capitals")
                            SerialValidation = False

                    if IMEIValidation == True:
                        if name == '':   ##This replaces all the spaces with line edits
                            self.IMEILineEdit = count-1
                            Regexp = QRegExp("[0-9]{1,20}")
                            self.LineEditList[count-1].setText('-')
                            self.LineEditList[count-1].setEnabled(False)
                            self.LineEditList[count-1].setValidator(QRegExpValidator(Regexp))
                            IMEIValidation = False

                    
                ## The below will check if a label exists with the name given and then will run the above if statements
                    
                elif name == 'WarrantyExpirationDate':
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    WarrantyDate = True

                elif name == 'PurchaseDate':
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    PurchaseDateExist = True
                
                elif name == "IMEINumber":
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    IMEIValidation = True
                    
                elif name == "SerialNumber":
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    SerialValidation = True

                elif name == 'Warranty':
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    WarrantyCB = True

                elif name == 'Cost':
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    CostValidation = True
                    self.Cost_Validation = count
                    self.CostExists = True

                elif name == 'PhoneNumber':
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    PhoneNumberValidation = True
                    self.PhoneNumber_Validation = count

                elif name == 'JobTitle':
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    self.JobTitle_Validation = count

                

                elif name == 'DepartmentID':
                    if count == 0:
                        label = QLabel(name)
                        label.setAlignment(Qt.AlignCenter)
                        self.MainGridLayout.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    DepartmentID_CB = True

                elif name == 'LocationID':
                    if count == 0:
                        label = QLabel(name)
                        label.setAlignment(Qt.AlignCenter)
                        self.MainGridLayout.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    LocationID_CB = True
                    
                elif name == 'HardwareModelID':
                    if count == 0:
                        label = QLabel(name)
                        label.setAlignment(Qt.AlignCenter)
                        self.MainGridLayout.addWidget(label,*position)
                        continue
                    name = "HarwareItem"
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    HardwareModelID_CB = True
                    
                elif name == 'HardwareMakeID':
                    if count == 0:
                        label = QLabel(name)
                        label.setAlignment(Qt.AlignCenter)
                        self.MainGridLayout.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    HardwareMakeID_CB = True
                    
                elif name == 'StaffID':
                    if count == 0:
                        label = QLabel(name)
                        label.setAlignment(Qt.AlignCenter)
                        self.MainGridLayout.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    StaffID_CB = True
                    
                elif name == 'HardwareID':
                    if count == 0:
                        label = QLabel(name)
                        label.setAlignment(Qt.AlignCenter)
                        self.MainGridLayout.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    HardwareID_CB = True

                elif name == 'DeviceID':
                    if count == 0:
                        label = QLabel(name)
                        label.setAlignment(Qt.AlignCenter)
                        self.MainGridLayout.addWidget(label,*position)
                        continue
                    name = name[:-2]
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)
                    DeviceID_CB = True
                    
                else:
                    label = QLabel(name)
                    label.setAlignment(Qt.AlignCenter)
                    self.MainGridLayout.addWidget(label,*position)

            self.AddData_Choice = QPushButton("Add Data")
            self.Cancel_Choice = QPushButton("Cancel")
            
            self.VerticalLayout.addLayout(self.MainGridLayout)  ## Layouts are all added, the grid is added to a verticle layout along with the push buttons
            
            self.HorizontalLayout.addWidget(self.AddData_Choice)
            self.HorizontalLayout.addWidget(self.Cancel_Choice)

            self.VerticalLayout.addLayout(self.HorizontalLayout)


            ### The code below will make lists/tuples into strings that work with SQL statements


            ID = str(self.col[0])   ##The Primary Key will be replaced since it is not needed for SQL

            for n,i in enumerate(self.col):
                if i == ID:
                    self.col[n] = (CurrentCBValue+'(') ##The Primary Key is replaced with the table name in the format TableName(xx, xx, xx)

            self.col[-1] = self.col[-1]+')' ##The last item in the column list will need a bracket at the end

        
            b = "[]'',"     ## b holds all chracters that need replacing when converting to a string
            
            
            self.col = str(self.col)


            for i in range(0,len(b)):
                self.col = self.col.replace(b[i],"")    ## replaces chracters with a space



            self.col = ", ".join(self.col.split())  ## addes a comma in between each item in the string

            self.col = self.col.replace("(, ","(")  ##Ignores the first comma and space
            self.col = self.col.replace(", )",")")  ##Ignores the last comma and space


    
            self.setLayout(self.VerticalLayout)

            self.CurrentCBValue = CurrentCBValue ##makes the current selected table available for other methods


            self.AddData_Choice.clicked.connect(self.Commit_Changes) ## Button click will run chosen method
            self.Cancel_Choice.clicked.connect(self.Close_window) ## Closes the Add data GUI
            
    def PresenceValid(self):
        """Will change line edit colours depending on the text in each lineedit"""
        
        for count in range(len(self.LineEditList)):
            text = self.LineEditList[count].text()
            if text == '':
                self.LineEditList[count].setStyleSheet("background-color: White; border-radius: 3px; border: 2px solid black")
            elif text == '-':
                self.LineEditList[count].setStyleSheet("background-color: #D3D3D3; border-radius: 3px; border: 2px solid black")
            else:
                self.LineEditList[count].setStyleSheet("background-color: #C7DE43; border-radius: 3px; border: 2px solid black")
        


    def Close_window(self):
        self.reject()

    def CheckBox(self):
        if self.CostSB.isChecked():
            self.LineEditList[self.CheckBoxLineEdit-1].setText('True')
            self.calander_btn.show()
        else:
            self.LineEditList[self.CheckBoxLineEdit-1].setText('False')
            self.calander_btn.hide()
            self.LineEditList[self.CurrentLineEdit-1].clear()
            self.LineEditList[self.CurrentLineEdit-1].setText('-')

    def OpenCalander(self):
        CalenderWidget = Calendar()
        CalenderWidget.exec_()
        self.LineEditList[self.CurrentLineEdit-1].setText("{0:>16}".format(CalenderWidget.date))
        self.LineEditList[self.CurrentLineEdit-1].setAlignment(Qt.AlignCenter)

    def DepartmentComboBox_Activated(self,text):
        print(text)
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT DepartmentID FROM Department WHERE DepartmentName=?",(text,))
            department = list(cursor.fetchone())
            db.commit()
        self.LineEditList[self.DepartmentLineEdit].setText(str(department[0]))

    def LocationComboBox_Activated(self,text):
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT LocationID FROM Location WHERE AddressLine3=?",(text,))
            location = list(cursor.fetchone())
            db.commit()
            
        self.LineEditList[self.LocationLineEdit].setText(str(location[0]))

    def HardwareModelComboBox_Activated(self,text):
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareModelID FROM HardwareModel WHERE HardwareModelName=?",(text,))
            hardwaremodel = list(cursor.fetchone())
            db.commit()
        self.LineEditList[self.HardwareModelLineEdit].setText(str(hardwaremodel[0]))


    def HardwareMakeComboBox_Activated(self,text):            
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareMakeID FROM HardwareMake WHERE HardwareMakeName=?",(text,))
            HardwareMake = list(cursor.fetchone())
            db.commit()
        self.LineEditList[self.HardwarMakeLineEdit].setText(str(HardwareMake[0]))

    def StaffComboBox_Activated(self,text):
        FullStaff = text
        print(FullStaff)
        split = tuple(x.strip() for x in FullStaff.split(','))
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT StaffID FROM Staff WHERE Surname =? AND FirstName =?",(split[1],split[0],))
            StaffsID = list(cursor.fetchone())
            db.commit()
        self.LineEditList[self.StaffLineEdit].setText(str(StaffsID[0]))

    def SelectModel(self,text):
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareMakeID FROM HardwareMake WHERE HardwareMakeName =?",(text,))
            HardwareID = list(cursor.fetchone())
            db.commit()
            
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareModelName FROM HardwareModel WHERE HardwareMakeID=?",(HardwareID[0],))
            db.commit()
        self.Model = [item[0] for item in cursor.fetchall()]
        
        ModelLineEdit = QLineEdit()
        self.MainGridLayout.addWidget(ModelLineEdit,4,2)
        self.ModelCB = QComboBox()
        self.ModelCB.setFixedHeight(30)
        self.ModelCB.addItems(self.Model)
        self.MainGridLayout.addWidget(self.ModelCB,4,2)

        self.ModelCB.activated.connect(self.DisplayMakeModel)

    def SelectModelFromHardware(self,text):

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareMakeID FROM HardwareMake WHERE HardwareMakeName =?",(text,))
            db.commit()
        HardwareMakeID  = [item[0] for item in cursor.fetchall()]
        
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            sql = "SELECT HardwareModelID FROM Hardware"
            cursor.execute(sql)
            db.commit()
        HardwareModels  = [item[0] for item in cursor.fetchall()]
        HardwareModels = str(HardwareModels).replace("[","(")
        HardwareModels = HardwareModels.replace("]",")")
        
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareModelName FROM HardwareModel WHERE HardwareMakeID = '{}' AND HardwareModelID IN {}".format(HardwareMakeID[0],HardwareModels))
            db.commit()
        
        self.ModelHardware = [item[0] for item in cursor.fetchall()]
        
        ModelLineEdit = QLineEdit()
        self.MainGridLayout.addWidget(ModelLineEdit,4,3)
        self.ModelCB = QComboBox()
        self.ModelCB.setFixedHeight(30)
        self.ModelCB.addItems(self.ModelHardware)
        self.MainGridLayout.addWidget(self.ModelCB,4,3)

        self.ModelCB.activated.connect(self.HardwareComboBox_Activated)

    def DisplayMakeModel(self):
        MakeName = (self.HardwareCB.currentText())
        ModelName = (self.ModelCB.currentText())
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT HardwareModel.HardwareModelID FROM HardwareMake,HardwareModel WHERE HardwareMake.HardwareMakeName =? AND HardwareModel.HardwareModelName =?",(MakeName,ModelName,))
            HardwareIDs = list(cursor.fetchone())
            db.commit()
        self.LineEditList[self.HardwareLineEdit].setText(str(HardwareIDs[0]))

    def HardwareComboBox_Activated(self):
        MakeName = (self.HardwareCB.currentText())
        ModelName = (self.ModelCB.currentText())
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()            
            cursor.execute("SELECT HardwareModel.HardwareMakeID,HardwareModel.HardwareModelID FROM HardwareModel,HardwareMake WHERE HardwareMake.HardwareMakeName =? AND HardwareModelName =?",(MakeName,ModelName,))
            HardwareModelIDs = list(cursor.fetchone())
            db.commit()
            
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT Hardware.HardwareID FROM Hardware,HardwareModel WHERE Hardware.HardwareModelID =? AND HardwareModel.HardwareMakeID=?",(HardwareModelIDs[1],HardwareModelIDs[0],))
            HardwareID = list(cursor.fetchone())
            db.commit()
        self.LineEditList[self.HardwareLineEdit].setText(str(HardwareID[0]))

    def DeviceComboBox_Activated(self,text):
        if text == 'Phone':
            self.LineEditList[self.PhoneNumberLineEdit].setEnabled(True)
            self.LineEditList[self.IMEILineEdit].setEnabled(True)
            self.LineEditList[self.PhoneNumberLineEdit].clear()
            self.LineEditList[self.IMEILineEdit].clear()
        else:
            self.LineEditList[self.PhoneNumberLineEdit].setEnabled(False)
            self.LineEditList[self.IMEILineEdit].setEnabled(False)
            self.LineEditList[self.PhoneNumberLineEdit].setText('-')
            self.LineEditList[self.IMEILineEdit].setText('-')

            
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT DeviceID FROM DeviceType WHERE DeviceName=?",(text,))
            Device = list(cursor.fetchone())
            db.commit()
        self.LineEditList[self.DeviceLineEdit].setText(str(Device[0]))
            

    def Commit_Changes(self):
        Invalid = False
        data = []
        values = []
        for count in range(len(self.LineEditList)):
            if self.LineEditList[count].text() == '':
                self.LineEditList[count].setPlaceholderText('Field Cannot Be Blank')
                Invalid = True

            elif len(self.LineEditList[count].text()) > 25:
                self.LineEditList[count].clear()
                self.LineEditList[count].setPlaceholderText('Reached Maximum Characters (25)')
                Invalid = True
                
            else:
                Invalid = False
            
                
            data.append(self.LineEditList[count].text().lstrip())
            if 'Autonumber' in data:
                data.remove('Autonumber')   ## Removes the autonumber field from the list.
            elif '' in data:
                data.remove('')


                
        if self.CostExists == True:
            if (int(self.LineEditList[self.Cost_Validation].text())) > 2000:
                    self.LineEditList[self.Cost_Validation].clear()
                    self.LineEditList[self.Cost_Validation].setPlaceholderText('Price Invalid')
                    Invalid = True
            else:
                pass



            
                
        for count in range(len(data)):
            values.append('?')      ## creats specific amount of placeholders

        ## Converts placeholders to a string
            
        values = (str(values).replace('[','('))
        values = (str(values).replace(']',')'))
        values = values.replace("'","")


        ## Adds entered data into database
        try:
            with sqlite3.connect("Volac.db") as db:
                    cursor = db.cursor()
                    sql = "insert into {0} values {1}".format(self.col,values)
                    cursor.execute("PRAGMA foreign_keys = ON")
                    cursor.execute(sql,data)
                    db.commit()
            self.reject()
        except sqlite3.OperationalError:
            pass
    
            


            

       
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = AddDataWindow('StaffHardware')
    launcher.show()
    launcher.raise_()
    app.exec_()
