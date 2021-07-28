import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk


class StartPage(tk.Frame):
    def __init__(self, parent: tk.Frame, root, pageDict):
        super().__init__(parent)
        self.parent = parent
        self.pageDict = pageDict
        root.title(' HomePage - InvenPro V0.1A')

        imageFrame = tk.Frame(master = self)
        greetingFrame = tk.Frame(master = self)
        buttonFrame = tk.Frame(master = self)

        image = ImageTk.PhotoImage(file = (os.getcwd() + '/driverBin/images/MASLD Logo/LogoCroppedTransparent.png'))
        startImage = tk.Label(master = imageFrame, image = image)
        startImage.image = image
        startImage.grid(row = 0, column = 0, columnspan = 3)

        greeting = tk.Label(master = greetingFrame, text = "Welcome to the MASLD Inventory Software!", fg = "black", height = 3, width = 100)
        greeting.grid(row = 0, column = 0)

        buttonStyle = ttk.Style()
        buttonStyle.map("M.TButton",
            foreground=[('pressed', 'red'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'black'), ('active', 'white')]
            )

        uCPUButton = ttk.Button(master = buttonFrame, text = "View Computers", style = "M.TButton", command = lambda: self.jumpToCPU())
        uSoftButton = ttk.Button(master = buttonFrame, text = "View Softwares", style = "M.TButton", command = lambda: self.jumpToSoftware())
        uPerifButton = ttk.Button(master = buttonFrame, text = "View Office Inventory", style = "M.TButton", command = lambda: self.jumpToOffice())
        uCPUButton.grid(row = 0, column = 0)
        uSoftButton.grid(row = 1, column = 0)
        uPerifButton.grid(row = 2, column = 0)

        imageFrame.grid(row = 0, column = 0)
        greetingFrame.grid(row = 1, column = 0)
        buttonFrame.grid(row = 2, column = 0)

    def jumpToCPU(self):
        self.pageDict['cpuMenu'].lift()
        self.master.master.title(' CPU List - InvenPro')

    def jumpToSoftware(self):
        self.pageDict['softwareMenu'].lift()
        self.master.master.title(' Software List - InvenPro')

    def jumpToOffice(self):
        self.pageDict['officeMenu'].lift()
        self.master.master.title(' Office Inventory - InvenPro')