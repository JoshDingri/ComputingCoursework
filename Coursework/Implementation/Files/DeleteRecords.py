from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from OpenDatabaseWindow import *


class DeleteRecords(QWidget):
    """Class that will allows deletion of records in QTableWidget and Database"""

    def __init__(self):
        super().__init__()
        
