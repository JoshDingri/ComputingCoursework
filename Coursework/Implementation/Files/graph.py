from pylab import *
import sqlite3
from collections import Counter
import matplotlib.backends.backend_tkagg

class Graph():
    """Hardware By Department Graph"""
    def __init__(self):
        
        self.Create_Graph()
        
    def Create_Graph(self):

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT StaffID FROM StaffHardware")
            db.commit()

        NumberOfHardware = [item[0] for item in cursor.fetchall()]
              #### How many hardware devices are owned by staff

        departmentids = []

        for count in range(len(NumberOfHardware)):
                
            with sqlite3.connect("Volac.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT DepartmentID FROM Staff WHERE StaffID =?",(NumberOfHardware[count],))
                db.commit()
            DepartmentIDs = [item[0] for item in cursor.fetchall()]
            DepartmentIDs = str(DepartmentIDs).replace("[","")
            DepartmentIDs = DepartmentIDs.replace("]","")
            
            departmentids.append(DepartmentIDs)



        departmentnames = []

        for count in range(len(departmentids)):

            with sqlite3.connect("Volac.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT DepartmentName FROM Department WHERE DepartmentID =?",(departmentids[count],))
                db.commit()
            departments = [item[0] for item in cursor.fetchall()]
            departments = str(departments).replace("[","")
            departments = departments.replace("]","")
            departments = departments.replace("'","")
            departmentnames.append(departments)  #### which departments own hardware and how many they own

        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT DepartmentName FROM Department")
            db.commit()
        Departments =  [item[0] for item in cursor.fetchall()]


        counter = Counter(departmentnames)
        print(counter)

        d = {} #creates dictionary

        for count in range(len(Departments)):
            d["{0}".format(Departments[count])]=counter[Departments[count]]

        values = []
        for count in range(len(Departments)):
            values.append(d[Departments[count]])

            
                

            
        figure(figsize=(15,8))
        pos = arange(len(Departments))+1
        barh(pos,(values),align = 'center',color='#b8ff5c')
        yticks(pos,(Departments))
        xlabel("Number of Hardware Devices Owned")
        ylabel("Departments")
        title("Graph Showing Number of Hardware Devices Owned by Each Department")
        grid(True)
        show()

if __name__ == "__main__":
    Graph()
