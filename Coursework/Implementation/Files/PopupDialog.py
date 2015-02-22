from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class Presence_Dialog(QDialog):
    """Presence Check Dialog"""
    def __init__(self,text):
        super().__init__()
        self.resize(100,100)
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout2 = QHBoxLayout()
        self.horizontal_layout3 = QHBoxLayout()
        self.vertical = QVBoxLayout()
        
        Picture = QLabel()
        Pixmap = QPixmap('WarningPicture')
        Pixmap = Pixmap.scaled(250,150,Qt.KeepAspectRatio)
        Picture.setPixmap(Pixmap)
        self.horizontal_layout.addStretch(1)
        self.horizontal_layout.addWidget(Picture)
        self.horizontal_layout.addStretch(1)

        WarningText = QLabel(text)
        WarningText.setFont(QFont('Calibri',12))
        self.horizontal_layout2.addStretch(1)
        self.horizontal_layout2.addWidget(WarningText)
        self.horizontal_layout2.addStretch(1)

        self.OKbtn = QPushButton('OK')
        self.horizontal_layout3.addWidget(self.OKbtn)
        
        self.OKbtn.clicked.connect(self.CloseWindow)

        self.vertical.addLayout(self.horizontal_layout)
        self.vertical.addLayout(self.horizontal_layout2)
        self.vertical.addLayout(self.horizontal_layout3)

        self.setLayout(self.vertical)

    def CloseWindow(self):
        self.reject()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = Presence_Dialog()
    launcher.show()
    launcher.raise_()
    launcher.exec_()
    app.exec_()
