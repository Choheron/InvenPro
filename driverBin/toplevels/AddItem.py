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

    # ==============================
    # TEXT BOX INTERRUPT METHOD BELOW
    # ==============================
    def ignoreInput(self):
        # Break the input and ignore input as a whole
        return 'break'

    def nextAvailNum(self):
        pass

    def popDataFrame(self):
        # Configure columns of data frame
        self.dataFrame.grid_columnconfigure(0, weight = 1)
        self.dataFrame.grid_columnconfigure(1, weight = 1)

        # Declare a data frame dict to hold all widgets
        self.dataDict = {}
        # Declare local row counter
        dRow = 0
        # Do special case for ID Num
        self.dataDict["ID"] = {}
        self.dataDict["ID"]['label'] = tk.Label(master = self.dataFrame, text = "Item ID:").grid(row = dRow, column = 0, sticky = "E")
        self.dataDict["ID"]['var'] = tk.StringVar(master = self.dataFrame, value = "")
        # Declare and populate Frame to hold ID Textbox and ID Button
        self.idFrame = tk.Frame(master = self.dataFrame)
        self.dataDict["ID"]['widget'] = tk.Text(master = self.idFrame, height = 1, width = 3)
        self.dataDict["ID"]['widget'].insert(tk.END, "XXX")
        # Place a label before the textbox that uses nickname
        tk.Label(master = self.idFrame, text = f"MASLD-{self.inventoryDict[self.category]['admin']['nickname']}-").grid(row = 0, column = 0, sticky = "E")
        # Place textbox in frame
        self.dataDict["ID"]['widget'].grid(row = 0, column = 1, sticky = "W")
        # Create and place next open id button
        ttk.Button(master = self.idFrame, text = "Next Open ID", style = "M.TButton", command = lambda: self.nextAvailNum()).grid(row = 0, column = 2, sticky = "EW")
        # Bind enter key and tab to deselect the textbox
        self.dataDict["ID"]['widget'].bind("<Return>", lambda x=None: self.ignoreInput())
        self.dataDict["ID"]['widget'].bind("<Tab>", lambda x=None: self.ignoreInput())
        # Place ID Frame
        self.idFrame.grid(row = dRow, column = 1, sticky = "EW")

        # Loop Through template and populate data frame

    def terminate(self):
        response = messagebox.askyesno(" Cancel Item Addition?", "If you cancel now, the item will NOT be added to the system.\nAre you sure you would like to cancel?")
        if(response):
            self.grab_release()
            self.destroy()
        else:
            return

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
        # Declare widget dictionary to store data
        self.widgetDict = {}
        # Populate the data frame
        self.popDataFrame()

        # Create master button frame
        buttonFrame = tk.Frame(master = self)
        # Create and place buttons
        self.saveBttn = ttk.Button(master = buttonFrame, text = "Save New Item", style = "M.TButton", command = lambda: print("Save Item Button Clicked"))
        self.resetBttn = ttk.Button(master = buttonFrame, text = "Reset", style = "M.TButton", command = lambda: print("Reset Button Clicked"))
        self.cancelBttn = ttk.Button(master = buttonFrame, text = "Cancel", style = "M.TButton", command = lambda: print("Cancel Button Clicked"))
        self.saveBttn.grid(row = 0, column = 0, sticky = "E")
        self.resetBttn.grid(row = 0, column = 1, sticky = "E")
        self.cancelBttn.grid(row = 0, column = 2, sticky = "E")
        # Place master button frame
        buttonFrame.grid(row = 2, column = 0, sticky = "E")

        # Intercept close button
        self.protocol("WM_DELETE_WINDOW", lambda: self.terminate())

        # Disable resizing
        self.resizable(0, 0)