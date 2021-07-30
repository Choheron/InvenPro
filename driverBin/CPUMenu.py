import os, json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from .utils import ExcelReader
from .utils import settings as GLOBAL
from .toplevels.EditCPU import EditCPUMenu
from .toplevels.AddCPU import AddCPUMenu


class CPUMenu(tk.Frame):
    __currentlyViewing = {}
    __currIndex = 0
    __cpuListBox = None

    def __init__(self, parent, root, pageDict):
        super().__init__(parent)
        self.parent = parent
        self.pageDict = pageDict
        # Configure column weights
        self.grid_columnconfigure(3, weight = 1)
        self.grid_columnconfigure(4, weight = 1)
        self.launchCPUDriver(root)

    # ==============================
    # SHOW DETAIL METHODS BELOW
    # ============================== 

    # Helper method to assist in getting PC keys and ignoring the admin dict
    def getPCKey(self, index):
        pcKeys = list(GLOBAL.pcDict.keys())
        pcKeys.remove('admin') #remove admin key to maintain correct indexing
        return pcKeys[index]

    def showDetails(self, currSelection):
        self.__currIndex = currSelection # Set internal tracker of selection to index being displayed.
        pcKey = self.getPCKey(currSelection) # Subtract one due to indexing starting from zero.
        self.__currentlyViewing = GLOBAL.pcDict[pcKey]
        self.cDetailLabel.config(text = f'Showing Data for: {self.__currentlyViewing["idnum"]}')
        
        self.dataLabelList[0].config(text = f'{GLOBAL.pcDict[pcKey]["ipv4"]}')
        self.dataLabelList[1].config(text = f'{GLOBAL.pcDict[pcKey]["location"]}')
        self.dataLabelList[2].config(text = f'{GLOBAL.pcDict[pcKey]["userInit"]}')
        self.dataLabelList[3].config(text = f'{GLOBAL.pcDict[pcKey]["user"]}')
        self.dataLabelList[4].config(text = f'{GLOBAL.pcDict[pcKey]["build"]}')
        self.dataLabelList[5].config(text = f'{GLOBAL.pcDict[pcKey]["type"]}')
        self.dataLabelList[6].config(text = f'{GLOBAL.pcDict[pcKey]["cost"]}')
        self.dataLabelList[7].config(text = f'{GLOBAL.pcDict[pcKey]["year"]}')
        self.dataLabelList[8].config(text = f'{GLOBAL.pcDict[pcKey]["manufacturer"]}')
        # self.dataLabelList[9].config(text = f'{GLOBAL.pcDict[pcKey]["softwares"]}') -- REMOVED, BUTTON REPLACEMENT 07/21/2021
        self.dataLabelList[9].config(text = f'{GLOBAL.pcDict[pcKey]["wifi"]}')
        self.dataLabelList[10].config(text = f'{GLOBAL.pcDict[pcKey]["gpu"]}')
        self.dataLabelList[11].config(text = f'{GLOBAL.pcDict[pcKey]["cpu"]}')
        self.dataLabelList[12].config(text = f'{GLOBAL.pcDict[pcKey]["mobo"]}')
        self.dataLabelList[13].config(text = f'{GLOBAL.pcDict[pcKey]["ram"]}')
        self.dataLabelList[14].config(text = f'{GLOBAL.pcDict[pcKey]["storage"]}')
        self.dataLabelList[15].config(text =  f'{GLOBAL.pcDict[pcKey]["os"]}')
        self.dataLabelList[16].config(text = f'{GLOBAL.pcDict[pcKey]["lastRowUpdate"]}')

        self.cEditDetailButtn.config(state = 'normal')

    # ==============================
    # EDIT DETAIL METHODS BELOW
    # ============================== 
    def editDetails(self, currentlyViewing):
        # Disable edit button while edit window is open
        self.cEditDetailButtn.config(state = 'disabled')
        self.__cpuListBox.config(state = 'disabled')
        # Open a toplevel edit window and await its destruction
        editWindow = EditCPUMenu(self, currentlyViewing) 
        self.wait_window(editWindow)
        self.__cpuListBox.config(state = 'normal')
        # Refresh the listbox to change the name assosciated with the CPU if that was edited
        self.refreshListBox() 
        # Reactivate the edit button
        self.cEditDetailButtn.config(state = 'normal') 
        # Set the selection to the previously selected PC
        self.__cpuListBox.selection_set(self.__currIndex) 
        # Update the display to show the recent changes
        self.showDetails(self.__currIndex) 
        # Save changes to PC storage file
        GLOBAL.savePCdict()

    # ==============================
    # ADD COMPUTER METHODS BELOW
    # ============================== 

    # NOTE: Be sure to always save the dict globally BEFORE reloading or refreshing (this is due to the save order of the items)
    def addPC(self):
        # Disable add button while add window is open
        self.cAddPCButtn.config(state = 'disabled') 
        self.__cpuListBox.config(state = 'disabled')
        # Open a toplevel add window and await its destruction
        addWindow = AddCPUMenu(self) 
        self.wait_window(addWindow)
        # Reactivate the add button
        self.cAddPCButtn.config(state = 'normal') 
        self.__cpuListBox.config(state = 'normal')
        # Save changes to PC storage file
        GLOBAL.savePCdict()
        # Refresh the listbox to show new addition
        self.refreshListBox()
        # Set the current index to the added PC
        self.__currIndex = (GLOBAL.pcDict['admin']['cpuCount'] - 1)
        # Select the added PC
        self.__cpuListBox.select_set(self.__currIndex)
        # Update the display to show the added PC
        self.showDetails(self.__currIndex)


    # ==============================
    # LIST NAVIGATION METHODS BELOW
    # ============================== 
    def listBoxUpdate(self):
        try:
            self.__currIndex = self.__cpuListBox.curselection()[0]
            self.showDetails(self.__currIndex)
        except Exception as E:
            print(f'DEBUG: CPUMenu.listBoxUpdate(), Error Text:' + str(E))
        return

    def arrowUp(self):
        if(self.__currIndex >= 1):
            self.__currIndex = self.__currIndex - 1
    
    def arrowDown(self):
        if(self.__currIndex < len(GLOBAL.pcDict)):
            self.__currIndex = self.__currIndex + 1

    def returnPress(self):
        self.showDetails(self.__currIndex)
        self.__cpuListBox.selection_clear(0, tk.END)
        self.__cpuListBox.selection_set(self.__currIndex)
        return

    # ==============================
    # LIST POPULATION AND CONTROL METHODS BELOW
    # ==============================

    def refreshListBox(self):
        self.__cpuListBox.delete(0, tk.END)

        # Reload PC dict to ensure any new data is pulled
        GLOBAL.loadPCdict()

        # Populate list with items based off of number of computers TODO: Fix possible number issue with removed PC 
        for number in range(1, GLOBAL.pcDict['admin']['cpuCount'] + 1): 
            if(number < 10):
                out = f'MASLD-PC-00{number}'
            elif(number < 100):
                out = f'MASLD-PC-0{number}'
            else:
                out = f'MASLD-PC-{number}'

            self.__cpuListBox.insert(number, (out + f': {GLOBAL.pcDict[out]["userInit"]}'))
        
        GLOBAL.pcDict['admin']['updated'] = (str)(datetime.now())[:-7]
        self.clastUpdatedLabel.config(text = f'Updated: {GLOBAL.pcDict["admin"]["updated"]}')

    # ==============================
    # PROGRAM NAVIGATION METHODS BELOW
    # ==============================
    def jumpToSoftware(self):
        self.pageDict['softwareMenu'].lift()
        self.master.master.title(' Software List - InvenPro')

    # ==============================
    # DRIVER METHODS BELOW
    # ============================== 
    def launchCPUDriver(self, root):
        # Below: ALL GUI Elements related to the List of Computers and the labels above it.
        ctopLabel = tk.Label(master = self, text = "A list of the current computers can be found below:")
        ctopLabel.grid(row = 0, column = 0, columnspan = 4)

        # Delcare and Place label representing the last time the data was pulled from the excel sheet
        self.clastUpdatedLabel = tk.Label(master = self, text = f'Updated: {GLOBAL.pcDict["admin"]["updated"]}')
        self.clastUpdatedLabel.grid(row = 2, column = 0, columnspan = 2)

        # Button to refresh list
        cRefreshButtn = tk.ttk.Button(master = self, text = "Refresh", style = "M.TButton", command = lambda: self.refreshListBox())
        cRefreshButtn.grid(row = 2, column = 2, sticky = "WE")

        # Declare CPU Listbox and populate it with the names of the computers
        self.__cpuListBox = tk.Listbox(master = self, width = 50, height = 30, selectmode = 'single', exportselection = False)
        for PC in GLOBAL.pcDict: # Populate list with items based off of number of computers TODO: Fix possible number issue with removed PC
            # Skip admin dict
            if(PC == 'admin'):
                continue
            self.__cpuListBox.insert(tk.END, (PC + f': {GLOBAL.pcDict[PC]["userInit"]}'))
        self.__cpuListBox.grid(row = 3, column = 0, columnspan = 3, sticky = 'W')

        # Delcare the scrollbar for the listBox
        self.listBoxScroll = tk.Scrollbar(master = self)
        self.listBoxScroll.grid(row = 3, column = 2, sticky = 'NES')

        # Link listbox and scrollbar
        self.__cpuListBox.config(yscrollcommand = self.listBoxScroll.set)
        self.listBoxScroll.config(command = self.__cpuListBox.yview)

        # Declare and place directions label
        self.cDetailLabel = tk.Label(master = self, text = "Select a computer from the list to see more information here.", font = 'bold')
        self.cDetailLabel.grid(row = 2, column = 3, sticky = "W")

        # Below: ALL GUI Elements related to the display of individual CPU information of the right side of the window.
        self.dataLabelList = []

        # Create master frame for all labels to be placed in
        cDetailFrame = tk.Frame(master = self, bd = 2,relief = 'sunken')
        # Configure master frame columns
        cDetailFrame.grid_columnconfigure(0, minsize = 150)
        cDetailFrame.grid_columnconfigure(1, minsize = 200)

        cIPLabel = tk.Label(master = cDetailFrame, text = f'IPV4 ADDRESS:', font = 'Times 12 bold')
        cIPDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cIPDataLabel) # self.dataLabelList Index 0
        cIPLabel.grid(row = 0, column = 0, sticky = "E")
        cIPDataLabel.grid(row = 0, column = 1, sticky = "W")

        cLocLabel = tk.Label(master = cDetailFrame, text = f'LOCATION:', font = 'Times 12 bold')
        cLocDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cLocDataLabel) # self.dataLabelList Index 1
        cLocLabel.grid(row = 1, column = 0, sticky = "E")
        cLocDataLabel.grid(row = 1, column = 1, sticky = "W")
        
        cMUILabel = tk.Label(master = cDetailFrame, text = f'MAIN USER INITALS:', font = 'Times 12 bold')
        cMUIDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cMUIDataLabel) # self.dataLabelList Index 2
        cMUILabel.grid(row = 2, column = 0, sticky = "E")
        cMUIDataLabel.grid(row = 2, column = 1, sticky = "W")

        cMULabel = tk.Label(master = cDetailFrame, text = f'MAIN USER:', font = 'Times 12 bold')
        cMUDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cMUDataLabel) # self.dataLabelList Index 3
        cMULabel.grid(row = 3, column = 0, sticky = "E")
        cMUDataLabel.grid(row = 3, column = 1, sticky = "W")

        cBuildLabel = tk.Label(master = cDetailFrame, text = f'BUILD:', font = 'Times 12 bold')
        cBuildDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cBuildDataLabel) # self.dataLabelList Index 4
        cBuildLabel.grid(row = 4, column = 0, sticky = "E")
        cBuildDataLabel.grid(row = 4, column = 1, sticky = "W")

        cTypeLabel = tk.Label(master = cDetailFrame, text = f'TYPE:', font = 'Times 12 bold')
        cTypeDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cTypeDataLabel) # self.dataLabelList Index 5
        cTypeLabel.grid(row = 5, column = 0, sticky = "E")
        cTypeDataLabel.grid(row = 5, column = 1, sticky = "W")

        cCostLabel = tk.Label(master = cDetailFrame, text = f'COST:', font = 'Times 12 bold')
        cCostDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cCostDataLabel) # self.dataLabelList Index 6
        cCostLabel.grid(row = 6, column = 0, sticky = "E")
        cCostDataLabel.grid(row = 6, column = 1, sticky = "W")

        cYearLabel = tk.Label(master = cDetailFrame, text = f'YEAR:', font = 'Times 12 bold')
        cYearDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cYearDataLabel) # self.dataLabelList Index 7
        cYearLabel.grid(row = 7, column = 0, sticky = "E")
        cYearDataLabel.grid(row = 7, column = 1, sticky = "W")

        cManuLabel = tk.Label(master = cDetailFrame, text = f'MANUFACTURER:', font = 'Times 12 bold')
        cManuDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cManuDataLabel) # self.dataLabelList Index 8
        cManuLabel.grid(row = 8, column = 0, sticky = "E")
        cManuDataLabel.grid(row = 8, column = 1, sticky = "W")

        cSoftwaresLabel = tk.Label(master = cDetailFrame, text = f'SOFTWARES:', font = 'Times 12 bold')
        cSoftwaresWinButton= ttk.Button(master = cDetailFrame, text = 'VIEW SOFTWARES PAGE', style = "M.TButton", command = lambda: self.jumpToSoftware())
        cSoftwaresLabel.grid(row = 9, column = 0, sticky = "E")
        cSoftwaresWinButton.grid(row = 9, column = 1, sticky = "W", padx = 1, pady = .5)

        cInternetLabel = tk.Label(master = cDetailFrame, text = f'INTERNET:', font = 'Times 12 bold')
        cInternetDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cInternetDataLabel) # self.dataLabelList Index 9
        cInternetLabel.grid(row = 10, column = 0, sticky = "E")
        cInternetDataLabel.grid(row = 10, column = 1, sticky = "W")

        cGPULabel = tk.Label(master = cDetailFrame, text = f'GPU:', font = 'Times 12 bold')
        cGPUDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cGPUDataLabel) # self.dataLabelList Index 10
        cGPULabel.grid(row = 11, column = 0, sticky = "E")
        cGPUDataLabel.grid(row = 11, column = 1, sticky = "W")
        
        cCPULabel = tk.Label(master = cDetailFrame, text = f'CPU:', font = 'Times 12 bold')
        cCPUDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cCPUDataLabel) # self.dataLabelList Index 11
        cCPULabel.grid(row = 12, column = 0, sticky = "E")
        cCPUDataLabel.grid(row = 12, column = 1, sticky = "W")
        
        cMoboLabel = tk.Label(master = cDetailFrame, text = f'MOTHERBOARD:', font = 'Times 12 bold')
        cMoboDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cMoboDataLabel) # self.dataLabelList Index 12
        cMoboLabel.grid(row = 13, column = 0, sticky = "E")
        cMoboDataLabel.grid(row = 13, column = 1, sticky = "W")
        
        cRAMLabel = tk.Label(master = cDetailFrame, text = f'RAM:', font = 'Times 12 bold')
        cRAMDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cRAMDataLabel) # self.dataLabelList Index 13
        cRAMLabel.grid(row = 14, column = 0, sticky = "E")
        cRAMDataLabel.grid(row = 14, column = 1, sticky = "W")
        
        cStorageLabel = tk.Label(master = cDetailFrame, text = f'STORAGE:', font = 'Times 12 bold')
        cStorageDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cStorageDataLabel) # self.dataLabelList Index 14
        cStorageLabel.grid(row = 15, column = 0, sticky = "E")
        cStorageDataLabel.grid(row = 15, column = 1, sticky = "W")
        
        cOSLabel = tk.Label(master = cDetailFrame, text = f'OPERATING SYSTEM:', font = 'Times 12 bold')
        cOSDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cOSDataLabel) # self.dataLabelList Index 15
        cOSLabel.grid(row = 16, column = 0, sticky = "E")
        cOSDataLabel.grid(row = 16, column = 1, sticky = "W")
        
        cLULabel = tk.Label(master = cDetailFrame, text = f'INFO LAST UPDATED:', font = 'Times 12 bold')
        cLUDataLabel = tk.Label(master = cDetailFrame, text = '--')
        self.dataLabelList.append(cLUDataLabel) # self.dataLabelList Index 16
        cLULabel.grid(row = 17, column = 0, sticky = "E")
        cLUDataLabel.grid(row = 17, column = 1, sticky = "W")

        # Place master detail frame
        cDetailFrame.grid(row = 3, column = 3, sticky = "NESW")

        # Below: All GUI Buttons, required to be at bottom for better program functionality.
        self.cAddPCButtn = tk.ttk.Button(master = self, text = "Add Computer", style = "M.TButton", command = lambda: self.addPC())
        self.cEditDetailButtn = tk.ttk.Button(master = self, text = "Edit Details", style = "M.TButton", state = 'disabled', command = lambda: self.editDetails(self.__currentlyViewing))
        self.cAddPCButtn.grid(row = 4, column = 2, padx = 1, pady = .5, sticky = "E")
        self.cEditDetailButtn.grid(row = 4, column = 3, sticky = 'W', padx = 1, pady = .5)

        # Key Binding Statements Below
        root.bind('<Return>', lambda x=None: self.returnPress())
        root.bind('<Up>', lambda x=None: self.arrowUp())
        root.bind('<Down>', lambda x=None: self.arrowDown())

        # Bind Listbox Selection
        self.__cpuListBox.bind('<<ListboxSelect>>', lambda x=None: self.listBoxUpdate())

        # Setup listbox, make active and apply default selection.
        self.__cpuListBox.config(takefocus = 0)

        # self.mainloop() -- Commented out to see if this would fix wait_window() calls by parent process, UDPATE: It worked.
        return