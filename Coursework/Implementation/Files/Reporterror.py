from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import smtplib

class ReportBug(QMainWindow):
    """A Email GUI to send bug reports"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Report Incorrect Information")
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

        self.Description = QLabel("Description of data error:") 
        self.Description_LE = QTextEdit()
        self.Description_LE.setFixedHeight(150)

        self.grid_layout.addWidget(self.Description,3,0)
        self.grid_layout.addWidget(self.Description_LE,3,1)

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

        self.setStyleSheet("QLabel{font-size: 12px} QPushButton{font-size: 12px;")

        self.submit_btn.clicked.connect(self.SendMail)

    def SendMail(self):
        self.mail = smtplib.SMTP("smtp.live.com",25)                                                                                                                                                                                                                                                                                            
        
        self.mail.ehlo()
        self.mail.starttls()

        IT_Staff_Email = ('josh-dingri@hotmail.co.uk')
        Description = str(self.Description_LE.toPlainText())
        Email = ('donotreply_volac@hotmail.co.uk')

        
        Forename = str(self.Forename_LE.displayText())
        Surname_LE = str(self.Surname_LE.displayText())
        User_Email = str(self.Email_LE.displayText())

        try:
            self.mail.login('donotreply_volac@hotmail.co.uk','toffee2015')
        except smtplib.SMTPServerDisconnected:
            print("not valid")

        Content = ("Email: {0} \nForename: {1}\nSurname: {2}\nDescription: {3}".format(User_Email,Forename,Surname_LE,Description))
        Subject = ("Incorrect Information Report")

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
