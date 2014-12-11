import sqlite3

def Menu():
    print("1) Staff Table")
    print("2) Hardware Table Table")    
    print("3) Hardware Make Table")
    print("4) Hardware Model Table")
    print("5) Device Type Table")
    print("6) Staff-Hardware Table")
    print("7) Department Table")
    print("8) Location Table")
    print("9) Department-Location Table")
    InputChoice()

def InputChoice():
    Choice = int(input("Enter menu choice: "))
    if Choice == 1:
        StaffTable()
    elif Choice == 2:
        HardwareTable()
    elif Choice == 3:
        HardwareMake()
    elif Choice == 4:
        HardwareModel()
    elif Choice == 5:
        DeviceType()
    elif Choice == 6:
        StaffHardware()
    elif Choice == 7:
        Department()
    elif Choice == 8:
        Location()
    elif Choice == 9:
        DepartmentLocation()

def EditMenu(table_name,field_names,ID,fields,values,amount):
    print("1) Insert Data")
    print("2) Update Data")
    print("3) Delete Data")
    MenuChoice(table_name,field_names,ID,fields,values,amount)

def MenuChoice(table_name,field_names,ID,fields,values,amount):
    choice = int(input())
    if choice == 1:
        InsertData(fields,values,amount)
    elif choice == 2:
        UpdatingData(table_name,field_names,ID,fields)
    elif choice == 3:
        DeletingData(table_name,ID)
    
    
def InsertData(fields,values,amount):
    data = []
    for count in range (amount):
        input_data = input()
        data.append(input_data)
    with sqlite3.connect("Volac.db") as db:
        try:
            cursor = db.cursor()
            sql = "insert into {0} values {1}".format(fields,values)
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(sql,data)
            db.commit()
        except sqlite3.IntegrityError:
            print()
            print("Error: This primary key has been referenced somewhere else!")

def DeletingData(table_name,ID):
    print("You are currently accessing the {0} table".format(table_name))
    ID_Choice = input("Which ID would you like to delete?: ")
    with sqlite3.connect("Volac.db") as db:
        try:
            cursor = db.cursor()
            sql = "delete from {0} where {1}={2}".format(table_name,ID,ID_Choice)
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(sql)
            db.commit()
        except sqlite3.IntegrityError:
            print()
            print("Error: This primary key has been referenced somewhere else!")

def UpdatingData(table_name,field_names,ID,fields):
    update_fields = []
    data = []
    finished = 'n'
    print()
    print("You are updating the {0} table".format(table_name))
    ID_Choice = input("Which ID would you like to change?: ")
    print("Which fields would you like to change?")
    print()
    print()
    print(field_names)
    print()
    
    while finished == 'n':
        field_choice = input("Enter field index values (press x to continue): ")
        update_fields.append(field_names[int(field_choice)])
        inputdata = input("Change field to: ")
        data.append(inputdata)
        print()
        finished = input("Do you want to finish? (y/n): ")
        print()
    update_fields = ','.join(update_fields)
    
    
    with sqlite3.connect("Volac.db") as db:
        try:
            cursor = db.cursor()
            sql = "update {0} set {1} where {2}={3}".format(table_name,update_fields,ID,ID_Choice)
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(sql,data)
            db.commit()
        except sqlite3.IntegrityError:
            print()
            print("Error: This primary key has been referenced somewhere else!")    
    
def StaffTable():
    table_name = "Staff"
    field_names = ["FirstName=?","Surname=?","JobTitle=?","DepartmentID=?","LocationID=?"]
    ID = "StaffID"
    
    fields = "Staff (FirstName, Surname, JobTitle,DepartmentID,LocationID)"
    values = "(?,?,?,?,?)"
    amount = 5

    EditMenu(table_name,field_names,ID,fields,values,amount)

def HardwareTable():
    table_name = "Hardware"
    field_names = ["Cost=?","Warranty=?","WarrantyExpirationDate=?","SerialNumber=?","IMEINumber=?","PhoneNumber=?","DeviceID=?","HardwareModelID=?"]
    ID = "HardwareID"
    
    fields = "Hardware (Cost, Warranty, WarrantyExpirationDate, SerialNumber, IMEINumber, PhoneNumber, DeviceID, HardwareModelID)"
    values = "(?,?,?,?,?,?,?,?)"
    amount = 8
    EditMenu(table_name,field_names,ID,fields,values,amount)
    
def HardwareMake():
    table_name = "HardwareMake"
    field_names = ["HardwareMakeName=?"]
    ID = "HardwareMakeID"
    
    fields = "HardwareMake (HardwareMakeName)"
    values = "(?)"
    amount = 1
    EditMenu(table_name,field_names,ID,fields,values,amount)

def HardwareModel():
    table_name = "HardwareModel"
    field_names = ["HardwareModelName=?","HardwareMakeID=?"]
    ID = "HardwareModelID"
    
    fields = "HardwareModel (HardwareModelName, HardwareMakeID)"
    values = "(?,?)"
    amount = 2
    EditMenu(table_name,field_names,ID,fields,values,amount)

def DeviceType():
    table_name = "DeviceType"
    field_names = ["DeviceName=?"]
    ID = "DeviceTypeID"
    
    fields = "DeviceType (DeviceName)"
    values = "(?)"
    amount = 1
    EditMenu(table_name,field_names,ID,fields,values,amount)

def StaffHardware():
    table_name = "StaffHardware"
    field_names = ["PurchaseDate=?","StaffID=?","HardwareID=?"]
    ID = "StaffHardwareID"
    
    fields = "StaffHardware (PurchaseDate, StaffID, HardwareID)"
    values = "(?,?,?)"
    amount = 3
    EditMenu(table_name,field_names,ID,fields,values,amount)

def Department():
    table_name = "Department"
    field_names = ["DepartmentName=?"]
    ID = "DepartmentID"
    
    fields = "Department (DepartmentName)"
    values = "(?)"
    amount = 1
    EditMenu(table_name,field_names,ID,fields,values,amount)

def Location():
    table_name = "Location"
    field_names = ["AddressLine1=?","AddressLine2=?","AddressLine3=?"]
    ID = "LocationID"
    
    fields = "Location (AddressLine1, AddressLine2, AddressLine3)"
    values = "(?,?,?)"
    amount = 3
    EditMenu(table_name,field_names,ID,fields,values,amount)

def DepartmentLocation():
    table_name = "DepartmentLocation"
    field_names = ["LocationID=?","DepartmentID=?"]
    ID = "DepartmentLocationID"
    
    fields = "DepartmentLocation (LocationID, DepartmentID)"
    values = "(?,?)"
    amount = 2
    EditMenu(table_name,field_names,ID,fields,values,amount) 
    
if __name__ == "__main__":
    Menu()
