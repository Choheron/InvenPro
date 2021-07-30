import tkinter as tk
from tkinter import ttk
from ..utils.settings import setIconInvenPro as setIcon

class InputDioBox(tk.Toplevel):
    def __init__(self, master, title, message, textvar):
        super().__init__(master)
        self.grab_set()
        # Set Icon for Window
        setIcon(self)

        # Set Title and Size
        self.title(title)
        self.config(bg = 'grey70')
        
        # Create master frame to make window dynamically resize
        self.container = tk.Frame(master = self, bg = 'grey70')

        # Create Warning Message
        message = tk.Label(master = self.container, text = message, font = 'bold', bg = 'LightGoldenrod1', relief = 'raised')
        # Place Warning Message
        message.grid(row = 0, column = 0)

        # Create and Configure Text box
        self.textBox = tk.Text(master = self.container, height = textvar.get().count("\n"), width = 40)
        self.textBox.insert("1.0", textvar.get())
        # Place Text Box
        self.textBox.grid(row = 1, column = 0, padx = 5, pady = 5)

        # Create Button Frame
        bttnFrame = tk.Frame(master = self.container, bg = 'grey70')

        # Create Buttons
        subBttn = ttk.Button(master = bttnFrame, text = "Submit", style = "M.TButton", command = lambda: self.setText(textvar))
        cancelBttn = ttk.Button(master = bttnFrame, text = "Cancel", style = "M.TButton", command = lambda: self.terminateCancel(textvar))

        # Place Buttons in master frame
        subBttn.grid(row = 0, column = 1, padx = 1, pady = 1,sticky = "E")
        cancelBttn.grid(row = 0, column = 2, padx = 1, pady = 1, sticky = "E")

        # Place button frame
        bttnFrame.grid(row = 2, column = 0, sticky = "NES")

        # Place master frame on window
        self.container.grid(row = 0, column = 0)

        # Rebind enter key to submit for the window and the text box
        self.textBox.bind("<Return>", lambda x=None: self.setText(textvar))
        self.protocol("<Return>", lambda x=None: self.setText(textvar))

        # Disable use of [X] in window manager
        self.protocol("WM_DELETE_WINDOW", self.terminate)

        # Disable resizing
        self.resizable(0, 0)

    def terminate(self):
        self.grab_release()
        self.destroy()

    def terminateCancel(self, textvar):
        textvar.set(value = "INPUTDIOCANCEL.DEBUG.INVENPRO")
        self.terminate()

    def setText(self, textvar):
        textvar.set(value = self.textBox.get("1.0", 'end-1c'))
        self.terminate()
