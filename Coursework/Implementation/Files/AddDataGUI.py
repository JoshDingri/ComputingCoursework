from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3
from MainProgram import *

class AddDataWindow(QDialog):
    """The new window for entering data"""

    def __init__(self,text):
            self.linelist = []
            super().__init__()
            print(text)
        
            self.grid = QGridLayout()
            self.setLayout(self.grid)

                
            with sqlite3.connect("Volac.db") as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM {}".format('Hardware')) #change to text
                    db.commit()
            col = [tuple[0] for tuple in cursor.description]
            print(col)

            positions = [(i,j) for i in range (int(round(len(col)/2,1))) for j in range(4)]
            col = sum([[i,''] for i in col],[])

            col_num = (int(round(len(col)/4,1)+1))
            print(col_num)
                    
            count = 0    
            for position, name in zip(positions,col):
                if name == '':
                    self.LE = QLineEdit()
                    self.linelist.append(self.LE)
                    self.grid.addWidget(self.linelist[count],*position)
                    count+=1
                label = QLabel(name)
                self.grid.addWidget(label,*position)

            self.AddData_Choice = QPushButton("Add Data")
            self.Cancel_Choice = QPushButton("Cancel")
            
            self.grid.addWidget(self.AddData_Choice,col_num,2)
            self.grid.addWidget(self.Cancel_Choice,col_num,1)

            self.AddData_Choice.clicked.connect(self.Commit_Changes)
                

    def Commit_Changes(self):
        print(self.linelist[1].text())
            


            

       
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = AddDataWindow(None)
    launcher.show()
    launcher.raise_()
    app.exec_()
