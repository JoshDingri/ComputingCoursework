import sqlite3

def create_table(db_name,table_name,sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("Select name from sqlite_master where name=?",(table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            response = input("The table {0} already exists, do you wish to recreate it (y/n): ".format(table_name))
            if response == 'y':
                keep_table = False
                print("The {0} table will be created - all existing data will be lost".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                print("The existing table was kept")
        else:
            keep_table = False
            
        if keep_table == False:             
            cursor.execute(sql)
            db.commit()

def StaffTable():
    sql = """create table Staff
          (StaffID integer,
          FirstName text,
          Surname text,
          JobTitle text,
          primary key(StaffID),
          foreign key(DepartmentID) references Department(DepartmentID),
          foreign key(LocationID) references Location(LocationID)
                      
          
          """
    create_table(db_name,"Staff",sql)

def HardwareTable():
    sql = """create table Hardware
          (HardwareID integer,
          Cost real,
          Warranty boolean,
          WarrantyExpirationDate date,
          SerialNumber text,
          IMEINumber text,
          PhoneNumber text,
          primary key(HardwareID))"""
    create_table(db_name,"Hardware",sql)

def HardwareMake():
    sql = """create table HardwareMake
          (HardwareMakeID integer,
          HardwareMakeName text
          primary key(HardwareMakeID))"""
    create_table(db_name,"HardwareMake",sql)

def HardwareModel():
    sql = """create table HardwareModel
          (HardwareModelID integer,
          HardwareModelName text
          primary key(HardwareModelID))"""
    create_table(db_name,"HardwareModel",sql)

def DeviceType():
    sql = """create table DeviceType
          (DeviceID integer,
          DeviceName text
          primary key(DeviceID))"""
    create_table(db_name,"DeviceType",sql)

def StaffHardware():
    sql = """create table StaffHardware
          (StaffHardwareID integer,
          PurchaseDate date
          primary key(StaffHardwareID))"""
    create_table(db_name,"StaffHardware",sql)

def Department():
    sql = """create table Department
          (DepartmentID integer,
          DepartmentName text
          primary key(DepartmentID))"""
    create_table(db_name,"Department",sql)

def Location():
    sql = """create table Location
          (LocationID integer,
          AddressLine1 text
          AddressLine2 text
          AddressLine3 text
          primary key(LocationID))"""
    create_table(db_name,"Location",sql)

def DepartmentLocation():
    sql = """create table DepartmentLocation
          (DepartmentLocationID integer,
          primary key(DepartmentLocationID))"""
    create_table(db_name,"DepartmentLocation",sql)



if __name__ == "__main__":
    db_name = "Volac.db"
