import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.

exe=Executable(
     script="LoginWindow.py",
     base="Win32Gui",
     icon="windowicon.ico"
     )

build_options = {'build_exe':
                    {'packages': ["os", "tkinter"]},
                'bdist_mac':
                    {'iconfile': "windowicon.ico",
                    },
                }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "guifoo",
        version = "0.1",
        description = "My GUI application!",
        options = build_options,
        executables = [exe])
