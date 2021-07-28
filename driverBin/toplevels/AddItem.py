import tkinter as tk
from tkinter import messagebox, ttk

class AddItem(tk.Toplevel):
    def __init__(self, master, inventoryDict, currCategory):
        super().__init__(master)
        self.parent = master
        self.inventoryDict = inventoryDict
        self.category = currCategory
        self.grab_set()
        self.buildWindow()

    def popDataFrame(self):
        pass

    def buildWindow(self):
        self.title(f' Add New {self.category}')

        # Create direction master frame
        dirFrame = tk.Frame(master = self, bg = 'grey')
        # Create and place direction labels
        dirLabel1 = tk.Label(master = dirFrame, text = f"Fill out information to add a new {self.category}.", font = 'Times 20 bold', bg = 'grey')
        dirLabel2 = tk.Label(master = dirFrame, text = "Fill out the information for each field below. Please double check all information before submitting.", bg = 'grey')
        dirLabel1.grid(row = 0, column = 0, sticky = "EW")
        dirLabel2.grid(row = 1, column = 0, sticky = "EW")
        # Place direction master frame
        dirFrame.grid(row = 0, column = 0, sticky = "NESW")

        # Create frame to place data canvas and scrollbar, trying to maintain visual border -- FIRST MASTER CANVAS FRAME
        mainCanvasFrame = tk.Frame(master = self, borderwidth = 2, relief = 'sunken')
        mainCanvasFrame.grid_columnconfigure(0, weight = 1)

        # Create and place Canvas for the datas to be added
        self.dataCanvas = tk.Canvas(master = mainCanvasFrame, highlightthickness = 0, borderwidth = 0)
        self.dataCanvas.grid(row = 0, column = 0, sticky = "NSEW")
        # Create internal frame for all of the datas
        self.dataFrame = tk.Frame(master = self.dataCanvas)
        # Set weights of grid in frame
        self.dataFrame.grid_columnconfigure(0, weight = 1)
        self.dataFrame.grid_columnconfigure(1, weight = 1)
        # Attach frame to internals of center canvas
        self.windowID = self.dataCanvas.create_window((0, 0), window = self.dataFrame, anchor = 'n')

        # Create and place scrollbar for data canvas
        self.attrScrollBar = tk.Scrollbar(master = mainCanvasFrame, orient = tk.VERTICAL, bd = 2, command = self.dataCanvas.yview)
        self.attrScrollBar.grid(row = 0, column = 0, sticky = "NES")
        # Config scrollbar to have better relation to canvas in size
        self.dataCanvas.config(yscrollcommand = self.attrScrollBar.set)
        # Define scrollable area
        self.dataFrame.bind('<Configure>', lambda event: self.dataCanvas.config(scrollregion = self.dataCanvas.bbox('all')))

        # Place the data master frame
        mainCanvasFrame.grid(row = 1, column = 0, sticky = "NESW")
        # Populate the data frame
        self.popDataFrame()

        # Create master button frame
        buttonFrame = tk.Frame(master = self)
        # Create and place buttons
        self.saveBttn = ttk.Button(master = buttonFrame, text = "Save New Item", style = "M.TButton", command = lambda: print("Reset Button Clicked"))
        self.resetBttn = ttk.Button(master = buttonFrame, text = "Reset", style = "M.TButton", command = lambda: print("Reset Button Clicked"))
        self.cancelBttn = ttk.Button(master = buttonFrame, text = "Cancel", style = "M.TButton", command = lambda: print("Reset Button Clicked"))
        self.saveBttn.grid(row = 0, column = 0, sticky = "E")
        self.resetBttn.grid(row = 0, column = 1, sticky = "E")
        self.cancelBttn.grid(row = 0, column = 2, sticky = "E")
        # Place master button frame
        buttonFrame.grid(row = 2, column = 0, sticky = "E")