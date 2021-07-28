import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
# ==============================
# Inital code duplicated from AddSoftware.py window
# ==============================
class AddCategory(tk.Toplevel):
    def __init__(self, master, officeDict, catName):
        super().__init__(master)
        self.parent = master
        self.officeDict = officeDict
        self.catName = catName
        self.grab_set()
        self.buildWindow()

    # ==============================
    # TEXT BOX INTERRUPT METHOD BELOW
    # ==============================
    def ignoreInput(self):
        # Break the input and ignore input as a whole
        return 'break'

    # ==============================
    # DELETE ATTRIBUTES METHOD BELOW
    # ==============================
    def deleteAttribute(self, num):
        # Destroy the three widgets contained in dictionary
        self.widgetDict[f'Attr{num}']['Label'].destroy()
        self.widgetDict[f'Attr{num}']['Widget'].destroy()
        self.widgetDict[f'Attr{num}']['DelBttn'].destroy()
        # Delete dictionary
        del self.widgetDict[f'Attr{num}']
        # Update preview window
        self.updatePreview()

    # ==============================
    # ADD ATTRIBUTES METHODS BELOW
    # ==============================
    def addTextAttr(self):
        # Create Attribute label and text entry and configure dictionary
        attributeNum = self.widgetDict['count']
        self.widgetDict[f'Attr{attributeNum}'] = {}
        self.widgetDict[f'Attr{attributeNum}']['Label'] = tk.Label(master = self.attrFrame, text = f"Text Attribute:")
        self.widgetDict[f'Attr{attributeNum}']['Widget'] = tk.Text(master = self.attrFrame, height = 1, width = 30)
        self.widgetDict[f'Attr{attributeNum}']['Widget'].insert(tk.END, f"Attribute Name")
        self.widgetDict[f'Attr{attributeNum}']['Type'] = 'Text'
        self.widgetDict[f'Attr{attributeNum}']['Index'] = self.widgetDict['count']
        # Place Attribute label and text entry
        self.widgetDict[f'Attr{attributeNum}']['Label'].grid(row = self.widgetDict[f'Attr{attributeNum}']['Index'], column = 0, sticky = "NESW")
        self.widgetDict[f'Attr{attributeNum}']['Widget'].grid(row = self.widgetDict[f'Attr{attributeNum}']['Index'], column = 1, sticky = "W")
        # Create and place delete button
        self.widgetDict[f'Attr{attributeNum}']['DelBttn'] = ttk.Button(master = self.attrFrame, text = "X", style = "M.TButton", command = lambda: self.deleteAttribute(self.widgetDict[f'Attr{attributeNum}']['Index']))
        self.widgetDict[f'Attr{attributeNum}']['DelBttn'].grid(row = self.widgetDict[f'Attr{attributeNum}']['Index'], column = 3)

        # Bind enter key to deselect the textbox
        self.widgetDict[f'Attr{attributeNum}']['Widget'].bind("<Return>", lambda x=None: self.ignoreInput())
        self.widgetDict[f'Attr{attributeNum}']['Widget'].bind("<Tab>", lambda x=None: self.ignoreInput())

        # Increment widget count
        self.widgetDict['count'] += 1
        # Update preview window
        self.updatePreview()

    def addTFAttr(self):
        # Create Attribute label and text entry and configure dictionary
        attributeNum = self.widgetDict['count']
        self.widgetDict[f'Attr{attributeNum}'] = {}
        self.widgetDict[f'Attr{attributeNum}']['Label'] = tk.Label(master = self.attrFrame, text = f"True/False Attribute:")
        self.widgetDict[f'Attr{attributeNum}']['Widget'] = tk.Text(master = self.attrFrame, height = 1, width = 30)
        self.widgetDict[f'Attr{attributeNum}']['Widget'].insert(tk.END, f"Attribute Name")
        self.widgetDict[f'Attr{attributeNum}']['Type'] = 'Checkbox'
        self.widgetDict[f'Attr{attributeNum}']['Index'] = self.widgetDict['count']
        # Place Install label and text entry
        self.widgetDict[f'Attr{attributeNum}']['Label'].grid(row = self.widgetDict[f'Attr{attributeNum}']['Index'], column = 0, sticky = "NESW")
        self.widgetDict[f'Attr{attributeNum}']['Widget'].grid(row = self.widgetDict[f'Attr{attributeNum}']['Index'], column = 1, sticky = "W")
        # Create and place delete button
        self.widgetDict[f'Attr{attributeNum}']['DelBttn'] = ttk.Button(master = self.attrFrame, text = "X", style = "M.TButton", command = lambda: self.deleteAttribute(self.widgetDict[f'Attr{attributeNum}']['Index']))
        self.widgetDict[f'Attr{attributeNum}']['DelBttn'].grid(row = self.widgetDict[f'Attr{attributeNum}']['Index'], column = 3)

        # Bind enter key to deselect the textbox
        self.widgetDict[f'Attr{attributeNum}']['Widget'].bind("<Return>", lambda x=None: self.ignoreInput())
        self.widgetDict[f'Attr{attributeNum}']['Widget'].bind("<Tab>", lambda x=None: self.ignoreInput())

        # Increment widget count
        self.widgetDict['count'] += 1
        # Update preview window
        self.updatePreview()

    # ==============================
    # UPDATE PREVIEW METHODS BELOW
    # ==============================
    def updatePreview(self):
        # Clear frame of previous widgets (to ensure a clean slate)
        for widget in self.previewFrame.winfo_children():
            widget.destroy()

        # Create and place an example Item in the preview frame
        tk.Label(master = self.previewFrame, text = (self.widgetDict['Name']['Widget'].get("1.0", 'end-1c')), bg = 'gray55', borderwidth = 1, relief = 'solid').grid(row = 0, column = 0, sticky = 'NESW')
        tk.Label(master = self.previewFrame, text = "MASLD-XX-XXX", font = ("Helvetica", "10", "italic"), bg = 'gray70').grid(row = 1, column = 0, sticky = 'NESW')
        # Loop through and place widgets on preview frame
        currCol = 1
        for widget in self.widgetDict:
            if((widget == 'count') or (widget == 'Name') or (widget == 'Nickname')): # Skip counting widget, name widget, and nickname widget
                continue
            tk.Label(master = self.previewFrame, text = self.widgetDict[widget]['Widget'].get("1.0", 'end-1c'), bg = 'gray55', borderwidth = 1, relief = 'solid').grid(row = 0, column = currCol, sticky = 'NESW')
            if(self.widgetDict[widget]['Type'] == 'Text'):
                tk.Label(master = self.previewFrame, text = "Example Text", font = ("Helvetica", "10", "italic"), bg = 'gray70').grid(row = 1, column = currCol, sticky = 'NESW')
            elif(self.widgetDict[widget]['Type'] == 'Checkbox'):
                tk.Checkbutton(master = self.previewFrame, var = False, fg = 'green', bg = 'gray70').grid(row = 1, column = currCol, sticky = 'NESW')
            else:
                print("SOMEHOW REACHED UNREACHABLE ERROR IN: (AddCategory.py function updatePreview)")
                tk.messagebox.showerror(" ERROR", "SOMEHOW REACHED UNREACHABLE ERROR IN: (AddCategory.py function updatePreview)")
                return
            currCol += 1

    # ==============================
    # TERMINATE METHOD BELOW
    # ==============================
    def terminate(self):
        response = tk.messagebox.askokcancel(parent = self, title = " Are you sure?", message = "Current Category addition will be lost.\nAre you sure you want to cancel?")
        if(response):
            self.catName.set(None)
            self.grab_release()
            self.destroy()
        else:
            return
    
    # ==============================
    # INPUT CHECKING METHODS BELOW
    # ==============================
    def checkInput(self, string):
        if(string == ''): # Check for empty string
            return 'ERROR - All attributes must have names.'
        elif(string == 'Attribute Name'): # Check for unchanged attribute names
            return 'ERROR - You must change all default attribute names.'
        elif(string == 'Category Name'): # Check for unchanged softare name
            return 'ERROR - You must give the category a name.'
        elif('ERROR' in string.upper()): # Check to make sure no inputs contain 'ERROR'
            return 'ERROR - The following string: \"ERROR\" is prohibited in any string values.'
        return string
    
    def checkNickname(self, string):
        if(string == ''):
            return 'ERROR - You must provide a Nickname.'
        elif(string == 'XXX'):
            return 'ERROR - You must change Nickname from default value.'
        elif(len(string) >= 4):
            return 'ERROR - Nickname must be at MAX 3 characters long.'
        for category in self.officeDict:
            if(category == 'admin'):
                continue
            if(self.officeDict[category]['admin']['nickname'] == string):
                return f'ERROR - Nickname is already taken by category: \"{category}\"'
        return string

    # ==============================
    # ADD CATEGORY METHOD BELOW (Terminates at end)
    # ==============================
    def addCategory(self):
        newCatDict = {}
        # Check category name input
        name = self.checkInput(self.widgetDict['Name']['Widget'].get('1.0', 'end-1c'))
        # Show error if needed
        if('ERROR' in name):
            tk.messagebox.showerror(" Category Addition Error", f'The category could not be added. Error contained the following message for debug:\n{name}')
            return

        # Declare template to show what fields are strings and what are T/F values
        newCatDict['template'] = {} 
        for attr in self.widgetDict:
            # Skip unimportant/un-needed fields
            if((attr == 'count') or (attr == 'Name') or (attr == "Nickname")):
                continue
            attribute = self.checkInput(self.widgetDict[attr]['Widget'].get('1.0', 'end-1c'))
            # Show error if the checkinput returned a failed input
            if('ERROR' in attribute):
                tk.messagebox.showerror(" Category Addition Error", f'The category could not be added. Error contained the following message for debug:\n{attribute}')
                return
            # Check if attribute is already in the system.
            if(attribute.upper() in newCatDict['template']):
                tk.messagebox.showerror(" Category Addition Error", f'The category could not be added due to a duplicate attribute name ({attribute.upper()}).\nCategory addition has been canceled.')
                return
            # Add field to template and give value based off of type of field
            if(self.widgetDict[attr]['Type'] == 'Checkbox'):
                newCatDict['template'][(self.widgetDict[attr]['Widget'].get('1.0', 'end-1c')).upper()] = "N"
            else:
                newCatDict['template'][(self.widgetDict[attr]['Widget'].get('1.0', 'end-1c')).upper()] = "--"
        # Append log to the template dict of each new category
        newCatDict['template']['LOG'] = ""

        # Give dictionary an admin dict
        newCatDict['admin'] = {}
        # Check nickname to ensure it works
        nickName = (self.checkNickname(self.widgetDict['Nickname']['Widget'][1].get('1.0', 'end-1c')))
        if('ERROR' in nickName):
            tk.messagebox.showerror(" Category Addition Error", f'The input nickname is not valid. Error contained the following message for debug:\n{nickName}')
            return
        # Store nickname in admin dict
        newCatDict['admin']['nickname'] = nickName
        # Add the category to the master category dictionary
        self.officeDict[name] = newCatDict
        self.catName.set(name)
        

        # Close window after releasing focus
        self.grab_release()
        self.destroy()

    # ==============================
    # BUILD WINDOW METHOD
    # ==============================
    def buildWindow(self):
        self.title(" Add New Item Category")

        # Create direction master frame
        dirFrame = tk.Frame(master = self, bg = 'grey')
        # Create and place direction labels
        dirLabel1 = tk.Label(master = dirFrame, text = "Fill out information to add a new Category of Item.", font = 'Times 20 bold', bg = 'grey')
        dirLabel2 = tk.Label(master = dirFrame, text = "Use the buttons at the bottom of the window to add new fields.\nThe example window at the bottom will reflect your current setup.", bg = 'grey')
        dirLabel1.grid(row = 0, column = 0, sticky = "EW")
        dirLabel2.grid(row = 1, column = 0, sticky = "EW")
        # Place direction master frame
        dirFrame.grid(row = 0, column = 0, sticky = "NESW")

        # Create frame to place attribute canvas and scrollbar in, trying to maintain visual border -- FIRST MASTER CANVAS FRAME
        attributeCanvasFrame = tk.Frame(master = self, borderwidth = 2, relief = 'sunken')
        attributeCanvasFrame.grid_columnconfigure(0, weight = 1)

        # Create and place Canvas for the attributes to be added
        self.attrCanvas = tk.Canvas(master = attributeCanvasFrame, highlightthickness = 0, borderwidth = 0)
        self.attrCanvas.grid(row = 0, column = 0, sticky = "NSEW")
        # Create internal frame for all of the attributes
        self.attrFrame = tk.Frame(master = self.attrCanvas)
        # Set weights of grid in frame
        self.attrFrame.grid_columnconfigure(0, weight = 1)
        self.attrFrame.grid_columnconfigure(1, weight = 1)
        # Attach frame to internals of center canvas
        self.windowID = self.attrCanvas.create_window((0, 0), window = self.attrFrame, anchor = 'n')

        # Create and place scrollbar for attribute canvas
        self.attrScrollBar = tk.Scrollbar(master = attributeCanvasFrame, orient = tk.VERTICAL, bd = 2, command = self.attrCanvas.yview)
        self.attrScrollBar.grid(row = 0, column = 0, sticky = "NES")
        # Config scrollbar to have better relation to canvas in size
        self.attrCanvas.config(yscrollcommand = self.attrScrollBar.set)
        # Define scrollable area
        self.attrFrame.bind('<Configure>', lambda event: self.attrCanvas.config(scrollregion = self.attrCanvas.bbox('all')))

        # Place the attribute master frame
        attributeCanvasFrame.grid(row = 1, column = 0, sticky = "NESW")

        # Declare Widget Dict
        self.widgetDict = {}
        self.widgetDict['count'] = 0

        # Declare category Data and configure widgetDict
        self.widgetDict['Name'] = {}
        self.widgetDict['Name']['Label'] = tk.Label(master = self.attrFrame, text = "Category Name:")
        self.widgetDict['Name']['Widget'] = tk.Text(master = self.attrFrame, height = 1, width = 30)
        self.widgetDict['Name']['Widget'].insert(tk.END, "Category Name")
        self.widgetDict['Name']['Type'] = 'Text'
        self.widgetDict['Name']['Index'] = self.widgetDict['count']
        # Bind enter key to deselect the textbox
        self.widgetDict['Name']['Widget'].bind("<Return>", lambda x=None: self.ignoreInput())
        self.widgetDict['Name']['Widget'].bind("<Tab>", lambda x=None: self.ignoreInput())
        # Increment widget count
        self.widgetDict['count'] += 1
        # Place category Data
        self.widgetDict['Name']['Label'].grid(row = self.widgetDict['Name']['Index'], column = 0, sticky = "NESW")
        self.widgetDict['Name']['Widget'].grid(row = self.widgetDict['Name']['Index'], column = 1, sticky = "W")

        # Declare Identifier label and text entry and place them in widgetDict
        self.widgetDict['Nickname'] = {}
        self.widgetDict['Nickname']['Label'] = tk.Label(master = self.attrFrame, text = "Category Nickname:")
        self.widgetDict['Nickname']['Widget'] = []
        # Create special widget frame for nickname
        nickFrame = tk.Frame(master = self.attrFrame)
        # Populate list with two labels and a text widget to allow for nickname setting
        self.widgetDict['Nickname']['Widget'].append(tk.Label(master = nickFrame, text = "MASLD-"))
        self.widgetDict['Nickname']['Widget'].append(tk.Text(master = nickFrame, height = 1, width = 3))
        self.widgetDict['Nickname']['Widget'].append(tk.Label(master = nickFrame, text = "-001"))
        # Insert Text into nickname textbox
        self.widgetDict['Nickname']['Widget'][1].insert(tk.END, "XXX")
        self.widgetDict['Nickname']['Type'] = 'Text'
        self.widgetDict['Nickname']['Index'] = self.widgetDict['count']
        # Populate widget frame with widgets
        self.widgetDict['Nickname']['Widget'][0].grid(row = 0, column = 0, sticky = "E")
        self.widgetDict['Nickname']['Widget'][1].grid(row = 0, column = 1, sticky = "NESW")
        self.widgetDict['Nickname']['Widget'][2].grid(row = 0, column = 2, sticky = "W")
        # Bind enter key to deselect the textbox
        self.widgetDict[f'Nickname']['Widget'][1].bind("<Return>", lambda x=None: self.ignoreInput())
        self.widgetDict[f'Nickname']['Widget'][1].bind("<Tab>", lambda x=None: self.ignoreInput())
        # Increment widget count
        self.widgetDict['count'] += 1
        # Place nickname Data
        self.widgetDict['Nickname']['Label'].grid(row = self.widgetDict['Nickname']['Index'], column = 0, sticky = "NESW")
        nickFrame.grid(row = self.widgetDict['Nickname']['Index'], column = 1, sticky = "W")

        # Declare Location label and text entry and place them in widgetDict
        self.widgetDict['Attr2'] = {}
        self.widgetDict['Attr2']['Label'] = tk.Label(master = self.attrFrame, text = "Required Attribute:")
        self.widgetDict['Attr2']['Widget'] = tk.Text(master = self.attrFrame, height = 1, width = 30)
        self.widgetDict['Attr2']['Widget'].insert(tk.END, "Location")
        self.widgetDict['Attr2']['Widget'].config(state = 'disabled')
        self.widgetDict['Attr2']['Type'] = 'Text'
        self.widgetDict['Attr2']['Index'] = self.widgetDict['count']
        # Place Location label and text entry
        self.widgetDict['Attr2']['Label'].grid(row = self.widgetDict['Attr2']['Index'], column = 0, sticky = "E")
        self.widgetDict['Attr2']['Widget'].grid(row = self.widgetDict['Attr2']['Index'], column = 1, sticky = "W")
        # Increment widget count
        self.widgetDict['count'] += 1

        # Create master button frame -- BUTTON MASTER FRAME
        bttnFrame = tk.Frame(master = self)
        # Fix weights on button frame columns
        bttnFrame.grid_columnconfigure(0, weight = 1)
        bttnFrame.grid_columnconfigure(1, minsize = 160) # For empty space management
        bttnFrame.grid_columnconfigure(2, weight = 1)
        # Create second button frame, strictly for spacing reasons
        bttnFrame2 = tk.Frame(master = bttnFrame)
        # Create and place buttons in frame
        self.previewBttn = ttk.Button(master = bttnFrame, text = "Update Preview", style = "M.TButton", command = lambda: self.updatePreview())
        self.addTextBttn = ttk.Button(master = bttnFrame2, text = "Add Text Attribute", style = "M.TButton", command = lambda: self.addTextAttr())
        self.addTFBttn = ttk.Button(master = bttnFrame2, text = "Add True/False Attribute", style = "M.TButton", command = lambda: self.addTFAttr())
        self.previewBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "W")
        self.addTextBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "E")
        self.addTFBttn.grid(row = 0, column = 1, padx = 1, pady = .5, sticky = "E")
        # Place internal second button frame
        bttnFrame2.grid(row = 0, column = 2, sticky = "NESW")
        # Place master button frame
        bttnFrame.grid(row = 2, column = 0, sticky = "NESW")

        # Create and place preview label
        previewLabel = tk.Label(master = self, text = "Preview:")
        previewLabel.grid(row = 3, column = 0, sticky = "W")

        # Create master frame for preview -- SECOND MASTER CANVAS FRAME
        previewMasterFrame = tk.Frame(master = self, borderwidth = 2, relief = 'sunken')
        # Configure preview frame column
        previewMasterFrame.grid_columnconfigure(0, weight = 1)

        # Create and place Canvas for the preview to be displayed
        self.prevCanvas = tk.Canvas(master = previewMasterFrame, height = 75, highlightthickness = 0, borderwidth = 0, bg = 'gray70')
        self.prevCanvas.grid(row = 0, column = 0, sticky = "NSEW")
        # Create internal frame for preview contents
        self.previewFrame = tk.Frame(master = self.prevCanvas, bg = 'gray70')
        # Set weights of grid in frame
        for number in range (0, 50):
            self.previewFrame.grid_columnconfigure(number, weight = 1)
        # Attach frame to internals of center canvas
        self.prevCanvasFrame = self.prevCanvas.create_window((0, 0), window = self.previewFrame, anchor = 'center')

        # Create and place scrollbar for preivew canvas
        self.prevScrollBar = tk.Scrollbar(master = previewMasterFrame, orient = tk.HORIZONTAL, bd = 2, command = self.prevCanvas.xview)
        self.prevScrollBar.grid(row = 0, column = 0, sticky = "ESW")
        # Config scrollbar to have better relation to canvas in size
        self.prevCanvas.config(xscrollcommand = self.prevScrollBar.set)
        # Define scrollable area
        self.previewFrame.bind('<Configure>', lambda event: self.prevCanvas.config(scrollregion = self.prevCanvas.bbox('all')))

        # Place preview master frame
        previewMasterFrame.grid(row = 4, column = 0, sticky = "NESW")

        # Update the preview canvas after loading all required elements
        self.updatePreview()

        # Create bottom button master frame
        bottomButtons = tk.Frame(master = self)
        # Declare and place save and cancel button
        self.saveBttn = ttk.Button(master = bottomButtons, text = "Save New Category", style = "M.TButton", command = lambda: self.addCategory())
        self.cancelBttn = ttk.Button(master = bottomButtons, text = "Cancel", style = "M.TButton",  command = lambda: self.terminate())
        self.saveBttn.grid(row = 0, column = 0, padx = 1, pady = .5, sticky = "E")
        self.cancelBttn.grid(row = 0, column = 1, padx = 1, pady = .5, sticky = "E")
        # Place bottom button master frame
        bottomButtons.grid(row = 5, column = 0, sticky = "E")

        # Intercept close button
        self.protocol("WM_DELETE_WINDOW", lambda: self.terminate())

        # Disable resizing
        self.resizable(0, 0)

        return