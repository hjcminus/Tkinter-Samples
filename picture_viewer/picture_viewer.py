"""
if image too small then center display. never scale it up to fit the canvas

"""

import os
import platform
from tkinter import *
from tkinter.ttk import Separator
from tkinter import filedialog
from tkinter.messagebox import *    # showdialog
import PIL.Image
import PIL.ImageTk


class PictureViewer(Tk):
    def __init__(self):
        super().__init__()

        scn_w, scn_h = self.maxsize()

        # half fullscreen size
        init_wnd_cx = scn_w // 2
        init_wnd_cy = scn_h // 2

        cen_x = (scn_w - init_wnd_cx) // 2
        cen_y = (scn_h - init_wnd_cy) // 2
        geometry_size_xy = '%dx%d+%d+%d' % (init_wnd_cx, init_wnd_cy, cen_x, cen_y)

        self.title("Picture Viewer")
        self.geometry(geometry_size_xy)

        # setup application icon
        self.__app_icon = Image('photo', file='res/app.png')
        self.tk.call('wm', 'iconphoto', self._w, self.__app_icon)

        # load icons
        self.__icon_open = PIL.ImageTk.PhotoImage(PIL.Image.open("res/open.png"))
        self.__icon_exit = PIL.ImageTk.PhotoImage(PIL.Image.open("res/exit.png"))
        self.__icon_about = PIL.ImageTk.PhotoImage(PIL.Image.open("res/about.png"))
        self.__icon_prior = PIL.ImageTk.PhotoImage(PIL.Image.open("res/prior.png"))
        self.__icon_next = PIL.ImageTk.PhotoImage(PIL.Image.open("res/next.png"))
        self.__icon_fit = PIL.ImageTk.PhotoImage(PIL.Image.open("res/fit.png"))
        self.__icon_zoom_in = PIL.ImageTk.PhotoImage(PIL.Image.open("res/zoom_in.png"))
        self.__icon_zoom_out = PIL.ImageTk.PhotoImage(PIL.Image.open("res/zoom_out.png"))

        # create a menubar
        menubar = Menu(self)
        self.config(menu=menubar)

        # add file menu
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", image=self.__icon_open, compound='left', command=self.__on_open)
        file_menu.add_separator()
        file_menu.add_command(label="Prior", image=self.__icon_prior, compound='left', command=self.__on_prior)
        file_menu.add_command(label="Next", image=self.__icon_next, compound='left', command=self.__on_next)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", image=self.__icon_exit, compound='left', command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # add edit menu
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Fit", image=self.__icon_fit, compound='left', command=self.__on_fit)
        edit_menu.add_command(label="Zoom In", image=self.__icon_zoom_in, compound='left', command=self.__on_zoom_in)
        edit_menu.add_command(label="Zoom Out", image=self.__icon_zoom_out, compound='left', command=self.__on_zoom_out)
        menubar.add_cascade(label='Edit', menu=edit_menu)

        # add help menu
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About...", image=self.__icon_about, compound='left', command=PictureViewer.on_about)
        menubar.add_cascade(label='Help', menu=help_menu)

        # create a toolbar
        toolbar = Frame(self, bd=1, relief=FLAT)

        btn_open = Button(toolbar, text="Open", image=self.__icon_open, bd=1, relief=FLAT, command=self.__on_open)
        btn_open.pack(side=LEFT, padx=1, pady=1)

        sep = Separator(toolbar)
        sep.pack(side=LEFT, fill="y", padx=2, pady=2)

        btn_prior = Button(toolbar, text="Prior", image=self.__icon_prior, bd=1, relief=FLAT, command=self.__on_prior)
        btn_prior.pack(side=LEFT, padx=1, pady=1)

        btn_next = Button(toolbar, text="Next", image=self.__icon_next, bd=1, relief=FLAT, command=self.__on_next)
        btn_next.pack(side=LEFT, padx=1, pady=1)

        sep = Separator(toolbar)
        sep.pack(side=LEFT, fill="y", padx=2, pady=2)

        btn_fit = Button(toolbar, text="Fit", image=self.__icon_fit, bd=1, relief=FLAT, command=self.__on_fit)
        btn_fit.pack(side=LEFT, padx=1, pady=1)

        btn_zoom_in = Button(toolbar, text="Zoom In", image=self.__icon_zoom_in, bd=1, relief=FLAT, command=self.__on_zoom_in)
        btn_zoom_in.pack(side=LEFT, padx=1, pady=1)

        btn_zoom_out = Button(toolbar, text="Zoom Out", image=self.__icon_zoom_out, bd=1, relief=FLAT, command=self.__on_zoom_out)
        btn_zoom_out.pack(side=LEFT, padx=1, pady=1)

        toolbar.pack(side=TOP, fill=X)

        # create a statusbar
        statusbar = Frame(self, bd=1, height=20, relief=SUNKEN)
        self.__lab_info = Label(statusbar, text="Ready")
        self.__lab_info.pack(side=LEFT)

        statusbar.pack(side=BOTTOM, fill=X)

        # create canvas
        self.__canvas = Canvas(self, width=100, height=100, background='lightgray')
        self.__canvas.pack(expand=1, fill=BOTH)

        # bind arrow keys
        self.__canvas.bind('<Left>', self.__on_canvas_left_key_press)
        self.__canvas.bind('<Right>', self.__on_canvas_right_key_press)

        # mouse wheel to zoomin & zoomout
        if platform.system().lower() == 'windows':
            self.__canvas.bind("<MouseWheel>", self.__on_canvas_mousewheel)
        elif platform.system().lower() == 'linux':
            self.__canvas.bind("<Button-4>", self.__on_canvas_zoom_in)
            self.__canvas.bind("<Button-5>", self.__on_canvas_zoom_out)

        # hold left button to pan image
        self.__canvas.bind("<Button-1>", self.__on_canvas_left_button_down)
        self.__canvas.bind("<ButtonRelease-1>", self.__on_canvas_left_button_up)
        self.__canvas.bind('<Motion>', self.__on_canvas_mouse_move)

        # canvas resize
        self.__canvas.bind('<Configure>', self.__on_canvas_resize)

        self.__tk_image = None  # hold an ImageTk object reference to avoid garbage collected

        self.__filenames = []   # all image filenames in user opened folder
        self.__cur_filename = ''
        self.__cur_original_image = None
        self.__min_zoom_factor = 1.0
        self.__max_zoom_factor = 1.0
        self.__cur_zoom_factor = 1.0
        self.__min_image_x = 0  # int
        self.__min_image_y = 0  # int
        self.__max_image_x = 0  # int
        self.__max_image_y = 0  # int
        self.__cur_image_x = 0   # int
        self.__cur_image_y = 0    # int
        self.__left_button_down = False     # left button state
        self.__prior_mouse_x = 0
        self.__prior_mouse_y = 0

    def __adjust_image_size(self, image):
        image_cx = image.width
        image_cy = image.height

        canvas_cx = self.__canvas.winfo_width()
        canvas_cy = self.__canvas.winfo_height()

        image_ratio = image_cy / image_cx
        canvas_ratio = canvas_cy / canvas_cx

        if image_cx < canvas_cx and image_cy < canvas_cy:
            # smaller than canvas, show as original size

            self.__min_zoom_factor = 1.0

            if image_ratio > canvas_ratio:
                self.__max_zoom_factor = canvas_cy / image_cy
            else:
                self.__max_zoom_factor = canvas_cx / image_cx

            self.__cur_zoom_factor = self.__min_zoom_factor

            return image
        else:
            # either dimension of the image is larger than the canvas

            self.__max_zoom_factor = 4.0    # tune this

            # min zoom: fit display
            if image_ratio > canvas_ratio:
                new_image_cy = canvas_cy
                new_image_cx = int(round(new_image_cy / image_ratio))
                self.__min_zoom_factor = canvas_cy / image_cy
            else:
                new_image_cx = canvas_cx
                new_image_cy = int(round(new_image_cx * image_ratio))
                self.__min_zoom_factor = canvas_cx / image_cx

            self.__cur_zoom_factor = self.__min_zoom_factor

            return image.resize((new_image_cx, new_image_cy))   # new size as a tuple

    def __update_image_min_max_pos(self, image):
        canvas_cx = self.__canvas.winfo_width()
        canvas_cy = self.__canvas.winfo_height()

        image_cx = image.width
        image_cy = image.height

        if image_cx > canvas_cx:
            self.__min_image_x = canvas_cx - image_cx
            self.__max_image_x = 0
        else:
            # center
            self.__min_image_x = self.__max_image_x = (canvas_cx - image_cx) // 2

        if image_cy > canvas_cy:
            self.__min_image_y = canvas_cy - image_cy
            self.__max_image_y = 0
        else:
            # center
            self.__min_image_y = self.__max_image_y = (canvas_cy - image_cy) // 2

    def __clamp_image_cur_pos(self):
        if self.__cur_image_x < self.__min_image_x:
            self.__cur_image_x = self.__min_image_x
        if self.__cur_image_x > self.__max_image_x:
            self.__cur_image_x = self.__max_image_x

        if self.__cur_image_y < self.__min_image_y:
            self.__cur_image_y = self.__min_image_y
        if self.__cur_image_y > self.__max_image_y:
            self.__cur_image_y = self.__max_image_y

    def __clamp_cur_zoom_factor(self):
        if self.__cur_zoom_factor < self.__min_zoom_factor:
            self.__cur_zoom_factor = self.__min_zoom_factor
        if self.__cur_zoom_factor > self.__max_zoom_factor:
            self.__cur_zoom_factor = self.__max_zoom_factor

    def __init_show_image(self, filename):
        self.__cur_filename = filename

        self.__cur_original_image = PIL.Image.open(self.__cur_filename)
        if not self.__cur_original_image:
            print('open image failed')
            return

        image = self.__adjust_image_size(self.__cur_original_image)
        self.__update_image_min_max_pos(image)

        canvas_cx = self.__canvas.winfo_width()
        canvas_cy = self.__canvas.winfo_height()

        # center display
        self.__cur_image_x = (canvas_cx - image.width) // 2
        self.__cur_image_y = (canvas_cy - image.height) // 2
        self.__clamp_image_cur_pos()

        # clear old image
        self.__canvas.delete("all")

        # display new image
        self.__tk_image = PIL.ImageTk.PhotoImage(image)
        self.__canvas.create_image(self.__cur_image_x, self.__cur_image_y, anchor=NW, image=self.__tk_image)

        self.__lab_info.config(text=self.__cur_filename)

    def __zoom_at(self, zoom_factor_adjust, view_x, view_y):
        # the viewport (canvas) is fixed

        if self.__cur_original_image:
            old_zoom_factor = self.__cur_zoom_factor
            self.__cur_zoom_factor *= zoom_factor_adjust
            self.__clamp_cur_zoom_factor()

            zoom_factor_adjust = self.__cur_zoom_factor / old_zoom_factor

            new_image_cx = int(round(self.__cur_original_image.width * self.__cur_zoom_factor))
            new_image_cy = int(round(self.__cur_original_image.height * self.__cur_zoom_factor))
            image_scaled = self.__cur_original_image.resize((new_image_cx, new_image_cy))
            self.__update_image_min_max_pos(image_scaled)

            old_view_x_to_image_x = view_x - self.__cur_image_x
            old_view_y_to_image_y = view_y - self.__cur_image_y

            new_view_x_to_image_x = old_view_x_to_image_x * zoom_factor_adjust
            new_view_y_to_image_y = old_view_y_to_image_y * zoom_factor_adjust

            self.__cur_image_x = view_x - new_view_x_to_image_x
            self.__cur_image_y = view_y - new_view_y_to_image_y
            self.__clamp_image_cur_pos()

            # clear old image
            self.__canvas.delete("all")

            # display new image
            self.__tk_image = PIL.ImageTk.PhotoImage(image_scaled)
            self.__canvas.create_image(self.__cur_image_x, self.__cur_image_y, anchor=NW, image=self.__tk_image)

    def move_view(self, delta_x, delta_y):
        if self.__tk_image:
            self.__cur_image_x += delta_x
            self.__cur_image_y += delta_y
            self.__clamp_image_cur_pos()

            # clear old image
            self.__canvas.delete("all")
            self.__canvas.create_image(self.__cur_image_x, self.__cur_image_y, anchor=NW, image=self.__tk_image)

    def __on_open(self):
        filename = filedialog.askopenfilename(parent=self)
        if filename:
            try:
                self.__filenames.clear()
                self.__cur_filename = ''
                self.__lab_info.config(text='')

                lst = os.path.split(filename)[0:-1]
                folder_name = os.sep.join(lst)

                for it in os.listdir(folder_name):
                    it_filename = os.path.join(folder_name, it)  # full filename
                    if os.path.isfile(it_filename) and (it_filename.endswith('jpg')
                                                        or it_filename.endswith('jpeg')
                                                        or it_filename.endswith('bmp')
                                                        or it_filename.endswith('tga')
                                                        or it_filename.endswith('png')
                                                        or it_filename.endswith('gif')
                                                        or it_filename.endswith('tif')
                                                        or it_filename.endswith('tiff')):
                        self.__filenames.append(it_filename)

                base_filename = os.path.basename(filename)
                for it in self.__filenames:
                    if base_filename == os.path.basename(it):
                        self.__init_show_image(it)
                        break

            except Exception as e:
                print(f'{e}')

    def __on_prior(self):
        # find prior image
        prior_image_filename = ''
        sz = len(self.__filenames)
        for i in range(sz-1, 0, -1):
            if self.__filenames[i] == self.__cur_filename:
                prior_image_filename = self.__filenames[i - 1]
                break

        if len(prior_image_filename) > 0:
            self.__init_show_image(prior_image_filename)

    def __on_next(self):
        # find next image
        next_image_filename = ''
        sz = len(self.__filenames)
        for i in range(0, sz-1):
            if self.__filenames[i] == self.__cur_filename:
                next_image_filename = self.__filenames[i+1]
                break

        if len(next_image_filename) > 0:
            self.__init_show_image(next_image_filename)

    def __on_fit(self):
        if len(self.__cur_filename) > 0:
            self.__init_show_image(self.__cur_filename)

    def __on_zoom_in(self):
        canvas_cx = self.__canvas.winfo_width()
        canvas_cy = self.__canvas.winfo_height()

        self.__zoom_at(1.1, canvas_cx / 2, canvas_cy / 2)  # zoom in at center

    def __on_zoom_out(self):
        canvas_cx = self.__canvas.winfo_width()
        canvas_cy = self.__canvas.winfo_height()

        self.__zoom_at(0.9, canvas_cx / 2, canvas_cy / 2)  # zoom out at center

    def __on_canvas_left_key_press(self, event):
        self.__on_prior()

    def __on_canvas_right_key_press(self, event):
        self.__on_next()

    def __on_canvas_mousewheel(self, event):
        if event.delta > 0:
            self.__on_canvas_zoom_in(event)
        else:
            self.__on_canvas_zoom_out(event)

    def __on_canvas_zoom_in(self, event):
        self.__zoom_at(1.1, event.x, event.y)  # zoom in

    def __on_canvas_zoom_out(self, event):
        self.__zoom_at(0.9, event.x, event.y)  # zoom out

    def __on_canvas_left_button_down(self, event):
        self.__canvas.focus_set()   # set keyboard target
        self.__left_button_down = True

        self.__prior_mouse_x = event.x
        self.__prior_mouse_y = event.y

    def __on_canvas_left_button_up(self, event):
        self.__left_button_down = False

    def __on_canvas_mouse_move(self, event):
        if self.__left_button_down:
            delta_view_x = event.x - self.__prior_mouse_x
            delta_view_y = event.y - self.__prior_mouse_y
            self.move_view(delta_view_x, delta_view_y)
            self.__prior_mouse_x = event.x
            self.__prior_mouse_y = event.y

    def __on_canvas_resize(self, event):
        if len(self.__cur_filename):
            self.__init_show_image(self.__cur_filename)

    @staticmethod
    def on_about():
        showinfo('About', 'Simple Picture Viewer')


def main():
    picture_viewer = PictureViewer()
    picture_viewer.mainloop()


if __name__ == '__main__':
    main()
