from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MenuBarAdmin import *

class OpenDatabase(QMainWindow):
    """Opening database to add, edit and remove"""

    def __init__(self):
        super().__init__()
        self.MenuBar()
        self.MainLayout()

    def MenuBar(self):
        MenuBarAdmin.MenuBar(self)

    def MainLayout(self):
        
        self.grid = QGridLayout()
        self.verticle = QVBoxLayout()
        self.verticle2 = QVBoxLayout()
        
        
        DatabaseLbl = QLabel("Database")
        DatabaseLbl.setFont(QFont("Calibri",15))
        Database_CB = QComboBox()
        Database_CB.setFixedWidth(150)

        SearchLbl = QLabel("Search Fields")
        Search_LE = QLineEdit()
        Search_LE.setFixedWidth(150)
        SearchLbl.setFont(QFont("Calibri",15))

        EditDatabase_btn = QPushButton("Edit Database")
        Add_btn = QPushButton("Add Data")
        Remove_btn = QPushButton("Remove Data")

        self.setLayout(self.grid)

        self.horizontal.addStretch(1)
        self.horizontal.addWidget(DatabaseLbl)
        self.horizontal.addStretch(1)
        self.horizontal.addWidget(Database_CB)
        self.horizontal.addStretch(1)

        self.horizontal2.addStretch(1)
        self.horizontal2.addWidget(SearchLbl)
        self.horizontal2.addStretch(1)
        self.horizontal2.addWidget(Search_LE)
        self.horizontal2.addStretch(1)
        
        self.horizontal3.addWidget(EditDatabase_btn)
        self.horizontal3.addWidget(Add_btn)
        self.horizontal3.addWidget(Remove_btn)

        self.verticle.addLayout(self.horizontal)
        self.verticle.addLayout(self.horizontal2)
        self.verticle.addLayout(self.horizontal3)

        self.LayoutWidget = QWidget()

        self.LayoutWidget.setLayout(self.verticle)

        self.setCentralWidget(self.LayoutWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = OpenDatabase()
    launcher.show()
    launcher.raise_()
    app.exec_()
