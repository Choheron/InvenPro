import sys
import tkinter as tk
import tkinter.messagebox
from .toplevels.AboutWin import AboutPopup
import os

class MainMenuBar(tk.Menu):

    def __init__(self, parent, controllerFrame: tk.Frame, pageDict):
        super().__init__(parent)
        self.master = parent
        self.controlFrame = controllerFrame
        self.pageDict = pageDict

        self.controlFrame.tkraise(self.pageDict['home'])
        self.buildMenu()
        self.pageDict['home'].lift()

    # ==============================
    # BUILD MENU METHOD BELOW
    # ==============================
    def buildMenu(self):
        # Delcare file menu and add commands
        fileMenu = tk.Menu(self, tearoff = 0)
        # Declare "New" submenu
        newMenu = tk.Menu(self, tearoff = 0)
        newMenu.add_command(label = "PC", command = lambda x=None: self.newPC())
        newMenu.add_command(label = "Software", command = lambda x=None: self.newSoftware())
        newMenu.add_command(label = "Office Category", command = lambda x=None: self.newOfficeCat())
        newMenu.add_command(label = "Field Category", command = lambda x=None: self.newFieldCat())
        # Add "New" submenu
        fileMenu.add_cascade(label = "New...", menu = newMenu)
        fileMenu.add_separator()
        fileMenu.add_command(label = "EXIT", command = lambda: self.systemTerminate())
        self.add_cascade(label = "File", menu = fileMenu)

        # Declare window menu option and add commands
        windowMenu = tk.Menu(self, tearoff = 0)
        windowMenu.add_command(label = "PC", command = lambda: self.raisePCPage())
        windowMenu.add_command(label = "Software", command = lambda: self.raiseSoftwarePage())
        windowMenu.add_command(label = "Office", command = lambda: self.raiseOfficePage())
        windowMenu.add_command(label = "Field", command = lambda: self.raiseFieldPage())
        windowMenu.add_separator()
        windowMenu.add_command(label = "Homepage", command = lambda: self.raiseHomepage())
        self.add_cascade(label = "Windows", menu = windowMenu)

        # Declare help menu option and add commands
        helpMenu = tk.Menu(self, tearoff = 0)
        helpMenu.add_command(label = "Help Index...", command = lambda: self.helpIndex())
        # Declare icon for about page
        self.aboutIcon = tk.PhotoImage(file = (os.getcwd() + '/driverBin/images/icons/info-16px.png'))
        helpMenu.add_command(label = "About", image = self.aboutIcon, compound = 'left',command = lambda: self.aboutPage())
        self.add_cascade(label = "Help", menu = helpMenu)

    # ==============================
    # SYSTEMLEVEL TERMINATE METHOD BELOW
    # ==============================
    def systemTerminate(root):
        response = tk.messagebox.askyesno(title = "Are you sure?", message = "You are about to close the program!\nAll unsaved data/changes will be lost.\nAre you sure?")
        if(response):
            sys.exit(0)
        else:
            return

    # ==============================
    # PAGE SWITCHING METHODS BELOW
    # ==============================
    # Open About page on click
    def aboutPage(self):
        AboutPopup(self)

    # Bring the homepage to the front on click
    def raiseHomepage(self):
        self.pageDict['home'].updateStats()
        self.pageDict['home'].lift()
        self.master.title(' HomePage - InvenPro V0.1A')

    # Bring the PC page to the front on click
    def raisePCPage(self):
        self.pageDict['cpuMenu'].lift()
        self.master.title(' CPU List - InvenPro')

    # Bring the Software page to the front on click
    def raiseSoftwarePage(self):
        self.pageDict['softwareMenu'].lift()
        self.master.title(' Software List - InvenPro')

    # Bring the Office page to the front on click
    def raiseOfficePage(self):
        self.pageDict['officeMenu'].lift()
        self.master.title(' Office Inventory - InvenPro')

    # Bring the Field page to the front on click
    def raiseFieldPage(self):
        self.pageDict['fieldMenu'].lift()
        self.master.title(' Field Inventory - InvenPro')

    # Activate and run a help window (TODO: Implement)
    def helpIndex(self):
        print("HELP INDEX NOT IMPLEMENTED")
        return
    
    # ==============================
    # FILE>NEW METHODS BELOW
    # ==============================
    def newPC(self):
        self.raisePCPage()
        self.pageDict['cpuMenu'].addPC()
    
    def newSoftware(self):
        self.raiseSoftwarePage()
        self.pageDict['softwareMenu'].addSoftware()

    def newOfficeCat(self):
        self.raiseOfficePage()
        self.pageDict['officeMenu'].addCategory()

    def newFieldCat(self):
        self.raiseFieldPage()
        self.pageDict['fieldMenu'].addCategory()