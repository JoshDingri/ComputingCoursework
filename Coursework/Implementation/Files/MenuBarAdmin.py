from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class MenuBarAdmin(QMainWindow):
    """Menu bar for every window"""

    def __init__(self):
        super().__init__()
        self.MenuBar()

    def MenuBar(self):
        self.menu_bar = QMenuBar()
        
        self.AccountMenu = self.menu_bar.addMenu("Account")
        
        self.Logout = QAction("Log Out",self)
        self.ChangePassword = QAction("Change Password",self)        
        self.AccountMenu.addAction(self.Logout)
        self.AccountMenu.addAction(self.ChangePassword)
     
        self.DatabaseMenu = self.menu_bar.addMenu("Database")

        self.SelectDatabaseMenu = QMenu("Select Database",self)
        self.DatabaseMenu.addMenu(self.SelectDatabaseMenu)

        self.staffmenu = QMenu("Staff",self)
        self.SelectDatabaseMenu.addMenu(self.staffmenu)

        self.hardwaremenu = QMenu("Hardware",self)
        self.SelectDatabaseMenu.addMenu(self.hardwaremenu)

        self.locationmenu = QMenu("Location",self)
        self.SelectDatabaseMenu.addMenu(self.locationmenu)

        self.departmentmenu = QMenu("Department",self)
        self.SelectDatabaseMenu.addMenu(self.departmentmenu)

        self.ViewDatabase = QAction("View Database",self)
        self.EditDatabase = QAction("Edit Database",self)
        self.AddData = QAction("Add Data",self)
        self.RemoveData = QAction("Remove Data",self)

        self.staffmenu.addAction(self.ViewDatabase)
        self.hardwaremenu.addAction(self.ViewDatabase)
        self.locationmenu.addAction(self.ViewDatabase)
        self.departmentmenu.addAction(self.ViewDatabase)

        self.staffmenu.addAction(self.EditDatabase)
        self.hardwaremenu.addAction(self.EditDatabase)
        self.locationmenu.addAction(self.EditDatabase)
        self.departmentmenu.addAction(self.EditDatabase)

        self.staffmenu.addAction(self.AddData)
        self.hardwaremenu.addAction(self.AddData)
        self.locationmenu.addAction(self.AddData)
        self.departmentmenu.addAction(self.AddData)

        self.staffmenu.addAction(self.RemoveData)
        self.hardwaremenu.addAction(self.RemoveData)
        self.locationmenu.addAction(self.RemoveData)
        self.departmentmenu.addAction(self.RemoveData)

        self.setMenuBar(self.menu_bar)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = MenuBarAdmin()
    launcher.show()
    launcher.raise_()
    app.exec_()