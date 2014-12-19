from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MenuBarAdmin import *


class AdminMainMenu(QWidget):
    """The admin's main menu screen"""

    def __init__(self):
        super().__init__()

        self.horizontal_layout = QHBoxLayout()

        self.OpenDatabaseBtn = QPushButton("Open Database")
        self.SearchStaffBtn = QPushButton("Search for Staff")

        self.horizontal_layout.addWidget(self.OpenDatabaseBtn)
        self.horizontal_layout.addWidget(self.SearchStaffBtn)


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = AdminMainMenu()
    launcher.show()
    launcher.raise_()
    app.exec_()
