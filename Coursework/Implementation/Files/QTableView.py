from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtSql
from PyQt4.Qt import *
import sys
import sqlite3

class db(QTableView):
    def __init__(self):
        

        model = QtSql.QSqlTableModel(self, db)
        model.setTable("Volac")
        model.select()

        tableview = QtGui.QTableView()
        tableview.setModel(model)
        tableview.show()
