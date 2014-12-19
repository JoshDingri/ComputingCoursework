from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MenuBarAdmin import *

class OpenDatabase(QMainWindow):
    """Opening database to add, edit and remove"""

    def __init__(self):
        super().__init__()
        
        self.grid = QGridLayout()
        self.horizontal = QHBoxLayout()
        self.verticle = QVBoxLayout()
        
        
        DatabaseLbl = QLabel("Database")
        DatabaseLbl.setFont(QFont("Calibri",20))
        Database_CB = QComboBox()
        Database_CB.setFixedHeight(30)
        Database_CB.setFixedWidth(150)
        Items = ['Staff','Hardware','Department']
        Database_CB.addItems(Items)



        SearchLbl = QLabel("Search Fields")
        Search_LE = QLineEdit()
        Search_LE.setFixedWidth(150)
        Search_LE.setFixedHeight(25)
        SearchLbl.setFont(QFont("Calibri",20))

        self.Back_btn = QPushButton("Back")
        self.Back_btn.setFixedWidth(50)

        EditDatabase_btn = QPushButton("Edit Database")
        Add_btn = QPushButton("Add Data")
        Remove_btn = QPushButton("Remove Data")

        space = QLabel('')
        AddDatabase = QPushButton('Add Database')
        AddDatabase.setFont(QFont("Calibri",10))
        AddDatabase.setFixedWidth(80)
        AddDatabase.setFixedHeight(20)



        self.grid.addWidget(self.Back_btn,0,0)
        self.grid.addWidget(space,1,0)
        self.grid.addWidget(DatabaseLbl,1,1)
        self.grid.addWidget(Database_CB,1,2)
        self.grid.addWidget(AddDatabase,1,3)
        

        self.grid.addWidget(SearchLbl,2,1)
        self.grid.addWidget(Search_LE,2,2)

        self.grid.setVerticalSpacing(20)

        self.horizontal.addWidget(EditDatabase_btn)
        self.horizontal.addWidget(Add_btn)
        self.horizontal.addWidget(Remove_btn)

        self.verticle.addLayout(self.grid)
        self.verticle.addLayout(self.horizontal)
        self.setLayout(self.verticle)


        
        self.LayoutWidget = QWidget()

        self.LayoutWidget.setLayout(self.verticle)

        self.setCentralWidget(self.LayoutWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = OpenDatabase()
    launcher.show()
    launcher.raise_()
    launcher.resize(550,350)
    app.exec_()
