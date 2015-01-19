from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from OpenDatabaseWindow import *
import sqlite3
from MainProgram import *

class Warning_Dialog(QDialog):
    """Warning message for deleting data"""
    
    def __init__(self):
        super().__init__()
        self.resize(450,300)
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout2 = QHBoxLayout()
        self.horizontal_layout3 = QHBoxLayout()
        self.vertical = QVBoxLayout()
        
        Picture = QLabel()
        Pixmap = QPixmap('WarningPicture')
        Pixmap = Pixmap.scaled(300,200,Qt.KeepAspectRatio)
        Picture.setPixmap(Pixmap)
        self.horizontal_layout.addStretch(1)
        self.horizontal_layout.addWidget(Picture)
        self.horizontal_layout.addStretch(1)

        WarningText = QLabel('ARE YOU SURE YOU WANT TO DELETE ITEM(S)')
        WarningText.setFont(QFont('Calibri',12))
        self.horizontal_layout2.addStretch(1)
        self.horizontal_layout2.addWidget(WarningText)
        self.horizontal_layout2.addStretch(1)

        self.YesBtn = QPushButton('Yes')
        self.NoBtn = QPushButton('No')
        self.horizontal_layout3.addWidget(self.YesBtn)
        self.horizontal_layout3.addWidget(self.NoBtn)


        self.vertical.addLayout(self.horizontal_layout)
        self.vertical.addLayout(self.horizontal_layout2)
        self.vertical.addLayout(self.horizontal_layout3)
        

        
        self.setLayout(self.vertical)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = Warning_Dialog()
    launcher.show()
    launcher.raise_()
    launcher.exec_()
    app.exec_()


    
    
    
