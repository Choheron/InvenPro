import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
from .utils import settings as GLOBAL


class StartPage(tk.Frame):
    def __init__(self, parent: tk.Frame, root, pageDict):
        super().__init__(parent)
        self.parent = parent
        self.pageDict = pageDict
        # TODO: Create an Icon for InvenPro
        root.title(' HomePage - InvenPro V0.1A')

        imageFrame = tk.Frame(master = self)
        greetingFrame = tk.Frame(master = self)
        
        # TODO: Replace with newer, nicer image
        image = ImageTk.PhotoImage(file = (os.getcwd() + '/driverBin/images/LogoV1Alpha.png'))
        startImage = tk.Label(master = imageFrame, image = image)
        startImage.image = image
        startImage.grid(row = 0, column = 0)

        greeting = tk.Label(master = greetingFrame, text = "Welcome to InvenPro!", fg = "black")
        greeting.grid(row = 0, column = 0)

        buttonStyle = ttk.Style()
        buttonStyle.map("M.TButton",
            foreground=[('pressed', 'red'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'black'), ('active', 'white')]
            )

        # Declare button Labelframe
        buttonFrame = tk.LabelFrame(master = self, text = "Pages", labelanchor = 'nw')
        # Configure button labelframe columns
        buttonFrame.grid_columnconfigure(0, weight = 1)
        # Populate button labelframe
        uCPUButton = ttk.Button(master = buttonFrame, text = "View Computers", style = "M.TButton", command = lambda: self.jumpToCPU())
        uSoftButton = ttk.Button(master = buttonFrame, text = "View Softwares", style = "M.TButton", command = lambda: self.jumpToSoftware())
        uOfficeButton = ttk.Button(master = buttonFrame, text = "View Office Inventory", style = "M.TButton", command = lambda: self.jumpToOffice())
        uFieldButton = ttk.Button(master = buttonFrame, text = "View Field Inventory", style = "M.TButton", command = lambda: self.jumpToField())
        uCPUButton.grid(row = 0, column = 0, sticky = "EW")
        uSoftButton.grid(row = 1, column = 0, sticky = "EW")
        uOfficeButton.grid(row = 2, column = 0, sticky = "EW")
        uFieldButton.grid(row = 3, column = 0, sticky = "EW")

        # Place master frames
        imageFrame.grid(row = 0, column = 0, columnspan = 2)
        greetingFrame.grid(row = 1, column = 0, columnspan = 2)
        buttonFrame.grid(row = 2, column = 0, sticky = "NESW")

        # Declare statistics frame
        statsLFrame = tk.LabelFrame(master = self, text = "Statistics", labelanchor = 'nw')
        # Configure statistics columns
        statsLFrame.grid_columnconfigure(0, weight = 1)
        statsLFrame.grid_columnconfigure(1, weight = 1)
        # Configure statistics rows
        for x in range(4):
            statsLFrame.grid_rowconfigure(x, minsize = 25)
        # Populate statistics frame
        totalPLabel = tk.Label(master = statsLFrame, text = "Total PCs Stored:")
        self.totalPData = tk.Label(master = statsLFrame)
        totalSLabel = tk.Label(master = statsLFrame, text = "Total Software Types:")
        self.totalSData = tk.Label(master = statsLFrame)
        totalOLabel = tk.Label(master = statsLFrame, text = "Total Office Items:")
        self.totalOData = tk.Label(master = statsLFrame)
        totalFLabel = tk.Label(master = statsLFrame, text = "Total Field Items:")
        self.totalFData = tk.Label(master = statsLFrame)
        # Place statistics frame labels
        totalPLabel.grid(row = 0, column = 0, sticky = "E")
        self.totalPData.grid(row = 0, column = 1)
        totalSLabel.grid(row = 1, column = 0, sticky = "E")
        self.totalSData.grid(row = 1, column = 1)
        totalOLabel.grid(row = 2, column = 0, sticky = "E")
        self.totalOData.grid(row = 2, column = 1)
        totalFLabel.grid(row = 3, column = 0, sticky = "E")
        self.totalFData.grid(row = 3, column = 1)
        self.updateStats()
        # Place statistics frame
        statsLFrame.grid(row = 2, column = 1, sticky = "NESW")


    def jumpToCPU(self):
        self.pageDict['cpuMenu'].lift()
        self.master.master.title(' CPU List - InvenPro')

    def jumpToSoftware(self):
        self.pageDict['softwareMenu'].lift()
        self.master.master.title(' Software List - InvenPro')

    def jumpToOffice(self):
        self.pageDict['officeMenu'].lift()
        self.master.master.title(' Office Inventory - InvenPro')

    def jumpToField(self):
        self.pageDict['fieldMenu'].lift()
        self.master.master.title(' Field Inventory - InvenPro')

    def updateStats(self):
        # Set PC count
        self.totalPData.config(text = f'{GLOBAL.pcDict["admin"]["cpuCount"]}')
        # Set software count
        softwareCount = 0
        for software in GLOBAL.softDict:
            if(software == 'admin'):
                continue
            softwareCount += 1
        self.totalSData.config(text = f'{softwareCount}')
        # Count office items
        officeItems = 0
        for cat in GLOBAL.officeDict:
            # Skip admin in count
            if(cat == "admin"):
                continue
            officeItems += GLOBAL.officeDict[cat]['admin']['count']
        self.totalOData.config(text = f'{officeItems}')
        # Count field items
        fieldItems = 0
        for cat in GLOBAL.fieldDict:
            # Skip admin field
            if(cat == "admin"):
                continue
            fieldItems += GLOBAL.fieldDict[cat]['admin']['count']
        self.totalFData.config(text = f'{fieldItems}')