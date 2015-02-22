from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PopupDialog import *
import sys
import smtplib

class ForgottenAccount(QDialog):
    """A Email GUI to recover account information"""
    def __init__(self):
        super().__init__()
        self.resize(500,250)
        self.setWindowTitle("Account Recovery")
        self.WindowLayout()

    def WindowLayout(self):
        self.grid_layout = QGridLayout()
        
        self.Email_lbl = QLabel("Email:")
        self.Email_LE = QLineEdit()
        EmailRegExp = QRegExp("[^@]+@[^@]+\.[^@]+") 
        self.Email_LE.setValidator(QRegExpValidator(EmailRegExp))

        self.grid_layout.addWidget(self.Email_lbl,0,0)
        self.grid_layout.addWidget(self.Email_LE,0,1)

        self.Forename_lbl = QLabel("Forename:")
        self.Forename_LE = QLineEdit()

        self.grid_layout.addWidget(self.Forename_lbl,1,0)
        self.grid_layout.addWidget(self.Forename_LE,1,1)

        self.Surname_lbl = QLabel("Surname:")
        self.Surname_LE = QLineEdit()

        self.grid_layout.addWidget(self.Surname_lbl,2,0)
        self.grid_layout.addWidget(self.Surname_LE,2,1)

        self.cancel_btn = QPushButton("Cancel")
        self.submit_btn = QPushButton("Submit")

        self.horizontal_layout = QHBoxLayout()

        self.horizontal_layout.addWidget(self.cancel_btn)
        self.horizontal_layout.addWidget(self.submit_btn)

        self.vertical_overall_layout = QVBoxLayout()

        self.vertical_overall_layout.addLayout(self.grid_layout)
        self.vertical_overall_layout.addLayout(self.horizontal_layout)

        self.setLayout(self.vertical_overall_layout)

        self.submit_btn.clicked.connect(self.SendMail)
        self.cancel_btn.clicked.connect(self.CloseWindow)

    def CloseWindow(self):
        self.reject()

    def SendMail(self):
        BlankFieldsWarning = Presence_Dialog("PLEASE MAKE SURE ALL FIELDS ARE FILLED OUT") 
        self.mail = smtplib.SMTP("smtp.live.com",25)
        self.mail.ehlo()
        self.mail.starttls()

        IT_Staff_Email = ('josh-dingri@hotmail.co.uk')
        Email = ('donotreply_volac@hotmail.co.uk')

        Forename = str(self.Forename_LE.displayText())
        Surname_LE = str(self.Surname_LE.displayText())
        Email_LE = str(self.Email_LE.displayText())

        if Email_LE == '' or Forename == '' or Surname_LE == '':
            BlankFieldsWarning.exec_()
        else:

            try:
                self.mail.login('donotreply_volac@hotmail.co.uk','toffee2015')
            except smtplib.SMTPServerDisconnected:
                print("not valid")

            Content = ("\nForename: {0}\nSurname: {1}\nEmail: {2}".format(Forename,Surname_LE,Email_LE))
            Subject = ("Account Recovery Request")

            Body = ("Subject: {0}\n\n{1}".format(Subject,Content))

            self.mail.sendmail(Email,IT_Staff_Email,Body)
            self.mail.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = ForgottenAccount()
    launcher.show()
    launcher.raise_()
    app.exec_()





        
