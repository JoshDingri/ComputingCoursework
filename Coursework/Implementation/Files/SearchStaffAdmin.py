from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class SearchStaff(QMainWindow):
    """Admin search staff window"""

    def __init__(self):
        super().__init__()

        self.grid = QGridLayout()
        self.verticle = QVBoxLayout()
                
        DatabaseLbl = QLabel("Department")
        DatabaseLbl.setFont(QFont("Calibri",20))
        Database_CB = QComboBox()
        Database_CB.setFixedHeight(30)
        Database_CB.setFixedWidth(150)
        Items = ['Financing','Marketing']
        Database_CB.addItems(Items)
        

        SearchLbl = QLabel("Name")
        Search_LE = QLineEdit()
        Search_LE.setFixedWidth(150)
        Search_LE.setFixedHeight(25)
        SearchLbl.setFont(QFont("Calibri",20))

        self.Back_btn = QPushButton("Back")
        self.Back_btn.setFixedWidth(50)


        space = QLabel('')
        
        self.grid.addWidget(self.Back_btn,0,0)
        self.grid.addWidget(space,1,0)
        self.grid.addWidget(DatabaseLbl,1,1)
        self.grid.addWidget(Database_CB,1,2)
        self.grid.addWidget(space,1,3)

        self.grid.addWidget(SearchLbl,2,1)
        self.grid.addWidget(Search_LE,2,2)

        self.grid.setVerticalSpacing(20)

        self.verticle.addLayout(self.grid)
        self.setLayout(self.verticle)


        
        self.LayoutWidget = QWidget()

        self.LayoutWidget.setLayout(self.verticle)

        self.setCentralWidget(self.LayoutWidget)
