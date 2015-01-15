from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class Calendar(QDialog):

    def __init__(self):
        super().__init__()
        self.clicked = False
        self.initUI()

    def initUI(self):
        horizontal = QHBoxLayout()
        verticle = QVBoxLayout()
        
        
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        verticle.addWidget(self.cal)
        self.cal.clicked[QDate].connect(self.showDate)

        self.lbl = QLabel(self)
        horizontal.addStretch(1)
        horizontal.addWidget(self.lbl)
        horizontal.addStretch(1)
        date = self.cal.selectedDate()
        self.lbl.setText(date.toString())
        

        self.setGeometry(300,300,350,300)
        self.setWindowTitle("Calender")

        verticle.addLayout(horizontal)

        self.setLayout(verticle)
    

    def showDate(self, date):
        self.clicked = True
        self.lbl.setText(date.toString())
        self.date = date.toString("dd-MM-yy")
        self.reject()

def main():
    app = QApplication(sys.argv)
    launcher = Calendar()
    launcher.show()
    launcher.raise_()
    app.exec_()

if __name__ == "__main__":
    main()
