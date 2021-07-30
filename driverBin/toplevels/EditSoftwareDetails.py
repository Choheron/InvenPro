import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from ..utils.settings import setIconInvenPro as setIcon

class EditSoftDetails(tk.Toplevel):
    softDict = None
    # Create a dictionary to hold all of the fields and their widgets
    internalDict = None

    def __init__(self, parent, softwareDict, selectedSoft, selectedPC):
        super().__init__(parent)
        self.parent = parent
        self.softDict = softwareDict
        self.internalDict = {}
        self.currSoft = selectedSoft
        self.currPC = selectedPC
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
    # APPLY METHOD (CLOSES THE WINDOW)
    # ==============================
    def apply(self):
        # Loop through all fields in the internal dict
        for field in self.internalDict:
            # Save based off of type of input
            if(self.internalDict[field]['type'] == 'Text'):
                # Save text for checking
                outString = self.internalDict[field]['widget'].get('1.0', 'end-1c')
                if((outString == "") or (outString == " ") or (outString == "\n")):
                    outString = "--"
                # Set software dict answer to the currently contained text
                self.softDict[self.currSoft][self.currPC][field] = outString
            else:
                # Save boolean values
                if(self.internalDict[field]['var'].get()):
                    self.softDict[self.currSoft][self.currPC][field] = "Y"
                else:
                    self.softDict[self.currSoft][self.currPC][field] = "N"
        
        self.softDict[self.currSoft][self.currPC]['LOG'] = (str)(datetime.now())[:-7]
        # Release grab and close window
        self.grab_release()
        self.destroy()

    # ==============================
    # RESET METHOD
    # ==============================
    def resetVals(self):
        # Ask user if they are sure they want to reset changes
        if(not(tk.messagebox.askyesno(" Warning", "This action will reset any unsaved changes you have made to these details. Are you sure?"))):
            return
        
        # Disable reset button as the reset process takes place
        self.sResetBttn.config(state = 'disabled')
        # Loop through all fields and reset their values to the ones currently stored in the software dict
        for field in self.internalDict:
            # Reset based off of type of input
            if(self.internalDict[field]['type'] == 'Text'):
                # Clear text box
                self.internalDict[field]['widget'].delete("1.0", tk.END)
                # Place original data in text box
                self.internalDict[field]['widget'].insert(tk.END, self.internalDict[field]['var'].get())
            else:
                # Check or uncheck the checkbox based off of original value
                if(self.softDict[self.currSoft][self.currPC][field] == "Y"):
                    self.internalDict[field]['widget'].select()
                else:
                    self.internalDict[field]['widget'].deselect()
        # Enable button once function is complete
        self.sResetBttn.config(state = 'normal')

    # ==============================
    # TERMINATE METHOD
    # ==============================
    def terminate(self):
        response = tk.messagebox.askokcancel(parent = self, title = " Are you sure?", message = "Any unsaved changes will be lost.\nAre you sure you want to cancel?")
        if(response):
            self.grab_release()
            self.destroy()
        else:
            return

    # ==============================
    # BUILD INTERNAL FRAME (DEATILS FRAME) METHOD
    # ==============================
    def popInternalFrame(self, internalFrame):
        currRow = 0
        # Populate editable fields from the template in order to control input types
        for field in self.softDict[self.currSoft]['template']:
            # Create an empty dict in the internal dict to control variables and widgets
            self.internalDict[field] = {}
            # Populate dict for field based off of input type
            if(self.softDict[self.currSoft]['template'][field] == "--"):
                self.internalDict[field]['type'] = 'Text'
                self.internalDict[field]['var'] = tk.StringVar(master = internalFrame, value = f'{self.softDict[self.currSoft][self.currPC][field]}')
                self.internalDict[field]['widget'] = tk.Text(master = internalFrame, height = 1, width = 30)
                self.internalDict[field]['widget'].insert(tk.END, self.internalDict[field]['var'].get())
                # Bind enter key and tab to deselect the textbox
                self.internalDict[field]['widget'].bind("<Return>", lambda x=None: self.ignoreInput())
                self.internalDict[field]['widget'].bind("<Tab>", lambda x=None: self.ignoreInput())
            else:
                self.internalDict[field]['type'] = 'Checkbox'
                self.internalDict[field]['var'] = tk.BooleanVar(master = internalFrame, value = (True if (self.softDict[self.currSoft][self.currPC][field] == "Y") else False))
                self.internalDict[field]['widget'] = tk.Checkbutton(master = internalFrame, var = self.internalDict[field]['var'], foreground = 'green')

            # Declare and place label, place widgets in loop
            tk.Label(master = internalFrame, text = f'{field}:', font = 'Times 11').grid(row = currRow, column = 0, sticky = "EW")
            self.internalDict[field]['widget'].grid(row = currRow, column = 1, sticky = "EW")
            currRow += 1

    # ==============================
    # BUILD WINDOW METHOD
    # ==============================
    def buildWindow(self):
        # Edit title to reflect the purpose of the window
        self.title(" Edit Software Details")

        # Create and place directions Frame, and populate it - calling the name and current selection of the software and PC
        sDirectionFrame = tk.Frame(master = self, bg = 'grey80')
        # Evenly distribute labels and columns of directions frame
        sDirectionFrame.grid_columnconfigure(0, weight = 1)
        sDirectionFrame.grid_columnconfigure(1, weight = 1)
        # Create directions labels
        sMainDirLabel = tk.Label(master = sDirectionFrame, text = "Edit the fields below as needed, the changes made will be FINAL.", bg = 'grey80', font = ("Helvetica", "13", "bold"))
        sCurrEditLabel = tk.Label(master = sDirectionFrame, text = "Currently editing data for:", bg = 'grey80', font = ("Helvetica", "12"))
        # Create information frame
        sCurrInfoFrame = tk.Frame(master = sDirectionFrame, bg = 'grey80')
        # Format information frame
        sCurrInfoFrame.grid_columnconfigure(0, minsize = 25)
        # Create informational labels, give them borders for visual improvement
        sCurrSoftLabel = tk.Label(master = sCurrInfoFrame, text = 'Software:',  bg = 'grey70', font = ("Helvetica", "10", "italic"), borderwidth = 1, relief = 'solid')
        sCurrPCLabel = tk.Label(master = sCurrInfoFrame, text = 'PC:',  bg = 'grey70', font = ("Helvetica", "10", "italic"), borderwidth = 1, relief = 'solid')
        sCurrSoftInfo = tk.Label(master = sCurrInfoFrame, text = f'{self.currSoft}',  bg = 'grey70', font = ("Helvetica", "10", "bold"), borderwidth = 1, relief = 'solid')
        sCurrPCInfo = tk.Label(master = sCurrInfoFrame, text = f'{self.currPC}',  bg = 'grey70', font = ("Helvetica", "10", "bold"), borderwidth = 1, relief = 'solid')
        # Place Directions labels
        sMainDirLabel.grid(row = 0, column = 0, columnspan = 2, sticky = "NESW")
        sCurrEditLabel.grid(row = 1, column = 0, sticky = "E")
        # Place informational labels
        sCurrSoftLabel.grid(row = 1, column = 1, sticky = "NESW")
        sCurrPCLabel.grid(row = 2, column = 1, sticky = "NESW")
        sCurrSoftInfo.grid(row = 1, column = 2, sticky = "NESW")
        sCurrPCInfo.grid(row = 2, column = 2, sticky = "NESW")
        # Place information frame
        sCurrInfoFrame.grid(row = 1, column = 1, sticky = "NESW")
        # Place Direction Frame
        sDirectionFrame.grid(row = 0, column = 0, sticky = "NESW")

        # Create canvas master frame and format columns
        sMainCanvasFrame = tk.Frame(master = self, borderwidth = 2, relief = 'sunken')
        sMainCanvasFrame.grid_columnconfigure(0, weight = 1)
        
        # Create and place center information canvas
        sMainCanvas = tk.Canvas(master = sMainCanvasFrame, highlightthickness = 0, borderwidth = 0)
        sMainCanvas.grid(row = 0, column = 0, sticky = 'NESW')
        # Create internal frame for all data
        sInfoFrame = tk.Frame(master = sMainCanvas)
        # Configure columns of internal frame
        sInfoFrame.grid_columnconfigure(0, weight = 1)
        sInfoFrame.grid_columnconfigure(1, weight = 1)
        # Populate internal frame (with call to another function)
        self.popInternalFrame(sInfoFrame)
        # Place internal frame into canvas window
        self.windowID = sMainCanvas.create_window((0, 0), window = sInfoFrame, anchor = 'n')

        # Create and place scrollbar for information canvas
        infoScrollBar = tk.Scrollbar(master = sMainCanvasFrame, orient = tk.VERTICAL, bd = 2, command = sMainCanvas.yview)
        infoScrollBar.grid(row = 0, column = 0, sticky = "NES")
        # Config scrollbar to have better relation to canvas in size
        sMainCanvas.config(yscrollcommand = infoScrollBar.set)
        # Define scrollable area
        sInfoFrame.bind('<Configure>', lambda event: sMainCanvas.config(scrollregion = sMainCanvas.bbox('all')))

        # Place canvas master frame
        sMainCanvasFrame.grid(row = 1, column = 0, sticky = "NESW")

        # Create master button frame
        sBttnFrame = tk.Frame(master = self)
        # Configure columns in button frame
        sBttnFrame.grid_columnconfigure(0, weight = 1)
        sBttnFrame.grid_columnconfigure(1, minsize = 260)
        sBttnFrame.grid_columnconfigure(2, weight = 1)
        sBttnFrame.grid_columnconfigure(3, weight = 1)
        # Create and place buttons in frame
        sSaveBttn = ttk.Button(master = sBttnFrame, text = "Apply", style = "M.TButton", command = lambda: self.apply())
        self.sResetBttn = ttk.Button(master = sBttnFrame, text = "Reset", style = "M.TButton", command = lambda: self.resetVals())
        sCancelBttn = ttk.Button(master = sBttnFrame, text = "Cancel", style = "M.TButton", command = lambda: self.terminate())
        # Place in Grid (skipping column 1 in order to space out buttons)
        sSaveBttn.grid(row = 0, column = 0, padx = .5, pady = .5, sticky = "W")
        self.sResetBttn.grid(row = 0, column = 2, padx = .5, pady = .5, sticky = "EW")
        sCancelBttn.grid(row = 0, column = 3, padx = .5, pady = .5, sticky = "EW")
        # Place button frame
        sBttnFrame.grid(row = 2, column = 0 , sticky = "NESW")

        # Intercept close button
        self.protocol("WM_DELETE_WINDOW", lambda: self.terminate())

        # Disable window resizing
        self.resizable(0, 0)