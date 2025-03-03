"""@ package docstring
MenuBar
"""

from tkinter import *
import common


# -----------------------------------------------------------------------------#
# GUIMenuBar
# -----------------------------------------------------------------------------#

class GUIMenuBar(Menu):
    def __init__(self, parent, var_proj_mode):
        Menu.__init__(self, parent)

        self.__main_frame = parent
        self.__var_proj_mode = var_proj_mode

        parent.config(menu=self)

        # file
        file_menu = Menu(self, tearoff=0)
        file_menu.add_command(label="Open...", font=common.g_font_tuple, command=self.__on_open_model)
        file_menu.add_command(label="Load Test Cube", font=common.g_font_tuple, command=self.__on_load_test_cube)
        file_menu.add_command(label="Clear", font=common.g_font_tuple, command=self.__on_clear_model)

        file_menu.add_separator()
        file_menu.add_command(label="Settings...", font=common.g_font_tuple, command=self.__on_settings)

        file_menu.add_separator()
        file_menu.add_command(label="Exit", font=common.g_font_tuple, command=self.__on_exit)
        self.add_cascade(label='File', font=common.g_font_tuple, menu=file_menu)

        # project mode
        proj_mode_menu = Menu(self, tearoff=0)
        proj_mode_menu.add_radiobutton(label="Perspective", font=common.g_font_tuple,
                                       command=self.__on_projection_mode,
                                       variable=self.__var_proj_mode,
                                       value=common.PROJ_MODE_PERSPECTIVE)
        proj_mode_menu.add_radiobutton(label="Orthographic", font=common.g_font_tuple,
                                       command=self.__on_projection_mode,
                                       variable=self.__var_proj_mode,
                                       value=common.PROJ_MODE_ORTHOGRAPHIC)
        self.add_cascade(label='Projection Mode', font=common.g_font_tuple, menu=proj_mode_menu)

        # help
        help_menu = Menu(self, tearoff=0)
        help_menu.add_command(label="About...", font=common.g_font_tuple, command=self.__on_about)
        self.add_cascade(label='Help', font=common.g_font_tuple, menu=help_menu)

    def __on_open_model(self):
        self.__main_frame.open_model()

    def __on_load_test_cube(self):
        self.__main_frame.load_test_cube()

    def __on_clear_model(self):
        self.__main_frame.clear_model()

    def __on_settings(self):
        self.__main_frame.on_settings()

    def __on_exit(self):
        self.__main_frame.on_closing()

    def __on_projection_mode(self):
        self.__main_frame.on_projection_mode()

    def __on_about(self):
        self.__main_frame.about()
