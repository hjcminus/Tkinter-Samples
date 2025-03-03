"""@ package docstring
ToolBar

"""


from tkinter import *
from tkinter import ttk


# -----------------------------------------------------------------------------#
# ToolButton
# -----------------------------------------------------------------------------#


class ToolButton(Button):

    def __init__(self, parent, hint, **kwargs):
        Button.__init__(self, parent, **kwargs)
        self.tooltip_window = None
        self.hint = hint

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def on_hover(self, event):
        self.config(background='DeepSkyBlue')

        # Create a new top-level window with the tooltip text
        self.tooltip_window = Toplevel(self)
        tooltip_label = Label(self.tooltip_window, text=self.hint)
        tooltip_label.pack()

        # Use the overrideredirect method to remove the window's decorations
        self.tooltip_window.overrideredirect(True)

        # Calculate the coordinates for the tooltip window
        x = self.winfo_pointerx() + 10
        y = self.winfo_pointery() + 10
        self.tooltip_window.geometry("+{}+{}".format(x, y))

    def on_leave(self, event):
        self.config(background='WhiteSmoke')

        # Destroy the tooltip window
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


# -----------------------------------------------------------------------------#
# GUIToolBar
# -----------------------------------------------------------------------------#


class GUIToolBar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bd=1, relief=RAISED)

        self.__main_frame = parent

        # open
        btn_open = ToolButton(self, 'open', image=self.__main_frame.itk_open, relief=FLAT,
                              command=self.__on_open_model)
        btn_open.pack(side=LEFT, padx=2, pady=2)

        # clear
        btn_clear = ToolButton(self, 'clear', image=self.__main_frame.itk_clear, relief=FLAT,
                               command=self.__on_clear_model)
        btn_clear.pack(side=LEFT, padx=2, pady=2)

        sep = ttk.Separator(self)
        sep.pack(side=LEFT, fill="y", padx=2, pady=2)

        # settings
        btn_settings = ToolButton(self, 'settings', image=self.__main_frame.itk_settings, relief=FLAT,
                                  command=self.__on_settings)
        btn_settings.pack(side=LEFT, padx=2, pady=2)

        self.pack(side=TOP, fill=X)

    def __on_open_model(self):
        self.__main_frame.open_model()

    def __on_clear_model(self):
        self.__main_frame.clear_model()

    def __on_settings(self):
        self.__main_frame.on_settings()
