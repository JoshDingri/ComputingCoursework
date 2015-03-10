import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.

exe=Executable(
     script="LoginWindow.py",
     base="Win32Gui",
     icon="windowicon.ico",
     targetName="Volac Hardware Database.exe"
     )

includefiles = ["search.png","calendar-icon.png","arrow.png","WarningPicture.gif","chart_bar.png","Splashscreen.png","accounticon.png","windowicon.png","Accounts.db","warningimage.jpg","volaclogo.jpg","Volac.db",]

build_options = {'build_exe':
                    {'packages': ["os", "tkinter"],
                     'include_files':includefiles},
                'bdist_mac':
                    {'iconfile': "windowicon.ico",
                    },
                'bdist_msi':
                 {'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
                'add_to_path': False}
                }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Volac Int. Hardware Database",
        version = "0.1",
        description = "My GUI application!",
        options = build_options,
        executables = [exe])
