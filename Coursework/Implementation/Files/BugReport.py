from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Calender import *
import sys
import smtplib

class ReportBug(QDialog):
    """A Email GUI to send bug reports"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Send Bug Report")
        self.WindowLayout()

    def WindowLayout(self):
        self.grid_layout = QGridLayout()

##        self.Email_lbl = QLabel("Email Address:")
##        self.Email_LE = QLineEdit()
##
##        self.Password_lbl = QLabel("Email Password:")
##        self.Password_LE = QLineEdit()
##        self.Password_LE.setEchoMode(QLineEdit.Password)
##        
##        self.grid_layout.addWidget(self.Email_lbl,0,0)
##        self.grid_layout.addWidget(self.Email_LE,0,1)
##
##        self.grid_layout.addWidget(self.Password_lbl,1,0)
##        self.grid_layout.addWidget(self.Password_LE,1,1)
        

        self.Forename_lbl = QLabel("Forename:")
        self.Forename_LE = QLineEdit()

        self.grid_layout.addWidget(self.Forename_lbl,2,0)
        self.grid_layout.addWidget(self.Forename_LE,2,1)

        self.Surname_lbl = QLabel("Surame:")
        self.Surname_LE = QLineEdit()

        self.grid_layout.addWidget(self.Surname_lbl,3,0)
        self.grid_layout.addWidget(self.Surname_LE,3,1)

        self.JobTitle_lbl = QLabel("Job Title:")
        self.JobTitle_LE = QLineEdit()

        self.grid_layout.addWidget(self.JobTitle_lbl,4,0)
        self.grid_layout.addWidget(self.JobTitle_LE,4,1)

        self.calander_btn = QPushButton()
        self.calander_btn.setFixedWidth(50)
        pixmap = QPixmap('calendar-icon.png')
        ButtonIcon = QIcon(pixmap)
        self.calander_btn.setIcon(ButtonIcon)
        self.calander_btn.setIconSize(QSize(13,13))
        self.calander_btn.clicked.connect(self.OpenCalander)

        self.Date_lbl = QLabel("Date:")
        self.Data_LE = QLineEdit()

        self.grid_layout.addWidget(self.Date_lbl,5,0)
        self.grid_layout.addWidget(self.Data_LE,5,1)
        self.grid_layout.addWidget(self.calander_btn,5,1)

        self.Bug_Details_lbl = QLabel("Details of Bug:\n \nPlease say where\nit happened,on which\ninterface and what you\nintended to do before it\nhappened.") 
        self.Bug_Details_LE = QTextEdit()
        self.Bug_Details_LE.setFixedHeight(150)

        self.grid_layout.addWidget(self.Bug_Details_lbl,6,0)
        self.grid_layout.addWidget(self.Bug_Details_LE,6,1)

        self.cancel_btn = QPushButton("Cancel")
        self.submit_btn = QPushButton("Submit")

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.cancel_btn)
        self.horizontal_layout.addWidget(self.submit_btn)

        self.vertical_overall_layout = QVBoxLayout()

        self.vertical_overall_layout.addLayout(self.grid_layout)
        self.vertical_overall_layout.addLayout(self.horizontal_layout)

        self.setLayout(self.vertical_overall_layout)

        self.setStyleSheet("QLabel{font-size: 12px} QPushButton{font-size: 12px;")

        self.submit_btn.clicked.connect(self.SendMail)
        
    def OpenCalander(self):
        CalenderWidget = Calendar()
        CalenderWidget.exec_()
        self.Data_LE.setText(CalenderWidget.date)
        self.Data_LE.setAlignment(Qt.AlignCenter)

    def SendMail(self):
        self.mail = smtplib.SMTP("smtp.live.com",25)
        self.mail.ehlo()
        self.mail.starttls()

        IT_Staff_Email = ('josh-dingri@hotmail.co.uk')
        Bug_Details_LE = str(self.Bug_Details_LE.toPlainText())
        Email = ('donotreply_volac@hotmail.co.uk')

        
        Forename = str(self.Forename_LE.displayText())
        Surname_LE = str(self.Surname_LE.displayText())
        JobTitle_LE = str(self.JobTitle_LE.displayText())
        Data_LE = str(self.Data_LE.displayText())
        print(Data_LE)

        try:
            self.mail.login('donotreply_volac@hotmail.co.uk','toffee2015')
        except smtplib.SMTPServerDisconnected:
            print("not valid")

        Content = ("\nForename: {0}\nSurname: {1}\nJobTitle: {2}\nDate: {3}\nBug Details: {4}".format(Forename,Surname_LE,JobTitle_LE,Data_LE,Bug_Details_LE))
        Subject = ("Bug Report")

        Body = ("Subject: {0}\n\n{1}".format(Subject,Content))
        print(Body)

        
                            

    
        self.mail.sendmail(Email,IT_Staff_Email,Body)
        self.mail.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = ReportBug()
    launcher.show()
    launcher.raise_()
    app.exec_()
