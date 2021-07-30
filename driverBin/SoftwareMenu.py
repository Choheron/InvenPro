import os
from datetime import datetime
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from .utils import settings as GLOBAL
from .toplevels.AddSoftware import AddSoftware
from .toplevels.EditSoftwareDetails import EditSoftDetails
from .toplevels.InputDialogue import InputDioBox


class SoftwareMenu(tk.Frame):
    DETAILFRAMECOL = 'gray70'

    def __init__(self, parent, root, pageDict):
        super().__init__(parent)
        self.parent = parent
        self.pageDict = pageDict
        self.pcDictLastUpdate = GLOBAL.pcDict['admin']['updated']
        # Configure column weights 
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.launchSoftwareDriver(root)

    # ==============================
    # ADD SOFTWARE METHOD BELOW
    # ==============================

    # NOTE: Be sure to always save the dict globally BEFORE reloading or refreshing (this is due to the save order of the items)
    def addSoftware(self):
        self.addSoftBttn.config(state = 'disabled')
        newName = tk.StringVar(master = self, value = None)
        addWindow = AddSoftware(self, GLOBAL.softDict, newName)
        self.wait_window(addWindow)
        # If no new software was added, return and do not change anything
        if((newName.get() == None) or (newName.get() == "None")):
            self.addSoftBttn.config(state = 'normal')
            return

        # Add default software values for each PC in the system
        for pc in GLOBAL.pcDict:
            if(pc == 'admin'):
                continue
            pcDict = {}
            # Add PC ID field and pass in the pc num
            pcDict['PC ID'] = pc
            for field in GLOBAL.softDict[newName.get()]['template']:
                pcDict[field] = GLOBAL.softDict[newName.get()]['template'][field]
            # Log the time of addition/most recent update
            pcDict['LOG'] = (str)(datetime.now())[:-7]
            # Add pc to software dictionary with default values
            GLOBAL.softDict[newName.get()][pc] = pcDict

        # Return the add software button to normal state    
        self.addSoftBttn.config(state = 'normal')
        # Set newName to None
        newName.set(None)
        # Save global software dict to system
        GLOBAL.saveSoftdict()
        # Refresh software list
        self.refreshSoftList()
        # Check software dict against pc dict
        self.checkSoftwares()
        # Update software label to signify last update
        self.updateTextLabel.config(text = f'{GLOBAL.softDict["admin"]["updated"]}')
        return

    # ==============================
    # EDIT SOFTWARE DETAILS METHOD BELOW
    # ==============================
    def editDetails(self):
        # Get the current selections
        software = str((self.softwareListBox.get(self.softwareListBox.curselection())))
        pc = str((self.pcListBox.get(self.pcListBox.curselection())))[:12]
        # Disable edit details button
        self.editDetailsBttn.config(state = 'disabled')
        # Declare new edit details window
        editWin = EditSoftDetails(self, GLOBAL.softDict, software, pc)
        # Wait for edit window to terminate
        self.wait_window(editWin)
        # Reenable edit details button
        self.editDetailsBttn.config(state = 'normal')
        # Save changes to JSON
        GLOBAL.saveSoftdict()
        # Refresh the software list
        self.refreshSoftList()

    # ==============================
    # EDIT SOFTWARE DETAILS METHOD BELOW
    # ==============================
    def editSoftAttributes(self):
        warnWindow = tk.messagebox.showwarning(" Feature not yet implemented", "This feature has not yet been implemented, as InvenPro is a work is progress and may require revising and further expanding." +
                                                    "\nFor the time being, you can delete the previous software and readd a new one, just be sure to write down all the values!\nThank you for your patience.")
        return

    # ==============================
    # DELETE SOFTWARE METHOD BELOW
    # ============================== 
    def delSoftware(self):
        # Get currently selected software from software list
        software = str((self.softwareListBox.get(self.softwareListBox.curselection())))
        # Store result variable
        resultVar = tk.StringVar(master = self, value = "")
        # Write out message
        wMessage = "WARNING: Please note, deletion of a software is FINAL and will result in the loss of ALL associated data.\n\nIf you are SURE you would like to delete "
        wMessage += f"the software from the system, please type the software name as seen on screen and press submit.\nSoftware: \"{software}\""
        # Delcare and wait for user input
        warningWin = InputDioBox(self, " Are you sure?", wMessage, resultVar)
        self.wait_window(warningWin)
        # Delete software from list if user input correctly
        if(resultVar.get() == software):
            # Delete software from dict
            del GLOBAL.softDict[software]
            # Refresh listbox if a software was deleted
            self.refreshSoftList()
            tk.messagebox.showinfo(" Deletion successful", f"Successfully deleted {software} from the system... If this was a mistake you will need to re-add the software and re-enter all associated data.")
            # Save new dict to finalize deletion
            GLOBAL.saveSoftdict()
        else:
            tk.messagebox.showinfo(" Deletion UNSUCESSFUL", f"IMPORTANT: {software} has NOT been deleted from the system.")
        
        return

    # ==============================
    # DETAIL BOX/CANVAS METHODS BELOW
    # ==============================
    def popDetailBox(self):
        # Store the currently selected software and pc
        software = str((self.softwareListBox.get(self.softwareListBox.curselection())))
        pc = str((self.pcListBox.get(self.pcListBox.curselection())))[:12]

        # Clear the detail frame
        self.clearDetailFrame()
        # Update label to show current information
        self.dTopLabel.config(text = f'Displaying \"{software}\" information for \"{pc}\":')

        # Make columns have weight of 1 and minimum sizes to avoid ugly visual movement
        self.detailFrame.grid_columnconfigure(0, weight = 1)
        self.detailFrame.grid_columnconfigure(0, minsize = 200)
        self.detailFrame.grid_columnconfigure(1, weight = 1)
        self.detailFrame.grid_columnconfigure(1, minsize = 200)

        # Declare local row counter and varList
        dRow = 0
        checkVarInt = 0
        # Declare a list of vars to be used for the checkbuttons (NOTE: IMPORTANT - This setup is required in order to avoid garbage collection and maintain values)
        self.checkVars = []
        # Loop through fields and place them on the detail canvas
        for field in GLOBAL.softDict[software]['fields']:
            if(field == 'PC ID'): # Skip PC ID, as it is shown in a label above and selected by the user
                continue
            # Create and place a label corresponding to the field
            fieldLabel = tk.Label(master = self.detailFrame, text = f'{field}:', font = "Times 12 bold", bg = self.DETAILFRAMECOL)
            fieldLabel.grid(row = dRow, column = 0, sticky = "E")
            # Declare placeholder for either checkbox or label
            value = None
            # Assign a checkbox to values that correspond to a Y/N or True/False
            if((GLOBAL.softDict[software][pc][field] == 'Y') or (GLOBAL.softDict[software][pc][field] == 'N')):
                self.checkVars.insert(checkVarInt, tk.BooleanVar())
                value = tk.Checkbutton(master = self.detailFrame, var = self.checkVars[checkVarInt], bg = self.DETAILFRAMECOL, disabledforeground = 'green')
                # Set checkbox status depending on variable
                if(GLOBAL.softDict[software][pc][field] == 'Y'):
                    self.checkVars[checkVarInt].set(True)
                else:
                    self.checkVars[checkVarInt].set(False)
                # Disable the checkbutton so the user cannot toggle it, then increment the checkbutton list
                value.config(state = 'disabled')
                checkVarInt += 1
            else:
                value = tk.Label(master = self.detailFrame, text = GLOBAL.softDict[software][pc][field], bg = self.DETAILFRAMECOL)
            # Place either checkbutton or label and increment row counter
            value.grid(row = dRow, column = 1, sticky = 'EW')
            dRow += 1
        # Enable the edit detail button
        self.editDetailsBttn.config(state = 'normal')
        
    def clearDetailFrame(self):
        # Clear the detail frame of all widgets if need be
        for wid in self.detailFrame.winfo_children():
            wid.destroy()

    # ==============================
    # LISTBOX POPULATION/HANDLING METHODS BELOW
    # ============================== 
    def softwareBoxSelect(self):
        # Enable edit software attributes button
        self.editSoftBttn.config(state = 'normal')
        # Enable delete software button
        self.deleteSoftBttn.config(state = 'normal')
        # Clear the detail frame and reset detail window label
        self.clearDetailFrame()
        self.dTopLabel.config(text = f'Select a PC to see details in the window below:')
        # Ensure the edit details button is disabled in order to make sure the user cannot cause error
        self.editDetailsBttn.config(state = 'disabled')

        # Check for new PC (if there is a difference in the last update times)
        if(self.pcDictLastUpdate != GLOBAL.pcDict['admin']['updated']):
            self.checkSoftwares()
            self.pcDictLastUpdate = GLOBAL.pcDict['admin']['updated']

        # Activate the listbox if it is still disabled at call
        self.activateListbox(self.pcListBox)
        # Clear list of any previous entries
        self.pcListBox.delete(0, tk.END)

        # Get the string value of the selected item
        selectedvalue = str((self.softwareListBox.get(self.softwareListBox.curselection())))

        # Set local dict for easier referece
        softDict = GLOBAL.softDict[selectedvalue]

        for pc in softDict:
            # Skip template dict
            if(pc == "template"):
                continue
            # Store and skip the fields attribute (fields are used for procedural display)
            if(pc == "fields"):
                fields = softDict[pc]
                continue
            self.pcListBox.insert(tk.END, (pc + ": " + GLOBAL.pcDict[pc]['userInit']))
            # Special cases for Microsoft Office, TODO: See a way to improve this and abstract it
            if(selectedvalue == "Microsoft Office"): 
                anyInstalled = False
                for field in fields:
                    # Skip non-install related functions
                    if((field == "PC ID") or (field == "EDITION") or (field == "LOG")): 
                        continue
                    else:
                        # Switch install to true if ANY of the office programs are installed
                        if(softDict[pc][field] == "Y"):
                            anyInstalled = True 
                if(anyInstalled):
                    self.pcListBox.itemconfig(tk.END, bg = 'yellow green')
                else:
                    self.pcListBox.itemconfig(tk.END, bg = 'indian red')
                # Move onto next PC, skipping the default coloring statements below
                continue

            if(softDict[pc]['INSTALLED'] == "Y"):
                self.pcListBox.itemconfig(tk.END, bg = 'yellow green')
            else:
                self.pcListBox.itemconfig(tk.END, bg = 'indian red')

    # Method to be run when the PC listbox is selected
    def pcBoxSelect(self):
        self.popDetailBox()

    # "Activates"(Sets state to normal) the listbox passed in
    def activateListbox(self, listbox: tk.Listbox):
        listbox.config(state = 'normal')
        listbox.config(bg = 'white')

    # "Disables"(Sets state to disabled) the listbox passed in
    def disableListbox(self, listbox: tk.Listbox):
        listbox.config(state = 'disabled')
        listbox.config(bg = 'ivory4')

    # Refresh software listbox
    def refreshSoftList(self):
        # Clear detail window and reset detail window label
        self.clearDetailFrame()
        self.dTopLabel.config(text = f'Select a software and a PC to see details in the window below:')
        # Delete current contents of software listbox
        self.softwareListBox.delete(0, tk.END)
        # Reload software dict GLOBALLY
        GLOBAL.loadSoftdict()
        # Populate list with items based off of number of softwares (Skip admin dict)
        for software in GLOBAL.softDict: 
            if(software == 'admin'):
                continue
            self.softwareListBox.insert(tk.END, software)
        
        # Delete contents of pc listbox and disable
        self.pcListBox.delete(0, tk.END)
        self.disableListbox(self.pcListBox)
        # Disable edit details button until a PC is selected
        self.editDetailsBttn.config(state = 'disabled')
        # Disable edit softwares button until a software is selected
        self.editSoftBttn.config(state = 'disabled')
        # Disable delete software button until a software is selected
        self.deleteSoftBttn.config(state = 'disabled')
    
    # ==============================
    # SOFTWARE DICTIONARY CHECK METHODS BELOW
    # ============================== 
    def checkSoftwares(self):
        # Loop through all softwares and check to see if they have PCs that arent included in the cpuJSON, then delete them
        for software in GLOBAL.softDict:
            # Skip admin dict
            if(software == "admin"):
                continue
            # Loop through all PCs currently stored in the software dict
            for PC in list(GLOBAL.softDict[software]):
                # Skip unimportant elements
                if(PC == 'template' or PC == 'fields'):
                    continue
                # Delete PC from software lists if the PC is not in the master CPU list
                if(not(PC in GLOBAL.pcDict)):
                    del GLOBAL.softDict[software][PC]
        
        # Loop through all PCs in cpuJSON (And add PC to each software that doesnt contain it)
        for PC in GLOBAL.pcDict:
            # Skip admin dict
            if(PC == "admin"):
                continue
            # Loop through all softwares for each PC
            for software in GLOBAL.softDict:
                # Skip admin dict
                if(software == "admin"):
                    continue
                # Add PC to software dict if it is not already in there
                if(not(PC in list(GLOBAL.softDict[software]))):
                    GLOBAL.softDict[software][PC] = {}
                    GLOBAL.softDict[software][PC]['PC ID'] = PC
                    for field in GLOBAL.softDict[software]['fields']:
                        # Skip fields that are not included in the template
                        if((field == "PC ID") or (field == "LOG")):
                            continue
                        GLOBAL.softDict[software][PC][field] =  GLOBAL.softDict[software]['template'][field]
                    GLOBAL.softDict[software][PC]['LOG'] = None
        # Save changes made.
        GLOBAL.saveSoftdict()

    # ==============================
    # DRIVER BULK METHODS BELOW
    # ============================== 
    def launchSoftwareDriver(self, root):
        # Check softJSON dict for missing PCs
        self.checkSoftwares()

        # Declare directions master frame
        directionFrame = tk.Frame(master = self)

        # Declare instruction label, last updated label, update text label
        instLabel = tk.Label(master = directionFrame, text = "Below is a list of all softwares, click on one expand the menu.")
        upTextLabel = tk.Label(master = directionFrame, text = "Software List Last Updated:")
        self.updateTextLabel = tk.Label(master = directionFrame, text = f'{GLOBAL.softDict["admin"]["updated"]}')
        # Set weight to avoid strange spacing
        directionFrame.grid_columnconfigure(0, weight = 1)
        directionFrame.grid_columnconfigure(1, weight = 1)
        # Place instruction label, last updated label, update text label
        instLabel.grid(row = 0, column = 0, columnspan = 2, sticky = "EW")
        upTextLabel.grid(row = 1, column = 0, sticky = "E")
        self.updateTextLabel.grid(row = 1, column = 1, sticky = "W")

        # Declare and place list title labels
        softListLabel = tk.Label(master = directionFrame, text = "Software List:")
        pcListLabel = tk.Label(master = directionFrame, text = "PC List:")
        softListLabel.grid(row = 2, column = 0, sticky = "W")
        pcListLabel.grid(row = 2, column = 1, sticky = "W")

        # Place directions master frame
        directionFrame.grid(row = 0, column = 0, columnspan = 2, sticky = "NSEW")

        # Declare and place software listbox, populate it with software names
        self.softwareListBox = tk.Listbox(master = self, width = 66, height = 20, selectmode = 'single', exportselection = False)
        for software in GLOBAL.softDict: # Populate list with items based off of number of softwares (Skip admin dict)
            if(software == 'admin'):
                continue
            self.softwareListBox.insert(tk.END, software)
        self.softwareListBox.grid(row = 1, column = 0, sticky = 'W')

        # Delcare scrollbar for the software listBox
        self.softListBoxScroll = tk.Scrollbar(master = self)
        self.softListBoxScroll.grid(row = 1, column = 0, sticky = 'NSE')
        # Link software listbox and scrollbar
        self.softwareListBox.config(yscrollcommand = self.softListBoxScroll.set)
        self.softListBoxScroll.config(command = self.softwareListBox.yview)
        # Bind the update function to the selecting of an item in the software listbox
        self.softwareListBox.bind('<<ListboxSelect>>', lambda x=None: self.softwareBoxSelect())

        # Declare and place secondary listbox for PC selection, disable it until a software is selected
        self.pcListBox = tk.Listbox(master = self, width = 66, height = 20, selectmode = 'single', exportselection = False)
        self.pcListBox.grid(row = 1, column = 1, sticky = 'W')
        self.disableListbox(self.pcListBox)

        # Delcare scrollbar for the pc listBox
        self.pcListBoxScroll = tk.Scrollbar(master = self)
        self.pcListBoxScroll.grid(row = 1, column = 1, sticky = 'NSE')
        # Link pc listbox and scrollbar
        self.pcListBox.config(yscrollcommand = self.pcListBoxScroll.set)
        self.pcListBoxScroll.config(command = self.pcListBox.yview)
        # Bind the detail display function to the selecting of an item in the pc listbox
        self.pcListBox.bind('<<ListboxSelect>>', lambda x=None: self.pcBoxSelect())

        # Declare master frame for software buttons
        self.softBttnFrame = tk.Frame(master = self)
        # Populate software button frame with buttons
        self.addSoftBttn = ttk.Button(master = self.softBttnFrame, text = "Add New Software", style = "M.TButton", command = lambda: self.addSoftware())
        self.editSoftBttn = ttk.Button(master = self.softBttnFrame, text = "Edit Software", style = "M.TButton", command = lambda: self.editSoftAttributes())
        self.deleteSoftBttn = ttk.Button(master = self.softBttnFrame, text = "Delete Software", style = "M.TButton", command = lambda: self.delSoftware())
        self.refreshSoftBttn = ttk.Button(master = self.softBttnFrame, text = "Refresh Software List", style = "M.TButton", command = lambda: self.refreshSoftList())
        self.addSoftBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "W")
        self.deleteSoftBttn.grid(row = 0, column = 1, padx = 1, pady = .5, sticky = "W")
        self.editSoftBttn.grid(row = 0, column = 2, padx = 1, pady = .5, sticky = "W")
        self.refreshSoftBttn.grid(row = 0, column = 3, padx = 1, pady = .5, sticky = "W")
        # Place software button frame
        self.softBttnFrame.grid(row = 2, column = 0, sticky = "NSEW")

        # Create and place overall label for detail information
        self.dTopLabel = tk.Label(master = self, text = f'Select a software and a PC to see details in the window below:', font = ("Helvetica", "12", "italic"))
        self.dTopLabel.grid(row = 3, column = 0, columnspan = 2, sticky = "W")

        # Create frame to place canvas and scrollbar in, trying to maintain visual border
        canvasParentFrame = tk.Frame(master = self, borderwidth = 2, bg = self.DETAILFRAMECOL, relief = 'sunken')
        canvasParentFrame.grid_columnconfigure(0, weight = 1)

        # Create detail canvas, required for scrollbar and procedural population to function as needed.
        self.detailCanvas = tk.Canvas(master = canvasParentFrame, highlightthickness = 0, borderwidth = 0, bg = self.DETAILFRAMECOL)
        self.detailCanvas.grid(row = 0, column = 0, sticky = "NSEW")
        # Create frame for labels and text boxes
        self.detailFrame = tk.Frame(master = self.detailCanvas, bg = self.DETAILFRAMECOL)
        # Set weights of grid in frame
        self.detailFrame.grid_columnconfigure(0, weight = 1)
        self.detailFrame.grid_columnconfigure(1, weight = 1)
        # Attach frame to internals of center canvas
        self.windowID = self.detailCanvas.create_window((0, 0), window = self.detailFrame, anchor = 'n')

        # Create and place scrollbar for detail canvas
        self.detailScrollBar = tk.Scrollbar(master = canvasParentFrame, orient = tk.VERTICAL, bd = 2, command = self.detailCanvas.yview)
        self.detailScrollBar.grid(row = 0, column = 0, sticky = "NSE")
        # Config scrollbar to have better relation to canvas in size
        self.detailCanvas.config(yscrollcommand = self.detailScrollBar.set)
        # Strange line of code, required for scrollbar to work, defines scrollable area
        self.detailFrame.bind('<Configure>', lambda event: self.detailCanvas.config(scrollregion = self.detailCanvas.bbox('all')))

        # Place master frame containing canvas and canvas scrollbar
        canvasParentFrame.grid(row = 4, column = 0, columnspan = 2, sticky = "NESW")

        # Create and place edit details button
        self.editDetailsBttn = ttk.Button(master = self, text = "Edit Details", style = "M.TButton", command = lambda: self.editDetails())
        self.editDetailsBttn.grid(row = 5, column = 1, sticky = "E")
        # Disable edit details, edit software and delete software button until a PC or Software is selected
        self.editSoftBttn.config(state = 'disabled')
        self.editDetailsBttn.config(state = 'disabled')
        self.deleteSoftBttn.config(state = 'disabled')

        return