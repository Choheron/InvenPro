from datetime import datetime
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from .utils import settings as GLOBAL

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
    # CATEGORY LISTBOX SELECTION AND EDITING METHODS BELOW
    # ==============================
    def categoryBoxSelect(self):
        pass

    # ==============================
    # ITEM LISTBOX SELECTION AND EDITING METHODS BELOW
    # ==============================
    def itemBoxSelect(self):
        pass

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
        self.oCatListBox.bind('<<ListboxSelect>>', lambda x=None: self.categoryBoxSelect())
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
        self.addItemCatBttn = ttk.Button(master = oItemCatBttnFrame, text = "Add Category", style = "M.TButton", command = lambda: print("Add Item Category Button Pressed"))
        self.editItemCatBttn = ttk.Button(master = oItemCatBttnFrame, text = "Edit Category", style = "M.TButton", command = lambda: print("Edit Item Category Button Pressed"))
        self.delItemCatBttn = ttk.Button(master = oItemCatBttnFrame, text = "Delete Category", style = "M.TButton", command = lambda: print("Delete Item Category Button Pressed"))
        self.refreshItemCatBttn = ttk.Button(master = oItemCatBttnFrame, text = "Refresh List", style = "M.TButton", command = lambda: print("Refresh Lists Button Pressed"))
        self.addItemCatBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "E")
        self.editItemCatBttn.grid(row = 0, column = 1, padx = 1, pady = .5, sticky = "E")
        self.delItemCatBttn.grid(row = 0, column = 2, padx = 1, pady = .5, sticky = "E")
        self.refreshItemCatBttn.grid(row = 0, column = 3, padx = 1, pady = .5, sticky = "E")
        # Place Item Category button master frame
        oItemCatBttnFrame.grid(row = 2, column = 0, sticky = "NE")

        # Create Item button master frame
        oItemBttnFrame = tk.Frame(master = self)
        # Create and place item buttons
        self.addItemBttn = ttk.Button(master = oItemBttnFrame, text = "New Item")
        self.delItemBttn = ttk.Button(master = oItemBttnFrame, text = "Delete Item")
        self.addItemBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "E")
        self.delItemBttn.grid(row = 0, column = 1, padx = 1, pady = .5, sticky = "E")
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

        # Place master frame containing canvas and canvas scrollbar
        oDetailMaster.grid(row = 4, column = 0, columnspan = 2, sticky = "NESW")

        # Create and place edit details button
        self.editDetailsBttn = ttk.Button(master = self, text = "Edit Details", style = "M.TButton", command = lambda: print("Edit Details Button Pressed"))
        self.editDetailsBttn.grid(row = 5, column = 1, sticky = "E")
        # Disable edit and delete buttons until items or categories are selected
        self.editItemCatBttn.config(state = 'disabled')
        self.delItemCatBttn.config(state = 'disabled')
        self.delItemBttn.config(state = 'disabled')
        self.editDetailsBttn.config(state = 'disabled')
