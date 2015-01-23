from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class ReportBug(QMainWindow):
    """A Email GUI to send bug reports"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Send Bug Report")
        self.WindowLayout()

    def WindowLayout(self):
        self.grid_layout = QGridLayout()

        self.Email_lbl = QLabel("Email Address:")
        self.Email_LE = QLineEdit()

        self.grid_layout.addWidget(self.Email_lbl,0,0)
        self.grid_layout.addWidget(self.Email_LE,0,1)

        self.Forename_lbl = QLabel("Forename:")
        self.Forename_LE = QLineEdit()

        self.grid_layout.addWidget(self.Forename_lbl,1,0)
        self.grid_layout.addWidget(self.Forename_LE,1,1)

        self.Surname_lbl = QLabel("Surame:")
        self.Surname_LE = QLineEdit()

        self.grid_layout.addWidget(self.Surname_lbl,2,0)
        self.grid_layout.addWidget(self.Surname_LE,2,1)

        self.JobTitle_lbl = QLabel("Job Title:")
        self.JobTitle_LE = QLineEdit()

        self.grid_layout.addWidget(self.JobTitle_lbl,3,0)
        self.grid_layout.addWidget(self.JobTitle_LE,3,1)

        self.Date_lbl = QLabel("Date:")
        self.Data_LE = QLineEdit()

        self.grid_layout.addWidget(self.Date_lbl,4,0)
        self.grid_layout.addWidget(self.Data_LE,4,1)

        self.Bug_Details_lbl = QLabel("Details of Bug:\n \nPlease say where\nit happened,on which\ninterface and what you\nintended to do before it\nhappened.") 
        self.Bug_Details_LE = QTextEdit()
        self.Bug_Details_LE.setFixedHeight(150)

        self.grid_layout.addWidget(self.Bug_Details_lbl,5,0)
        self.grid_layout.addWidget(self.Bug_Details_LE,5,1)

        self.cancel_btn = QPushButton("Cancel")
        self.submit_btn = QPushButton("Submit")

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.cancel_btn)
        self.horizontal_layout.addWidget(self.submit_btn)

        self.vertical_overall_layout = QVBoxLayout()

        self.vertical_overall_layout.addLayout(self.grid_layout)
        self.vertical_overall_layout.addLayout(self.horizontal_layout)

        window_widget = QWidget()
        window_widget.setLayout(self.vertical_overall_layout)
        self.setCentralWidget(window_widget)

    def SendMail(self):
        self.mail = smtplib.SMTP("smtp.live.com",25)
        self.mail.ehlo()
        self.mail.starttls()
        self.mail.login("josh-dingri@hotmail.co.uk","")

        Email = str(self.Email_LE.displayText())
        Forename = str(self.Forename_LE.displayText())
        Surname_LE = str(self.Surname_LE.displayText())
        JobTitle_LE = str(self.JobTitle_LE.displayText())
        Data_LE = str(self.Data_LE.displayText())
        Bug_Details_LE = str(self.Bug_Details_LE.displayText())

        self.mail.sendmail(Email,Forename,Surname_LE,JobTitle_LE,Data_LE,Bug_Details_LE)
        self.mail.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = ReportBug()
    launcher.show()
    launcher.raise_()
    app.exec_()
