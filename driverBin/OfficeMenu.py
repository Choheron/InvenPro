from datetime import datetime
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from .utils import settings as GLOBAL
from .toplevels.AddCategory import AddCategory
from .toplevels.AddItem import AddItem

class OfficeMenu(tk.Frame):
    DETAILFRAMECOL = 'gray70'

    def __init__(self, parent, root, pageDict):
        super().__init__(parent)
        self.parent = parent
        self.pageDict = pageDict
        # Configure Frame Weights
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.buildOfficeInventory(root)

    # ==============================
    # CATEGORY BUTTON METHODS BELOW
    # ==============================
    def addCategory(self):
        self.addCatBttn.config(state = 'disabled')
        catName = tk.StringVar(master = self, value = None)
        # Open the add category window
        addWindow = AddCategory(self, GLOBAL.officeDict, catName)
        # Await termination of the add category window
        self.wait_window(addWindow)
        # If no new category was added, return and do not change anything
        if((catName.get() == None) or (catName.get() == "None")):
            self.addCatBttn.config(state = 'normal')
            return
        # Return the add category button to normal state    
        self.addCatBttn.config(state = 'normal')
        # Set catName to None
        catName.set(None)
        # Save global software dict to system
        GLOBAL.saveOfficedict()
        # Refresh software list
        self.refreshList()
        return

    def delCategory(self):
        pass
    
    def refreshList(self):
        # Clear detail frame
        self.clearDetailFrame()
        # Disable all required buttons
        self.editCatBttn.config(state = 'disabled')
        self.delCatBttn.config(state = 'disabled')
        self.addItemBttn.config(state = 'disabled')
        self.editDetailsBttn.config(state = 'disabled')
        # Revert add item button text
        self.addItemBttn.config(text = 'New Item')
        # Clear item listbox
        self.oItemListBox.delete(0, tk.END)
        # Deactivate item listbox
        self.disableListbox(self.oItemListBox)
        # Clear category listbox
        self.oCatListBox.delete(0, tk.END)
        # Loop Through and populate category listbox
        for category in GLOBAL.officeDict:
            # Skip admin dict
            if(category == 'admin'):
                continue
            self.oCatListBox.insert(tk.END, category)

    # ==============================
    # ITEM BUTTON METHODS BELOW
    # ==============================
    def addItem(self):
        # Get current category
        selectedCat = str((self.oCatListBox.get(self.oCatListBox.curselection())))
        # Disable add item button
        self.addItemBttn.config(state = 'disabled')
        # Open add item window
        addWin = AddItem(self, GLOBAL.officeDict, selectedCat)
        # Await the termination of add window
        self.wait_window(addWin)

    def delItem(self):
        pass

    # ==============================
    # DETAIL FRAME METHODS BELOW
    # ==============================
    def clearDetailFrame(self):
        # Clear the detail frame of all widgets if need be
        for wid in self.detailFrame.winfo_children():
            wid.destroy()

    # ==============================
    # CATEGORY LISTBOX SELECTION AND EDITING METHODS BELOW
    # ==============================
    def catBoxSelect(self):
        # Check if listbox is empty, exit function if so
        if(self.oCatListBox.index(tk.END) == 0):
            return

        # Get the string value of the selected category
        selectedCat = str((self.oCatListBox.get(self.oCatListBox.curselection())))

        # Enable edit and delete category buttons
        self.editCatBttn.config(state = 'normal')
        self.delCatBttn.config(state = 'normal')
        self.addItemBttn.config(state = 'normal')
        # Change text on Add Item button
        self.addItemBttn.config(text = f"New {selectedCat}")
        # Activate the item listbox
        self.activateListbox(self.oItemListBox)
        # Clear the detail frame to make room for new widgets
        self.clearDetailFrame()
        # Configure detail frame label to include new instruction
        self.oDetailTitle.config(text = "Select an Item from the list to view details:")
        # Ensure the edit details button is disabled in order to make sure the user cannot cause error
        self.editDetailsBttn.config(state = 'disabled')

        # Activate the listbox if it is still disabled at call
        self.activateListbox(self.oItemListBox)
        # Clear list of any previous entries
        self.oItemListBox.delete(0, tk.END)

        # Create a local reference for easier understanding
        categoryDict = GLOBAL.officeDict[selectedCat]

        # Loop through items and populate list
        for item in categoryDict:
            # Skip template and admin dicts
            if((item == 'template') or (item == 'admin')):
                continue
            
            # Add item to list
            self.oItemListBox.insert(tk.END, item)

            # Color item based off of if it is currently in use or not
            if(categoryDict[item]['ACTIVE'] == "Y"):
                self.oItemListBox.itemconfig(tk.END, bg = 'yellow green')
            else:
                self.oItemListBox.itemconfig(tk.END, bg = 'indian red')


        pass

    # ==============================
    # ITEM LISTBOX SELECTION AND EDITING METHODS BELOW
    # ==============================

    def itemBoxSelect(self):
        # Check if listbox is empty, exit function if so
        if(self.oItemListBox.index(tk.END) == 0):
            return

        # Get current category and item
        selectedCat = str((self.oCatListBox.get(self.oCatListBox.curselection())))
        selectedItem = str((self.oItemListBox.get(self.oItemListBox.curselection())))

        # Clear detail frame to allow for clean slate
        self.clearDetailFrame()
        # Update label to show current information
        self.oDetailTitle.config(text = f'Displaying \"{selectedCat}\" information for \"{selectedItem}\":')

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
        for field in GLOBAL.officeDict[selectedCat]['template']:
            # Skip ID, as it is shown on the listbox
            if(field == 'ID'):
                continue
            # Create and place label for each field
            fieldLabel = tk.Label(master = self.detailFrame, text = f'{field}:', font = "Times 12 bold", bg = self.DETAILFRAMECOL)
            fieldLabel.grid(row = dRow, column = 0, sticky = "E")
            # Delcare placeholder for widget
            widget = None
            # Create checkbox or label based off of data type
            if((GLOBAL.officeDict[selectedCat][selectedItem][field] == "Y") or (GLOBAL.officeDict[selectedCat][selectedItem][field] == "N")):
                self.checkVars.insert(checkVarInt, tk.BooleanVar())
                widget = tk.Checkbutton(master = self.detailFrame, var = self.checkVars[checkVarInt], bg = self.DETAILFRAMECOL, disabledforeground = 'green')
                # Set checkbox status depending on variable
                if(GLOBAL.officeDict[selectedCat][selectedItem][field] == 'Y'):
                    self.checkVars[checkVarInt].set(True)
                else:
                    self.checkVars[checkVarInt].set(False)
                # Disable the checkbutton so the user cannot toggle it, then increment the checkbutton list
                widget.config(state = 'disabled')
                checkVarInt += 1
            else:
                widget = tk.Label(master = self.detailFrame, text = GLOBAL.officeDict[selectedCat][selectedItem][field], bg = self.DETAILFRAMECOL)
            # Place either checkbutton or label and increment row counter
            widget.grid(row = dRow, column = 1, sticky = 'EW')
            dRow += 1
        # Enable the edit detail button
        self.editDetailsBttn.config(state = 'normal')

    # "Activates"(Sets state to normal) the listbox passed in
    def activateListbox(self, listbox: tk.Listbox):
        listbox.config(state = 'normal')
        listbox.config(bg = 'white')

    # "Disables"(Sets state to disabled) the listbox passed in
    def disableListbox(self, listbox: tk.Listbox):
        listbox.config(state = 'disabled')
        listbox.config(bg = 'ivory4')
    
    # ==============================
    # BUILD METHOD BELOW
    # ==============================
    def buildOfficeInventory(self, root):
        # Create master directions frame
        oDirectionFrame = tk.Frame(master = self)
        # Create and place direction labels
        oMainDirections = tk.Label(master = oDirectionFrame, text = "Below is a list of all office inventory items, select one to expand the menus or add new ones using the buttons.")
        # TODO: Include more directions as well as last updated times
        oMainDirections.grid(row = 0, column = 0, sticky = "NESW")
        # Place master directions frame
        oDirectionFrame.grid(row = 0, column = 0, columnspan = 2, sticky = "NESW")

        # Create master frame for category listbox
        oCategoryMaster = tk.Frame(master = self)
        # Create category listbox
        self.oCatListBox = tk.Listbox(master = oCategoryMaster, width = 70, height = 20, selectmode = 'single', exportselection = False)
        # Populate category listbox
        for category in GLOBAL.officeDict:
            # Skip admin category
            if(category == 'admin'):
                continue
            self.oCatListBox.insert(tk.END, category)
        # Place category listbox
        self.oCatListBox.grid(row = 0, column = 0, sticky = "NESW")

        # Delcare scrollbar for the category listBox
        self.catListBoxScroll = tk.Scrollbar(master = oCategoryMaster)
        self.catListBoxScroll.grid(row = 0, column = 0, sticky = 'NSE')
        # Link software listbox and scrollbar
        self.oCatListBox.config(yscrollcommand = self.catListBoxScroll.set)
        self.catListBoxScroll.config(command = self.oCatListBox.yview)
        # Bind the update function to the selecting of an item in the software listbox
        self.oCatListBox.bind('<<ListboxSelect>>', lambda x=None: self.catBoxSelect())
        # Place category master frame
        oCategoryMaster.grid(row = 1, column = 0, sticky = "NESW")

        # Create master frame for item listbox
        oItemMaster = tk.Frame(master = self)
        # Create category listbox
        self.oItemListBox = tk.Listbox(master = oItemMaster, width = 70, height = 20, selectmode = 'single', exportselection = False)
        # Disable category listbox until something on the other listbox is selected
        self.oItemListBox.config(state = 'disabled')
        # Place category listbox
        self.oItemListBox.grid(row = 0, column = 0, sticky = "NESW")

        # Delcare scrollbar for the category listBox
        self.itemListBoxScroll = tk.Scrollbar(master = oItemMaster)
        self.itemListBoxScroll.grid(row = 0, column = 0, sticky = 'NSE')
        # Link software listbox and scrollbar
        self.oItemListBox.config(yscrollcommand = self.itemListBoxScroll.set)
        self.itemListBoxScroll.config(command = self.oItemListBox.yview)
        # Bind the update function to the selecting of an item in the software listbox
        self.oItemListBox.bind('<<ListboxSelect>>', lambda x=None: self.itemBoxSelect())
        # Place category master frame
        oItemMaster.grid(row = 1, column = 1, sticky = "NESW")

        # Create Item Category button master frame
        oItemCatBttnFrame = tk.Frame(master = self)
        # Create and place item category buttons
        self.addCatBttn = ttk.Button(master = oItemCatBttnFrame, text = "Add Category", style = "M.TButton", command = lambda: self.addCategory())
        self.editCatBttn = ttk.Button(master = oItemCatBttnFrame, text = "Edit Category", style = "M.TButton", command = lambda: print("Edit Item Category Button Pressed"))
        self.delCatBttn = ttk.Button(master = oItemCatBttnFrame, text = "Delete Category", style = "M.TButton", command = lambda: print("Delete Item Category Button Pressed"))
        self.refreshCatBttn = ttk.Button(master = oItemCatBttnFrame, text = "Refresh List", style = "M.TButton", command = lambda: self.refreshList())
        self.addCatBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "E")
        self.editCatBttn.grid(row = 0, column = 1, padx = 1, pady = .5, sticky = "E")
        self.delCatBttn.grid(row = 0, column = 2, padx = 1, pady = .5, sticky = "E")
        self.refreshCatBttn.grid(row = 0, column = 3, padx = 1, pady = .5, sticky = "E")
        # Place Item Category button master frame
        oItemCatBttnFrame.grid(row = 2, column = 0, sticky = "NE")

        # Create Item button master frame
        oItemBttnFrame = tk.Frame(master = self)
        # Create and place item buttons
        self.addItemBttn = ttk.Button(master = oItemBttnFrame, text = "New Item", style = "M.TButton", command = lambda: print("New Item Category Button Pressed"))
        self.addItemBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "E")
        # Place item button master frame
        oItemBttnFrame.grid(row = 2, column = 1, sticky = "NE")

        # Create detail label
        self.oDetailTitle = tk.Label(master = self, text = "Select a Category and an Item to see details in the window below:", font = ("Helvetica", "12", "italic"))
        self.oDetailTitle.grid(row = 3, column = 0, columnspan = 2, sticky = "W")

        # Create details master canvas frame
        oDetailMaster = tk.Frame(master = self)
        oDetailMaster.grid_columnconfigure(0, weight = 1)
        # Create detail canvas, required for scrollbar and procedural population to function as needed.
        self.detailCanvas = tk.Canvas(master = oDetailMaster, highlightthickness = 0, borderwidth = 0, bg = self.DETAILFRAMECOL)
        self.detailCanvas.grid(row = 0, column = 0, sticky = "NSEW")
        # Create frame for labels and text boxes
        self.detailFrame = tk.Frame(master = self.detailCanvas, bg = self.DETAILFRAMECOL)
        # Set weights of grid in frame
        self.detailFrame.grid_columnconfigure(0, weight = 1)
        self.detailFrame.grid_columnconfigure(1, weight = 1)
        # Attach frame to internals of center canvas
        self.windowID = self.detailCanvas.create_window((0, 0), window = self.detailFrame, anchor = 'n')

        # Create and place scrollbar for detail canvas
        self.detailScrollBar = tk.Scrollbar(master = oDetailMaster, orient = tk.VERTICAL, bd = 2, command = self.detailCanvas.yview)
        self.detailScrollBar.grid(row = 0, column = 0, sticky = "NSE")
        # Config scrollbar to have better relation to canvas in size
        self.detailCanvas.config(yscrollcommand = self.detailScrollBar.set)
        # Strange line of code, required for scrollbar to work, defines scrollable area
        self.detailFrame.bind('<Configure>', lambda event: self.detailCanvas.config(scrollregion = self.detailCanvas.bbox('all')))
        # Bind the detail display function to the selecting of an item in the item listbox
        self.oItemListBox.bind('<<ListboxSelect>>', lambda x=None: self.itemBoxSelect())

        # Place master frame containing canvas and canvas scrollbar
        oDetailMaster.grid(row = 4, column = 0, columnspan = 2, sticky = "NESW")
        

        # Create and place edit details button
        self.editDetailsBttn = ttk.Button(master = self, text = "Edit Details", style = "M.TButton", command = lambda: print("Edit Details Button Pressed"))
        self.editDetailsBttn.grid(row = 5, column = 1, sticky = "E")
        # Disable edit and delete buttons until items or categories are selected
        self.editCatBttn.config(state = 'disabled')
        self.delCatBttn.config(state = 'disabled')
        self.addItemBttn.config(state = 'disabled')
        self.editDetailsBttn.config(state = 'disabled')
        # Disable item listbox until a category is chosen
        self.disableListbox(self.oItemListBox)
