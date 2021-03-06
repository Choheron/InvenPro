from datetime import datetime
import os, sys
import tkinter as tk
import tkinter.messagebox
from driverBin.utils import settings as GLOBAL
from driverBin.MenuBar import MainMenuBar
from driverBin.LaunchPage import StartPage
from driverBin.CPUMenu import CPUMenu
from driverBin.SoftwareMenu import SoftwareMenu
from driverBin.OfficeMenu import OfficeMenu
from driverBin.FieldMenu import FieldMenu

class InvenPro(tk.Tk):
    def __init__(self):
        # Initalize the global module
        GLOBAL.init(self)
        # Decleare self as root Tk process
        tk.Tk.__init__(self, className = ' MASLD-InvenPro')

        # Set Icon for Window
        self.iconbitmap(os.getcwd() + '/driverBin/images/icons/DesktopIcon 32x32.ico')

        # Declare the master control frame for pages
        self.container = tk.Frame(self) 
        self.container.pack(side = "top", fill = "both", expand = True)

        # Configure the master control frame
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        # Declare a dictionary of pages for the program to control
        self.pageDict = {}

        # Declare Frames and make their master the controlFrame
        self.startPage = StartPage(parent = self.container, root = self, pageDict = self.pageDict)
        self.pageDict['home'] = self.startPage
        self.cpuPage = CPUMenu(parent = self.container, root = self, pageDict = self.pageDict)
        self.pageDict['cpuMenu'] = self.cpuPage
        self.softwarePage = SoftwareMenu(parent = self.container, root = self, pageDict = self.pageDict)
        self.pageDict['softwareMenu'] = self.softwarePage
        self.officePage = OfficeMenu(parent = self.container, root = self, pageDict = self.pageDict)
        self.pageDict['officeMenu'] = self.officePage
        self.fieldPage = FieldMenu(parent = self.container, root = self, pageDict = self.pageDict)
        self.pageDict['fieldMenu'] = self.fieldPage

        # Grid Frames into control frame
        self.cpuPage.grid(row = 0, column = 0, sticky="NESW")
        self.startPage.grid(row = 0, column = 0, sticky="NESW")
        self.softwarePage.grid(row = 0, column = 0, sticky = "NESW")
        self.officePage.grid(row = 0, column = 0, sticky = "NESW")
        self.fieldPage.grid(row = 0, column = 0, sticky = "NESW")

        # Delcare and configure menu bar
        menuBar = MainMenuBar(self, self.container, self.pageDict)
        self.config(menu = menuBar)

        # Intercept close button and rebind it to a confirmation
        self.protocol("WM_DELETE_WINDOW", lambda x=None: self.terminate())
        # Bind universal help button
        self.bind('<F1>', lambda x=None: menuBar.helpIndex())
        # Bind "Home" key to raise homepage
        self.bind('<Home>', lambda x=None: menuBar.raiseHomepage())
        # Bind "Shift + F1" to raise PC page
        self.bind('<Shift-F1>', lambda x=None: menuBar.raisePCPage())
        # Bind "Shift + F2" to raise Software page
        self.bind('<Shift-F2>', lambda x=None: menuBar.raiseSoftwarePage())
        # Bind "Shift + F3" to raise Office page
        self.bind('<Shift-F3>', lambda x=None: menuBar.raiseOfficePage())
        # Bind "Shift + F4" to raise PC page
        self.bind('<Shift-F4>', lambda x=None: menuBar.raiseFieldPage())

        # Disable resizing
        self.resizable(0, 0)      

    # ==============================
    #    TERMINATION METHODS BELOW
    # ==============================

    def terminate(self):
        response = tk.messagebox.askyesno(title = "Are you sure?", message = "You are about to close the program!\nAll unsaved data/changes will be lost.\nAre you sure?")
        if(response):
            sys.exit()
        else:
            return

program = InvenPro()
program.mainloop()