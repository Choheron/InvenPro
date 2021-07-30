import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from ..utils.settings import setIconInvenPro as setIcon

class AddItem(tk.Toplevel):
    dataDict = {}

    def __init__(self, master, inventoryDict, currCategory):
        super().__init__(master)
        self.parent = master
        self.inventoryDict = inventoryDict
        self.category = currCategory
        self.grab_set()
        self.focus_set()
        # Set Icon for Window
        setIcon(self)
        self.buildWindow()

    # ==============================
    # TEXT BOX INTERRUPT METHOD BELOW
    # ==============================
    def ignoreInput(self):
        # Break the input and ignore input as a whole
        return 'break'

    # ==============================
    # ID NUM HELPER METHODS BELOW
    # ==============================
    def nextAvailNum(self):
        # Get current item count
        currCount = self.inventoryDict[self.category]['admin']['count']
        # Add one to item count for proposed new item ID
        nextOpenID = (currCount + 1)
        if(nextOpenID < 10):
            out = f"00{nextOpenID}"
        elif(nextOpenID < 100):
            out = f"0{nextOpenID}"
        else:
            out = f"{nextOpenID}"
        # Return formatted ID
        return out
        
    def setNextNumText(self):
        # Get next available number in correct format
        nextNumString = self.nextAvailNum()
        # Clear the text widget
        self.dataDict["ID"]['widget'].delete('1.0', tk.END)
        # Insert next num
        self.dataDict["ID"]['widget'].insert(tk.END, nextNumString)

    # ==============================
    # DATA FRAME METHOD BELOW
    # ==============================
    def popDataFrame(self):
        # Declare a data frame dict to hold all widgets
        self.dataDict = {}
        # Declare local row counter
        dRow = 0
        # Do special case for ID Num
        self.dataDict["ID"] = {}
        self.dataDict["ID"]['label'] = tk.Label(master = self.dataFrame, text = f"{self.category.upper()} ID:", font = 'Times 11').grid(row = dRow, column = 0, sticky = "E")
        self.dataDict["ID"]['var'] = None
        # Declare and populate Frame to hold ID Textbox and ID Button
        self.idFrame = tk.Frame(master = self.dataFrame)
        # Format ID Frame columns
        self.idFrame.grid_columnconfigure(0, weight = 1)
        self.idFrame.grid_columnconfigure(1, weight = 1)
        self.idFrame.grid_columnconfigure(2, weight = 2)
        self.dataDict["ID"]['widget'] = tk.Text(master = self.idFrame, height = 1, width = 3)
        self.dataDict["ID"]['widget'].insert(tk.END, "XXX")
        # Place a label before the textbox that uses nickname
        tk.Label(master = self.idFrame, text = f"MASLD-{self.inventoryDict[self.category]['admin']['nickname']}-", font = ("Helvetica", "10", "italic")).grid(row = 0, column = 0, sticky = "E")
        # Place textbox in frame
        self.dataDict["ID"]['widget'].grid(row = 0, column = 1, sticky = "W")
        # Create and place next open id button
        ttk.Button(master = self.idFrame, text = "Next Open ID", style = "M.TButton", command = lambda: self.setNextNumText()).grid(row = 0, column = 2, sticky = "EW")
        # Bind enter key and tab to deselect the textbox
        self.dataDict["ID"]['widget'].bind("<Return>", lambda x=None: self.ignoreInput())
        self.dataDict["ID"]['widget'].bind("<Tab>", lambda x=None: self.ignoreInput())
        # Place ID Frame
        self.idFrame.grid(row = dRow, column = 1, sticky = "NESW")
        # Manually Increment dRow (NOTE: Look into a better way of doing this)
        dRow += 1

        # Loop Through template and populate data frame
        for field in self.inventoryDict[self.category]['template']:
            # Skip ID and LOG
            if((field == "ID") or (field == "LOG")):
                continue
            # Create dictionary for field
            self.dataDict[field] = {}
            self.dataDict[field]['label'] = tk.Label(master = self.dataFrame, text = f'{field}:', font = 'Times 11')
            # Place label
            self.dataDict[field]['label'].grid(row = dRow, column = 0, sticky = "E")
            # Assign text widget if field requires a text value
            if(self.inventoryDict[self.category]['template'][field] == "--"):
                self.dataDict[field]['var'] = None
                self.dataDict[field]['widget'] = tk.Text(master = self.dataFrame, height = 1, width = 40)
                # Bind enter key and tab to deselect the textbox
                self.dataDict[field]['widget'].bind("<Return>", lambda x=None: self.ignoreInput())
                self.dataDict[field]['widget'].bind("<Tab>", lambda x=None: self.ignoreInput())
            # Assign checkbutton widget and boolean based off of value
            else:
                self.dataDict[field]['var'] = tk.BooleanVar(master = self.dataFrame, value = False)
                self.dataDict[field]['widget'] = tk.Checkbutton(master = self.dataFrame, var = self.dataDict[field]['var'], fg = 'green')
                if(self.inventoryDict[self.category]['template'][field] == "Y"):
                    self.dataDict[field]['var'].set(True)
            # Place widget
            self.dataDict[field]['widget'].grid(row = dRow, column = 1)
            # Increment dRow
            dRow += 1

    # ==============================
    # SHOW ERROR METHOD BELOW
    # ==============================
    def showError(self, message):
        messagebox.showerror(" Add Item Error", message)
        return

    # ==============================
    # INPUT CHECKING METHOD BELOW
    # ==============================
    def checkID(self, idString):
        # Check for Null or empty string
        if((idString == None) or (idString == "")):
            return 'ERROR - ID number must be provided'
        elif(idString.strip() == ""):
            return 'ERROR - ID number cannot be only whitespace'
        # Check for length requirements
        elif(len(idString) != 3):
            return 'ERROR - ID number MUST be three characters long, if this is an issue of quantity of items please submit a bug report.'
        # Check if string has letters
        elif(not(idString.isdecimal())):
            return 'ERROR - ID number must be ONLY numerical values.'
        elif((f"MASLD-{self.inventoryDict[self.category]['admin']['nickname']}-{idString}") in self.inventoryDict[self.category]):
            return 'ERROR - ID number is already in use, please use an unused ID.'
        return idString
        
    def checkInput(self, input):
        # Check for Null or empty string, replace with '--'
        if((input == None) or (input == "")):
            return '--'
        elif(input.strip() == ""):
            return '--'
        # Check for "ERROR" string
        elif('ERROR' in input.upper()):
            return 'ERROR - No fields can contain the following string \"Error\" (Case Unsensitive).'
        else:
            return input

    # ==============================
    # APPLY METHOD BELOW - Closes window
    # ==============================
    def applyItem(self):
        outDict = {}
        itemID = f"MASLD-{self.inventoryDict[self.category]['admin']['nickname']}-"
        for field in self.inventoryDict[self.category]['template']:
            # Make the log the time of item addition
            if(field == "LOG"):
                outDict[field] = (str)(datetime.now())[:-7]
                continue
            # Check special case for ID
            if(field == "ID"):
                idString = self.dataDict[field]['widget'].get('1.0', 'end-1c')
                idOutString = self.checkID(idString)
                if('ERROR' in idOutString):
                    self.showError(message = f'The category could not be added. Error contained the following message for debug:\n{idOutString}')
                    return
                itemID += f'{idOutString}'
                outDict[field] = itemID
            # Check if widget is a Checkbutton
            if(isinstance(self.dataDict[field]['widget'], tk.Checkbutton)):
                if(self.dataDict[field]['var'].get()):
                    outDict[field] = "Y"
                else: 
                    outDict[field] = "N"
            else:
                # Check and format input of field for storage
                inputChecked = self.checkInput(self.dataDict[field]['widget'].get('1.0', 'end-1c'))
                if('ERROR' in inputChecked):
                    self.showError(message = f'The category could not be added. Error contained the following message for debug:\n{inputChecked}')
                    return
                outDict[field] = inputChecked
        
        # Store outDict in the inventory dict (Will save in office menu code)
        self.inventoryDict[self.category][itemID] = outDict
        self.inventoryDict[self.category]['admin']['count'] += 1
        # Release grab and close window
        self.grab_release()
        self.destroy()

    # ==============================
    # RESET METHOD BELOW
    # ==============================
    def resetValues(self):
        for field in self.dataDict:
            # Skip LOG field
            if(field == "LOG"):
                continue
            if(isinstance(self.dataDict[field]['widget'], tk.Checkbutton)):
                # Special case for active
                if(field == 'ACTIVE'):
                    self.dataDict[field]['var'].set(True)
                    continue
                self.dataDict[field]['var'].set(False)
            else:
                # Special case for ID
                if(field == 'ID'):
                    self.dataDict[field]['widget'].delete('1.0', tk.END)
                    self.dataDict[field]['widget'].insert(tk.END, 'XXX')
                    continue
                self.dataDict[field]['widget'].delete('1.0', tk.END)
    
    # ==============================
    # TERMINATE METHOD BELOW
    # ==============================
    def terminate(self):
        response = messagebox.askyesno(" Cancel Item Addition?", "If you cancel now, the item will NOT be added to the system.\nAre you sure you would like to cancel?")
        if(response):
            self.grab_release()
            self.destroy()
        else:
            return

    # ==============================
    # BUILD WINDOW METHOD - Called at Init
    # ==============================
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
        # Populate the data frame
        self.popDataFrame()
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
        

        # Create master button frame
        buttonFrame = tk.Frame(master = self)
        # Create and place buttons
        self.saveBttn = ttk.Button(master = buttonFrame, text = "Save New Item", style = "M.TButton", command = lambda: self.applyItem())
        self.resetBttn = ttk.Button(master = buttonFrame, text = "Clear All", style = "M.TButton", command = lambda: self.resetValues())
        self.cancelBttn = ttk.Button(master = buttonFrame, text = "Cancel", style = "M.TButton", command = lambda: self.terminate())
        self.saveBttn.grid(row = 0, column = 0, sticky = "E")
        self.resetBttn.grid(row = 0, column = 1, sticky = "E")
        self.cancelBttn.grid(row = 0, column = 2, sticky = "E")
        # Place master button frame
        buttonFrame.grid(row = 2, column = 0, sticky = "E")

        # Intercept close button
        self.protocol("WM_DELETE_WINDOW", lambda: self.terminate())

        # Disable resizing
        self.resizable(0, 0)