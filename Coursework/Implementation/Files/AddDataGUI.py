from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from MainProgram import *

class AddDataWindow(QDialog):
    """The new window for entering data"""

    def __init__(self,CurrentCBValue):  ##CurrentCBValue is the table selected from dropdown box. Passed in from main program
            self.linelist = []
            
            super().__init__()
        
            self.grid = QGridLayout()
            self.verticle = QVBoxLayout()
            self.horizontal = QHBoxLayout()

                
            with sqlite3.connect("Volac.db") as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM {}".format(CurrentCBValue))
                    db.commit()
            self.col = [tuple[0] for tuple in cursor.description]   ##Gets the column names and adds the to a tuple

            positions = [(i,j) for i in range (int(round(len(self.col)/2,1))) for j in range(4)]     ##works out how many rows down and how many rows accross the grid needs 
            self.col = sum([[i,''] for i in self.col],[])   ## adds a space in between each item in self.col tuple

            ##The code below will work out where the different labels and line edits need to go
                    
            count = 0    
            for position, name in zip(positions,self.col):
                if name == '':   ##This replaces all the spaces with line edits
                    self.LE = QLineEdit() 
                    self.linelist.append(self.LE)   ##line edits are added to a list so they can be seperated and chosen individually if needed later
                    self.grid.addWidget(self.linelist[count],*position)
                    count+=1
                else:
                    label = QLabel(name)
                    self.grid.addWidget(label,*position)
            self.linelist[0].setText('Autonumber')   ##The first label/line edit will always be a ID, since IDs are autoupdated the line edit has default text
            self.linelist[0].setReadOnly(True)   ## Line edit is read only

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
                

    def Commit_Changes(self):
        data = []
        values = []
        for count in range(len(self.linelist)):
            data.append(self.linelist[count].text())
            if 'Autonumber' in data:
                data.remove('Autonumber')   ## Removes the autonumber field from the list.
                
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
    
            


            

       
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = AddDataWindow(None)
    launcher.show()
    launcher.raise_()
    app.exec_()
