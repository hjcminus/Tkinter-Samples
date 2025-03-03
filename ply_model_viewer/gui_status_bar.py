"""@ package docstring
Status Bar

display the filename of the current ply file
"""


from tkinter import *


# -----------------------------------------------------------------------------#
# GUIStatusBar
# -----------------------------------------------------------------------------#


class GUIStatusBar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bd=1, height=20, relief=SUNKEN)
        self.pack(side=BOTTOM, fill=X)

        self.lab_infor = Label(self, text="")
        self.lab_infor.pack(side=LEFT)

    def set_infor(self, s):
        self.lab_infor.config(text=s)
