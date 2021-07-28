import tkinter as tk
import webbrowser
import os

# TODO: Make much more beautiful and make to include dynamic version information and the like.

class AboutPopup(tk.Toplevel):
    PROGRAMNAME = "InvenPro"
    bgCol = 'grey70'

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grab_set()
        self.buildAbout()

    # Function to call the default webbrowser to open the url passed in
    def callback(self, url):
        webbrowser.open_new(url)

    # ==============================
    # TERMINATE METHOD BELOW
    # ==============================
    def terminate(self):
        self.grab_release()
        self.destroy()

    # ==============================
    # BUILD METHOD BELOW
    # ==============================

    # Builds the page and sets it to be unresizeable
    def buildAbout(self):
        # Set title of about page
        # self.title(" About InvenPro") - AT TIME OF WRITING COMMENT WINDOW IS TOO SMALL TO SHOW TITLE TEXT
        self.title("")

        # Change icon to an information icon
        icon = tk.PhotoImage(file = (os.getcwd() + '/driverBin/images/icons/info-16px.png'))
        self.iconphoto(False, icon)

        # Set the background color to grey
        self.config(bg = self.bgCol)

        # Declare Top Label and Name Label
        aTopInfoLabel = tk.Label(master = self, text = f'{self.PROGRAMNAME} is developed and built by:', bg = self.bgCol)
        aNameLabel = tk.Label(master = self, text = "Thomas Campbell", font = 'bold', bg = self.bgCol)
        # Place Top Label and Name Label
        aTopInfoLabel.grid(row = 0, column = 0, columnspan = 2, sticky = "EW")
        aNameLabel.grid(row = 1, column = 0, columnspan = 2)

        # Declare Link Label
        aLinkLabel = tk.Label(master = self, text = "thomascampbell.dev", font = ('Helveticabold', 15), fg = "blue", cursor = "hand2", bg = self.bgCol)
        # Place Link Label
        aLinkLabel.grid(row = 2, column = 0, columnspan = 2, sticky = "EW")
        # Bind Click to Open Webpage
        aLinkLabel.bind("<Button-1>", lambda x: self.callback("https://thomascampbell.dev/"))

        # Declare Version labels
        aVersionLabel = tk.Label(master = self, text = f'Current InvenPro Version:', bg = self.bgCol)
        aVersionNumLabel = tk.Label(master = self, text = f'ALPHA', font = 'bold', bg = self.bgCol)
        # Place Version labels
        aVersionLabel.grid(row = 3, column = 0)
        aVersionNumLabel.grid(row = 3, column = 1)

        # Make the page unresizeable
        self.resizable(0, 0)
