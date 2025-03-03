"""@ package docstring
Main window
"""

import os
import configparser

from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb

import PIL.Image
import PIL.ImageTk

import common
from gui_view import GUIView
from gui_menu_bar import GUIMenuBar
from gui_toolbar import GUIToolBar
from gui_status_bar import GUIStatusBar
from gui_settings_dlg import *
from model_viewer import *


# -----------------------------------------------------------------------------#
# GUIMainframe
# -----------------------------------------------------------------------------#


class GUIMainframe(Tk):

    # inner class, implement CanvasIntf interface
    class GUICanvas(common.CanvasIntf):
        def __init__(self, owner, tk_canvas):
            common.CanvasIntf.__init__(self)
            self.__owner = owner
            self.__tk_canvas = tk_canvas

        # override
        def clear(self):
            self.__tk_canvas.delete('all')

        # override
        def draw_line(self, vec2_pt1, vec2_pt2):
            view_points = [vec2_pt1.x, vec2_pt1.y, vec2_pt2.x, vec2_pt2.y]
            self.__tk_canvas.create_line(view_points, fill=self.__owner.cfg_fg_color)

    def __init__(self):
        Tk.__init__(self)

        # load config

        # give some default values
        self.cfg_main_wnd_w = 640
        self.cfg_main_wnd_h = 480
        self.cfg_fovy = 45.0
        self.cfg_open_folder = './test_ply_files'
        self.cfg_bg_color = 'white'
        self.cfg_fg_color = 'black'
        self.cfg_proj_mode = common.PROJ_MODE_PERSPECTIVE
        self.__load_config()

        self.title('PLY Model View')

        img = Image('photo', file='res/app.png')
        self.tk.call('wm', 'iconphoto', self._w, img)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # init window size

        scn_w, scn_h = self.maxsize()
        cen_x = (scn_w - self.cfg_main_wnd_w) / 2
        cen_y = (scn_h - self.cfg_main_wnd_h) / 2
        cen_y -= 30
        geometry_size_xy = '%dx%d+%d+%d' % (self.cfg_main_wnd_w, self.cfg_main_wnd_h, cen_x, cen_y)
        self.geometry(geometry_size_xy)
        self.resizable(False, False)  # fixed window size
        self.update()

        # load icons
        self.__itk_open = PIL.ImageTk.PhotoImage(PIL.Image.open("res/open.png"))
        self.__itk_clear = PIL.ImageTk.PhotoImage(PIL.Image.open("res/clear.png"))
        self.__itk_settings = PIL.ImageTk.PhotoImage(PIL.Image.open("res/settings.png"))

        self.__var_proj_mode = StringVar()   # for menu bar Projection Mode
        self.__var_proj_mode.set(self.cfg_proj_mode)

        self.__menu_bar = GUIMenuBar(self, self.__var_proj_mode)
        self.__toolbar = GUIToolBar(self)
        self.__status_bar = GUIStatusBar(self)
        self.__gui_view = GUIView(self)

        canvas_impl = GUIMainframe.GUICanvas(self, self.__gui_view)
        self.__model_viewer = ModelViewer(canvas_impl, self.cfg_fovy, self.cfg_proj_mode,
                                          self.__gui_view.winfo_width(), self.__gui_view.winfo_height())

        self.__settings_dlg = None

    def __load_config(self):
        config = configparser.ConfigParser()
        try:
            config.read('./cfg.ini', encoding="utf-8")

            self.cfg_main_wnd_w = config.getint('config', 'main_wnd_w', fallback=self.cfg_main_wnd_w)
            self.cfg_main_wnd_h = config.getint('config', 'main_wnd_h', fallback=self.cfg_main_wnd_h)
            self.cfg_fovy = config.getfloat('config', 'fovy', fallback=self.cfg_fovy)
            self.cfg_open_folder = config.get('config', 'open_folder', fallback=self.cfg_open_folder)
            self.cfg_bg_color = config.get('config', 'bg_color', fallback=self.cfg_bg_color)
            self.cfg_fg_color = config.get('config', 'fg_color', fallback=self.cfg_fg_color)
            self.cfg_proj_mode = config.get('config', 'proj_mode', fallback=self.cfg_proj_mode)

        except Exception as e:
            print(f'__load_config error: {e}\n')

    def save_config(self):
        try:
            config = configparser.ConfigParser()

            config['config'] = {}
            config['config']['main_wnd_w'] = str(self.cfg_main_wnd_w)
            config['config']['main_wnd_h'] = str(self.cfg_main_wnd_h)
            config['config']['fovy'] = str(self.cfg_fovy)
            config['config']['open_folder'] = self.cfg_open_folder
            config['config']['bg_color'] = self.cfg_bg_color
            config['config']['fg_color'] = self.cfg_fg_color
            config['config']['proj_mode'] = self.cfg_proj_mode

            with open('./cfg.ini', 'w') as configfile:
                config.write(configfile)

            # update var
            self.__var_proj_mode.set(self.cfg_proj_mode)

            self.__gui_view.configure(bg=self.cfg_bg_color)
            self.__model_viewer.set_fovy(self.cfg_fovy)
            self.__model_viewer.set_proj_mode(self.cfg_proj_mode)
            self.__model_viewer.draw()

        except Exception as e:
            print(f'save_config error: {e}')

    @property
    def itk_open(self):
        return self.__itk_open

    @property
    def itk_clear(self):
        return self.__itk_clear

    @property
    def itk_settings(self):
        return self.__itk_settings

    @property
    def model_viewer(self):
        return self.__model_viewer

    def open_model(self):
        try:
            path = fd.askopenfilename(parent=self, filetypes=[('ply file', '.ply')], initialdir=self.cfg_open_folder)

            if path:
                s = os.path.split(path)
                folder = s[0]
                if folder != self.cfg_open_folder:
                    self.cfg_open_folder = folder
                    self.save_config()

                self.__model_viewer.load_model(path)
                self.__status_bar.set_infor(path)

        except Exception as e:
            print(f'open_model error: {e}\n')

    def load_test_cube(self):
        self.__model_viewer.load_test_cube()

    def clear_model(self):
        self.__model_viewer.clear_model()
        self.__status_bar.set_infor('')

    def on_settings(self):
        if not self.__settings_dlg:
            self.__settings_dlg = GUISettingsDialog(self)
            self.wait_window(self.__settings_dlg)

    def on_closing(self):
        self.__model_viewer.quit()
        self.destroy()

    def on_projection_mode(self):
        self.cfg_proj_mode = self.__var_proj_mode.get()
        self.save_config()

    def on_settings_dlg_closed(self):
        self.__settings_dlg = None

    def about(self):
        mb.showinfo('About', 'PLY Model Viewer\n')
