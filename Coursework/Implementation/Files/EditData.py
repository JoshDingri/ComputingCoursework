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
    
def InsertData(fields,values,amount):
    data = []
    for count in range (amount):
        input_data = input()
        data.append(input_data)
    with sqlite3.connect("Volac.db") as db:
        cursor = db.cursor()
        sql = "insert into {0} values {1}".format(fields,values)
        cursor.execute(sql,data)
        db.commit()


def StaffTable():
    fields = "Staff (FirstName, Surname, JobTitle,DepartmentID,LocationID)"
    values = "(?,?,?,?,?)"
    amount = 5
    InsertData(fields,values,amount)

def HardwareTable():
    fields = "Hardware (Cost, Warranty, WarrantyExpirationDate, SerialNumber, IMEINumber, PhoneNumber, DeviceID, HardwareModelID)"
    values = "(?,?,?,?,?,?,?,?)"
    amount = 8
    InsertData(fields,values,amount)
    
def HardwareMake():
    fields = "HardwareMake (HardwareMakeName)"
    values = "(?)"
    amount = 1
    InsertData(fields,values,amount)

def HardwareModel():
    fields = "HardwareModel (HardwareModelName, HardwareMakeID)"
    values = "(?,?)"
    amount = 2
    InsertData(fields,values,amount)

def DeviceType():
    fields = "DeviceType (DeviceName)"
    values = "(?)"
    amount = 1
    InsertData(fields,values,amount)

def StaffHardware():
    fields = "StaffHardware (PurchaseDate, StaffID, HardwareID)"
    values = "(?,?,?)"
    amount = 3
    InsertData(fields,values,amount)

def Department():
    fields = "Department (DepartmentName)"
    values = "(?)"
    amount = 1
    InsertData(fields,values,amount)

def Location():
    fields = "Location (AddressLine1, AddressLine2, AddressLine3)"
    values = "(?,?,?)"
    amount = 3
    InsertData(fields,values,amount)

def DepartmentLocation():
    print("heloo")
    fields = "DepartmentLocation (LocationID, DepartmentID)"
    values = "(?,?)"
    amount = 2
    InsertData(fields,values,amount)  
    
if __name__ == "__main__":
    Menu()
