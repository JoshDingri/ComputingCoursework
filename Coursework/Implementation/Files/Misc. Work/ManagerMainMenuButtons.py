from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class ManagerMainMenu_Buttons(QWidget):
    """Manager Main Menu Buttons"""

    def __init__(self):
        super().__init__()
    
        self.horizontalMMM = QHBoxLayout()
        self.department_btn = QPushButton("View Department")
        self.myinfo_btn = QPushButton("View My Information")

        self.horizontalMMM.addWidget(self.department_btn)
        self.horizontalMMM.addWidget(self.myinfo_btn)

        self.buttons = QWidget()

        self.buttons.setLayout(self.horizontalMMM)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = ManagerMainMenu_Buttons()
    launcher.show()
    launcher.raise_()
    app.exec_()
