from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import sqlite3

class AddDataWindow(QWidget):
    """The new window for entering data"""

    def __init__(self):
        super().__init__()
        self.AddWindow()


    def AddWindow(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        with sqlite3.connect("Volac.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * from Staff")
            db.commit()
        col = [tuple[0] for tuple in cursor.description]
        print(col)

        positions = [(i,j) for i in range (int(round(len(col)/2,1))) for j in range(4)]

        col = sum([[i,''] for i in col],[])

                
            
        
        for position, name in zip(positions,col):
            if name == '':
                LE = QLineEdit()
                self.grid.addWidget(LE,*position)
            label = QLabel(name)
            self.grid.addWidget(label,*position)

            

       
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = AddDataWindow()
    launcher.show()
    launcher.raise_()
    app.exec_()
