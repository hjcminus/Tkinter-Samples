"""@ package docstring
Settings Dialog
"""

from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor
import common

# -----------------------------------------------------------------------------#
# GUISettingsDialog
# -----------------------------------------------------------------------------#


class GUISettingsDialog(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.__main_frame = parent

        self.title('Settings')

        img = Image('photo', file='res/app.png')
        self.tk.call('wm', 'iconphoto', self._w, img)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind('<Escape>', self.on_escape_key)

        row = 0
        lbl_projection_mode = Label(self, text='Projection Mode', font=common.g_font_tuple, anchor=E)
        lbl_projection_mode.grid(row=row, column=0, padx=1, pady=1, sticky=W)

        self.__cbx_proj_mode = ttk.Combobox(self, width=16, font=common.g_font_tuple)
        self.__cbx_proj_mode['values'] = (common.PROJ_MODE_PERSPECTIVE, common.PROJ_MODE_ORTHOGRAPHIC)
        self.__cbx_proj_mode['state'] = 'readonly'
        self.__cbx_proj_mode.set(self.__main_frame.cfg_proj_mode)
        self.__cbx_proj_mode.grid(row=row, column=1, padx=1, pady=1, sticky=W)

        row += 1
        lbl_fov_y = Label(self, text='Field of View (Y)', font=common.g_font_tuple, anchor=E)
        lbl_fov_y.grid(row=row, column=0, padx=1, pady=1, sticky=W)

        self.__edt_fov_y = Entry(self, font=common.g_font_tuple, width=16)
        self.__edt_fov_y.insert(0, str(self.__main_frame.cfg_fovy))
        self.__edt_fov_y.grid(row=row, column=1, padx=1, pady=1, sticky=W)

        row += 1
        lbl_background_color = Label(self, text='Background Color', font=common.g_font_tuple, anchor=E)
        lbl_background_color.grid(row=row, column=0, padx=1, pady=1, sticky=W)

        self.__pan_background_color = PanedWindow(self, bg=self.__main_frame.cfg_bg_color, width=120, height=20)
        self.__pan_background_color.grid(row=row, column=1, padx=1, pady=1, sticky=W)
        self.__pan_background_color.bind("<Button-1>", self.on_choose_background_color)

        row += 1
        lbl_foreground_color = Label(self, text='Foreground Color', font=common.g_font_tuple, anchor=E)
        lbl_foreground_color.grid(row=row, column=0, padx=1, pady=1, sticky=W)

        self.__pan_foreground_color = PanedWindow(self, bg=self.__main_frame.cfg_fg_color, width=120, height=20)
        self.__pan_foreground_color.grid(row=row, column=1, padx=1, pady=1, sticky=W)
        self.__pan_foreground_color.bind("<Button-1>", self.on_choose_foreground_color)

        row += 1
        self.btn_ok = Button(self, text='Ok', font=common.g_font_tuple, width=16, command=self.on_ok)
        self.btn_ok.grid(row=row, column=1, sticky=E)

        dlg_w = 300
        dlg_h = 200

        # center display
        scn_w, scn_h = self.maxsize()
        cen_x = (scn_w - dlg_w) / 2
        cen_y = (scn_h - dlg_h) / 2
        cen_y -= 30
        geometry_size_xy = '%dx%d+%d+%d' % (dlg_w, dlg_h, cen_x, cen_y)
        self.geometry(geometry_size_xy)
        self.resizable(False, False)  # fixed window size
        self.attributes('-topmost', True)  # stay on top of parent window

    def on_choose_background_color(self, event):
        clr = askcolor(title='choose background color')
        if clr:
            self.__pan_background_color.configure(bg=clr[1])

    def on_choose_foreground_color(self, event):
        clr = askcolor(title='choose foreground color')
        if clr:
            self.__pan_foreground_color.configure(bg=clr[1])

    def on_ok(self):
        try:
            self.__main_frame.cfg_proj_mode = self.__cbx_proj_mode.get()
            self.__main_frame.cfg_fovy = float(self.__edt_fov_y.get())
            self.__main_frame.cfg_bg_color = self.__pan_background_color['background']
            self.__main_frame.cfg_fg_color = self.__pan_foreground_color['background']
            self.__main_frame.save_config()

            self.destroy()
            self.__main_frame.on_settings_dlg_closed()

        except Exception as e:
            print('[GUISettingsDialog.on_ok] Exception %s' % e)

    def on_escape_key(self, event):
        self.on_closing()

    # override
    def on_closing(self):
        self.destroy()
        self.__main_frame.on_settings_dlg_closed()
