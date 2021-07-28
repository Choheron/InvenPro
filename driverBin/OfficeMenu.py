from datetime import datetime
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from .utils import settings as GLOBAL

class OfficeMenu(tk.Frame):
    def __init__(self, parent, root, pageDict):
        super().__init__(parent)
        self.parent = parent
        self.pageDict = pageDict
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
        self.oCatListBox = tk.Listbox(master = oCategoryMaster, width = 60, height = 20, selectmode = 'single', exportselection = False)
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
        self.oItemListBox = tk.Listbox(master = oItemMaster, width = 60, height = 20, selectmode = 'single', exportselection = False)
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

