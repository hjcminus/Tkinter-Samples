"""@ package docstring
Center view, display a mesh in wireframe mode

"""

import platform
from tkinter import *


# -----------------------------------------------------------------------------#
# GUIView
# -----------------------------------------------------------------------------#


class GUIView(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent, width=1, height=1, bg=parent.cfg_bg_color)
        self.__main_frame = parent

        self.pack(expand=1, fill=BOTH)
        self.update()

        self.bind("<Button-1>", self.__on_canvas_left_button_down)
        self.bind("<Button-2>", self.__on_canvas_middle_button_down)
        self.bind("<Button-3>", self.__on_canvas_right_button_down)
        self.bind("<ButtonRelease-1>", self.__on_canvas_left_button_up)
        self.bind("<ButtonRelease-2>", self.__on_canvas_middle_button_up)
        self.bind("<ButtonRelease-3>", self.__on_canvas_right_button_up)
        self.bind('<Motion>', self.__on_canvas_mouse_move)

        if platform.system().lower() == 'windows':
            self.bind("<MouseWheel>", self.__on_canvas_mousewheel)
        elif platform.system().lower() == 'linux':
            self.bind("<Button-4>", self.__on_canvas_zoomin)
            self.bind("<Button-5>", self.__on_canvas_zoom_out)

        self.__left_button_down = False
        self.__right_button_down = False
        self.__cursor_prior_x = 0
        self.__cursor_prior_y = 0

    def __on_canvas_left_button_down(self, event):
        self.__left_button_down = True
        self.__cursor_prior_x = event.x
        self.__cursor_prior_y = event.y

    def __on_canvas_middle_button_down(self, event):
        pass

    def __on_canvas_right_button_down(self, event):
        self.__right_button_down = True
        self.__cursor_prior_x = event.x
        self.__cursor_prior_y = event.y

    def __on_canvas_left_button_up(self, event):
        self.__left_button_down = False

    def __on_canvas_middle_button_up(self, event):
        pass

    def __on_canvas_right_button_up(self, event):
        self.__right_button_down = False

    def __on_canvas_mouse_move(self, event):
        if self.__left_button_down or self.__right_button_down:
            cursor_current_x = event.x
            cursor_current_y = event.y

            delta_x = cursor_current_x - self.__cursor_prior_x
            delta_y = cursor_current_y - self.__cursor_prior_y

            if self.__left_button_down:
                self.__main_frame.model_viewer.rotate_camera_around_center(-delta_x * 0.5, -delta_y * 0.5)
            else:
                self.__main_frame.model_viewer.translate_camera(-delta_x, delta_y)

            self.__cursor_prior_x = cursor_current_x
            self.__cursor_prior_y = cursor_current_y

    def __on_canvas_mousewheel(self, event):
        if event.delta > 0:
            self.__on_canvas_zoomin(event)
        else:
            self.__on_canvas_zoom_out(event)

    def __on_canvas_zoomin(self, event):
        self.__main_frame.model_viewer.zoom_camera(0.9)

    def __on_canvas_zoom_out(self, event):
        self.__main_frame.model_viewer.zoom_camera(1.1)


