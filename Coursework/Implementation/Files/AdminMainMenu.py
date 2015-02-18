from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MenuBarAdmin import *
from graph import *
from AddingAccounts import *


class AdminMainMenu(QMainWindow):
    """The admin's main menu screen"""

    def __init__(self):
        super().__init__()

        self.horizontal_layout = QVBoxLayout()
        
        self.ButtonStyleSheet =  ("""QPushButton{
                    color: #333;
                    border: 2px solid #555;
                    border-radius: 11px;
                    padding: 5px;
                    background: qradialgradient(cx: 0.3, cy: -0.4,
                    fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #fff, stop: 1 #888);
                    min-width: 80px;
                    }"""
                             
                    """QPushButton:hover{
                    background: qradialgradient(cx: 0.3, cy: -0.4,
                    fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #fff, stop: 1 #bbb);
                    }"""

                    """QPushButton:pressed {
                    background: qradialgradient(cx: 0.4, cy: -0.1,
                    fx: 0.4, fy: -0.1,
                    radius: 1.35, stop: 0 #fff, stop: 1 #ddd);
                    }""")

        self.OpenDatabaseBtn = QPushButton("Open Database")
        self.OpenDatabaseBtn.setFont(QFont("Calibri",20))
        self.SearchStaffBtn = QPushButton("Search Staff")
        self.SearchStaffBtn.setFont(QFont("Calibri",20))
        
        self.OpenDatabaseBtn.setFixedHeight(100)
        self.SearchStaffBtn.setFixedHeight(100)
        self.SearchStaffBtn.setStyleSheet(self.ButtonStyleSheet)
        self.OpenDatabaseBtn.setStyleSheet(self.ButtonStyleSheet)

        self.horizontal_layout.addWidget(self.OpenDatabaseBtn)
        self.horizontal_layout.addWidget(self.SearchStaffBtn)



        
        window_widget = QWidget()
        window_widget.setLayout(self.horizontal_layout)
        self.setCentralWidget(window_widget)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = AdminMainMenu()
    launcher.show()
    launcher.raise_()
    app.exec_()
