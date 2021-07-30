from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from .utils import settings as GLOBAL
from .toplevels.AddCategory import AddCategory
from .toplevels.AddItem import AddItem
from .toplevels.EditItemDetails import EditItemDetails
from .toplevels.InputDialogue import InputDioBox

class FieldMenu(tk.Frame):
    DETAILFRAMECOL = 'gray70'

    def __init__(self, parent, root, pageDict):
        super().__init__(parent)
        self.parent = parent
        self.pageDict = pageDict
        # Configure Frame Weights
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.buildFieldInventory(root)

    # ==============================
    # CATEGORY BUTTON METHODS BELOW
    # ==============================

    # NOTE: Be sure to always save the dict globally BEFORE reloading or refreshing (this is due to the save order of the items)
    def addCategory(self):
        self.addCatBttn.config(state = 'disabled')
        catName = tk.StringVar(master = self, value = None)
        # Open the add category window
        addWindow = AddCategory(self, GLOBAL.fieldDict, catName)
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
        # Save global office dict to system
        GLOBAL.saveFielddict()
        # Refresh category list
        self.refreshList()
        return

    def delCategory(self):
        # Get currently selected category from category list
        category = str((self.fCatListBox.get(self.fCatListBox.curselection())))
        # Store result variable
        resultVar = tk.StringVar(master = self, value = "")
        # Write out message
        wMessage = "WARNING: Please note, deletion of a category is FINAL and will result in the loss of ALL associated data.\n\nIf you are SURE you would like to delete "
        wMessage += f"the category from the system, please type the category name as seen on screen and press submit.\nCategory: \"{category}\""
        # Delcare and wait for user input
        warningWin = InputDioBox(self, " Are you sure?", wMessage, resultVar)
        self.wait_window(warningWin)
        # Delete category from list if user input correctly
        if(resultVar.get() == category):
            # Delete category from dict
            del GLOBAL.fieldDict[category]
            # Save new dict to finalize deletion
            GLOBAL.saveFielddict()
            # Refresh listbox if a category was deleted
            self.refreshList()
            messagebox.showinfo(" Deletion successful", f"Successfully deleted {category} from the system... If this was a mistake you will need to re-add the category and re-enter all associated data.")
        else:
            messagebox.showinfo(" Deletion UNSUCESSFUL", f"IMPORTANT: {category} has NOT been deleted from the system.")
        
        return

    def editCategory(self):
        warnWindow = messagebox.showwarning(" Feature not yet implemented", "This feature has not yet been implemented, as InvenPro is a work is progress and may require revising and further expanding." +
                                                    "\nFor the time being, you can delete the previous category and readd a new one, just be sure to write down all the values!\nThank you for your patience.")
        return
    
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
        self.fItemListBox.delete(0, tk.END)
        # Deactivate item listbox
        self.disableListbox(self.fItemListBox)
        # Clear category listbox
        self.fCatListBox.delete(0, tk.END)
        # Reload field dict GLOBALLY
        GLOBAL.loadFielddict()
        # Loop Through and populate category listbox
        for category in GLOBAL.fieldDict:
            # Skip admin dict
            if(category == 'admin'):
                continue
            self.fCatListBox.insert(tk.END, category)
        self.updateTextLabel.config(text = f'{GLOBAL.fieldDict["admin"]["updated"]}')

    # ==============================
    # ITEM BUTTON METHODS BELOW
    # ==============================
    def addItem(self):
        # Get current category
        selectedCat = str((self.fCatListBox.get(self.fCatListBox.curselection())))
        # Disable add item button
        self.addItemBttn.config(state = 'disabled')
        # Open add item window
        addWin = AddItem(self, GLOBAL.fieldDict, selectedCat)
        # Await the termination of add window
        self.wait_window(addWin)
        # Save changes made by addItem window
        GLOBAL.saveFielddict()
        # Refresh lists
        self.refreshList()
        # Reactivate add Item button
        self.addItemBttn.config(state = 'normal')

    # ==============================
    # DETAIL FRAME METHODS BELOW
    # ==============================
    def clearDetailFrame(self):
        # Clear the detail frame of all widgets if need be
        for wid in self.detailFrame.winfo_children():
            wid.destroy()

    def editDetails(self):
        # Disable edit details button
        self.editDetailsBttn.config(state = 'disabled')
        # Get current category and item
        selectedCat = str((self.fCatListBox.get(self.fCatListBox.curselection())))
        selectedItem = str((self.fItemListBox.get(self.fItemListBox.curselection())))
        # Store currently selected values
        selectedCatIndex = self.fCatListBox.curselection()
        selectedItemIndex = self.fItemListBox.curselection()
        # Create edit details window
        editWin = EditItemDetails(self, GLOBAL.fieldDict, selectedCat, selectedItem)
        # Await termination of the window
        self.wait_window(editWin)
        # Reactivate edit details button
        self.editDetailsBttn.config(state = 'normal')
        # Save changes made
        GLOBAL.saveFielddict()
        # Refresh list
        self.refreshList()
        # Attempt to select the values again
        self.fCatListBox.selection_set(selectedCatIndex)
        self.fCatListBox.activate(selectedCatIndex)
        self.fItemListBox.selection_set(selectedItemIndex)
        self.fItemListBox.activate(selectedItemIndex)

    # ==============================
    # CATEGORY LISTBOX SELECTION AND EDITING METHODS BELOW
    # ==============================
    def catBoxSelect(self):
        # Check if listbox is empty, exit function if so
        if(self.fCatListBox.index(tk.END) == 0):
            return

        # Get the string value of the selected category
        selectedCat = str((self.fCatListBox.get(self.fCatListBox.curselection())))

        # Enable edit and delete category buttons
        self.editCatBttn.config(state = 'normal')
        self.delCatBttn.config(state = 'normal')
        self.addItemBttn.config(state = 'normal')
        # Change text on Add Item button
        self.addItemBttn.config(text = f"New {selectedCat}")
        # Activate the item listbox
        self.activateListbox(self.fItemListBox)
        # Clear the detail frame to make room for new widgets
        self.clearDetailFrame()
        # Configure detail frame label to include new instruction
        self.fDetailTitle.config(text = "Select an Item from the list to view details:")
        # Ensure the edit details button is disabled in order to make sure the user cannot cause error
        self.editDetailsBttn.config(state = 'disabled')

        # Activate the listbox if it is still disabled at call
        self.activateListbox(self.fItemListBox)
        # Clear list of any previous entries
        self.fItemListBox.delete(0, tk.END)

        # Create a local reference for easier understanding
        categoryDict = GLOBAL.fieldDict[selectedCat]

        # Loop through items and populate list
        for item in categoryDict:
            # Skip template and admin dicts
            if((item == 'template') or (item == 'admin')):
                continue
            
            # Add item to list
            self.fItemListBox.insert(tk.END, item)

            # Color item based off of if it is currently in use or not
            if(categoryDict[item]['ACTIVE'] == "Y"):
                self.fItemListBox.itemconfig(tk.END, bg = 'yellow green')
            else:
                self.fItemListBox.itemconfig(tk.END, bg = 'indian red')

    # ==============================
    # ITEM LISTBOX SELECTION AND EDITING METHODS BELOW
    # ==============================

    def itemBoxSelect(self):
        # Check if listbox is empty, exit function if so
        if(self.fItemListBox.index(tk.END) == 0):
            return

        # Get current category and item
        selectedCat = str((self.fCatListBox.get(self.fCatListBox.curselection())))
        selectedItem = str((self.fItemListBox.get(self.fItemListBox.curselection())))

        # Clear detail frame to allow for clean slate
        self.clearDetailFrame()
        # Update label to show current information
        self.fDetailTitle.config(text = f'Displaying \"{selectedCat}\" information for \"{selectedItem}\":')

        # Make columns have weight of 1 and minimum sizes to avoid ugly visual movement (NOTE: ALREADY DONE IN BUILDWINDOW)
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
        for field in GLOBAL.fieldDict[selectedCat]['template']:
            # Skip ID, as it is shown on the listbox
            if(field == 'ID'):
                continue
            # Create and place label for each field
            fieldLabel = tk.Label(master = self.detailFrame, text = f'{field}:', font = "Times 12 bold", bg = self.DETAILFRAMECOL)
            fieldLabel.grid(row = dRow, column = 0, sticky = "E")
            # Delcare placeholder for widget
            widget = None
            # Create checkbox or label based off of data type
            if((GLOBAL.fieldDict[selectedCat][selectedItem][field] == "Y") or (GLOBAL.fieldDict[selectedCat][selectedItem][field] == "N")):
                self.checkVars.insert(checkVarInt, tk.BooleanVar())
                widget = tk.Checkbutton(master = self.detailFrame, var = self.checkVars[checkVarInt], bg = self.DETAILFRAMECOL, disabledforeground = 'green')
                # Set checkbox status depending on variable
                if(GLOBAL.fieldDict[selectedCat][selectedItem][field] == 'Y'):
                    self.checkVars[checkVarInt].set(True)
                else:
                    self.checkVars[checkVarInt].set(False)
                # Disable the checkbutton so the user cannot toggle it, then increment the checkbutton list
                widget.config(state = 'disabled')
                checkVarInt += 1
            else:
                widget = tk.Label(master = self.detailFrame, text = GLOBAL.fieldDict[selectedCat][selectedItem][field], bg = self.DETAILFRAMECOL)
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
    def buildFieldInventory(self, root):
        # Create master directions frame
        fDirectionFrame = tk.Frame(master = self)
        # Create and place direction labels
        fMainDirections = tk.Label(master = fDirectionFrame, text = "Below is a list of all FIELD inventory items, select one to expand the menus or add new ones using the buttons.")
        upTextLabel = tk.Label(master = fDirectionFrame, text = "Field Category List Last Updated:")
        self.updateTextLabel = tk.Label(master = fDirectionFrame, text = f'{GLOBAL.fieldDict["admin"]["updated"]}')
        fMainDirections.grid(row = 0, column = 0, columnspan = 2, sticky = "NESW")
        upTextLabel.grid(row = 1, column = 0, sticky = "E")
        self.updateTextLabel.grid(row = 1, column = 1, sticky = "W")
        # Place master directions frame
        fDirectionFrame.grid(row = 0, column = 0, columnspan = 2)

        # Create master frame for category listbox
        fCategoryMaster = tk.Frame(master = self)
        # Create category listbox
        self.fCatListBox = tk.Listbox(master = fCategoryMaster, width = 70, height = 20, selectmode = 'single', exportselection = False)
        # Populate category listbox
        for category in GLOBAL.fieldDict:
            # Skip admin category
            if(category == 'admin'):
                continue
            self.fCatListBox.insert(tk.END, category)
        # Place category listbox
        self.fCatListBox.grid(row = 0, column = 0, sticky = "NESW")

        # Delcare scrollbar for the category listBox
        self.catListBoxScroll = tk.Scrollbar(master = fCategoryMaster)
        self.catListBoxScroll.grid(row = 0, column = 0, sticky = 'NSE')
        # Link software listbox and scrollbar
        self.fCatListBox.config(yscrollcommand = self.catListBoxScroll.set)
        self.catListBoxScroll.config(command = self.fCatListBox.yview)
        # Bind the update function to the selecting of an item in the software listbox
        self.fCatListBox.bind('<<ListboxSelect>>', lambda x=None: self.catBoxSelect())
        # Place category master frame
        fCategoryMaster.grid(row = 1, column = 0, sticky = "NESW")

        # Create master frame for item listbox
        fItemMaster = tk.Frame(master = self)
        # Create category listbox
        self.fItemListBox = tk.Listbox(master = fItemMaster, width = 70, height = 20, selectmode = 'single', exportselection = False)
        # Disable category listbox until something on the other listbox is selected
        self.fItemListBox.config(state = 'disabled')
        # Place category listbox
        self.fItemListBox.grid(row = 0, column = 0, sticky = "NESW")

        # Delcare scrollbar for the category listBox
        self.itemListBoxScroll = tk.Scrollbar(master = fItemMaster)
        self.itemListBoxScroll.grid(row = 0, column = 0, sticky = 'NSE')
        # Link software listbox and scrollbar
        self.fItemListBox.config(yscrollcommand = self.itemListBoxScroll.set)
        self.itemListBoxScroll.config(command = self.fItemListBox.yview)
        # Bind the update function to the selecting of an item in the software listbox
        self.fItemListBox.bind('<<ListboxSelect>>', lambda x=None: self.itemBoxSelect())
        # Place category master frame
        fItemMaster.grid(row = 1, column = 1, sticky = "NESW")

        # Create Item Category button master frame
        fItemCatBttnFrame = tk.Frame(master = self)
        # Create and place item category buttons
        self.addCatBttn = ttk.Button(master = fItemCatBttnFrame, text = "Add Category", style = "M.TButton", command = lambda: self.addCategory())
        self.editCatBttn = ttk.Button(master = fItemCatBttnFrame, text = "Edit Category", style = "M.TButton", command = lambda: self.editCategory())
        self.delCatBttn = ttk.Button(master = fItemCatBttnFrame, text = "Delete Category", style = "M.TButton", command = lambda: self.delCategory())
        self.refreshCatBttn = ttk.Button(master = fItemCatBttnFrame, text = "Refresh List", style = "M.TButton", command = lambda: self.refreshList())
        self.addCatBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "E")
        self.editCatBttn.grid(row = 0, column = 1, padx = 1, pady = .5, sticky = "E")
        self.delCatBttn.grid(row = 0, column = 2, padx = 1, pady = .5, sticky = "E")
        self.refreshCatBttn.grid(row = 0, column = 3, padx = 1, pady = .5, sticky = "E")
        # Place Item Category button master frame
        fItemCatBttnFrame.grid(row = 2, column = 0, sticky = "NE")

        # Create Item button master frame
        fItemBttnFrame = tk.Frame(master = self)
        # Create and place item buttons
        self.addItemBttn = ttk.Button(master = fItemBttnFrame, text = "New Item", style = "M.TButton", command = lambda: self.addItem())
        self.addItemBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "E")
        # Place item button master frame
        fItemBttnFrame.grid(row = 2, column = 1, sticky = "NE")

        # Create detail label
        self.fDetailTitle = tk.Label(master = self, text = "Select a Category and an Item to see details in the window below:", font = ("Helvetica", "12", "italic"))
        self.fDetailTitle.grid(row = 3, column = 0, columnspan = 2, sticky = "W")

        # Create details master canvas frame
        fDetailMaster = tk.Frame(master = self, borderwidth = 2, bg = self.DETAILFRAMECOL, relief = 'sunken')
        fDetailMaster.grid_columnconfigure(0, weight = 1)
        # Create detail canvas, required for scrollbar and procedural population to function as needed.
        self.detailCanvas = tk.Canvas(master = fDetailMaster, highlightthickness = 0, borderwidth = 0, bg = self.DETAILFRAMECOL)
        self.detailCanvas.grid(row = 0, column = 0, sticky = "NSEW")
        # Create frame for labels and text boxes
        self.detailFrame = tk.Frame(master = self.detailCanvas, bg = self.DETAILFRAMECOL)
        # Set weights of grid in frame
        self.detailFrame.grid_columnconfigure(0, weight = 1)
        self.detailFrame.grid_columnconfigure(1, weight = 1)
        # Set minsizes of grid in frame
        self.detailFrame.grid_columnconfigure(0, minsize = 200)
        self.detailFrame.grid_columnconfigure(1, minsize = 200)
        # Attach frame to internals of center canvas
        self.windowID = self.detailCanvas.create_window((0, 0), window = self.detailFrame, anchor = 'n')

        # Create and place scrollbar for detail canvas
        self.detailScrollBar = tk.Scrollbar(master = fDetailMaster, orient = tk.VERTICAL, bd = 2, command = self.detailCanvas.yview)
        self.detailScrollBar.grid(row = 0, column = 0, sticky = "NSE")
        # Config scrollbar to have better relation to canvas in size
        self.detailCanvas.config(yscrollcommand = self.detailScrollBar.set)
        # Strange line of code, required for scrollbar to work, defines scrollable area
        self.detailFrame.bind('<Configure>', lambda event: self.detailCanvas.config(scrollregion = self.detailCanvas.bbox('all')))
        # Bind the detail display function to the selecting of an item in the item listbox
        self.fItemListBox.bind('<<ListboxSelect>>', lambda x=None: self.itemBoxSelect())

        # Place master frame containing canvas and canvas scrollbar
        fDetailMaster.grid(row = 4, column = 0, columnspan = 2, sticky = "NESW")
        

        # Create and place edit details button
        self.editDetailsBttn = ttk.Button(master = self, text = "Edit Details", style = "M.TButton", command = lambda: self.editDetails())
        self.editDetailsBttn.grid(row = 5, column = 1, sticky = "E")
        # Disable edit and delete buttons until items or categories are selected
        self.editCatBttn.config(state = 'disabled')
        self.delCatBttn.config(state = 'disabled')
        self.addItemBttn.config(state = 'disabled')
        self.editDetailsBttn.config(state = 'disabled')
        # Disable item listbox until a category is chosen
        self.disableListbox(self.fItemListBox)