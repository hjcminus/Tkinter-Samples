"""
treeview
  context menu
ttk style
#drag and drop:
#  https://docs.python.org/3/library/tkinter.dnd.html#:~:text=The%20tkinter.dnd%20module%20provides%20drag-and-drop%20support%20for%20objects,binding%20for%20it%20that%20starts%20the%20drag-and-drop%20process.

drag and drop files:
  pip install tkinterdnd2

just_playback   # give more control to playsound package
  pip install just_playback
"""

import os
import platform
import codecs
from tkinter import *
from tkinter.ttk import *

"""
from tkinter.ttk import *
That code causes several tkinter.ttk widgets (Button, Checkbutton, Entry, Frame, Label, LabelFrame, Menubutton, 
PanedWindow, Radiobutton, Scale and Scrollbar) to automatically replace the Tk widgets.
"""

from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinterdnd2 import *

import PIL.Image
import PIL.ImageTk

from just_playback import Playback

"""
from just_playback import Playback
playback = Playback() # creates an object for managing playback of a single audio file
playback.load_file('music-files/sample.mp3')
# or just pass the filename directly to the constructor

playback.play() # plays loaded audio file from the beginning
playback.pause() # pauses playback. Has no effect if playback is already paused
playback.resume() # resumes playback. Has no effect if playback is playing
playback.stop() # stops playback. Has no effect if playback is not active

playback.seek(60) # positions playback at 1 minute from the start of the audio file
playback.set_volume(0.5) # sets the playback volume to 50% of the audio file's original value

playback.loop_at_end(True) # since 0.1.5. Causes playback to automatically restart when it completes.

playback.active # True if playback is active i.e playing or paused
playback.playing # True if playback is active and not paused
playback.curr_pos # current absolute playback position in seconds from 
				  #	the start of the audio file (unlike pygame.mixer.get_pos). 
playback.paused # True if playback is paused.
playback.duration # length of the audio file in seconds. 
playback.volume # current playback volume
playback.loops_at_end # True if playback is set to restart when it completes.
"""


def format_time_str(secs):
    sec = secs % 60
    mins = secs // 60
    min_ = mins % 60
    hours = mins // 60

    if hours > 0:
        return f'{hours}:{min_}:{sec}'
    else:
        return f'{min_}:{sec}'


def get_file_duration_str(filename) -> str:
    pb = Playback()
    try:
        pb.load_file(filename)
        seconds = int(pb.duration)
        return format_time_str(seconds)
    except Exception as e:
        return ''


# inherited from TkinterDnD.Tk instead of Tk
class MainFrame(TkinterDnD.Tk):

    def __init__(self):
        Tk.__init__(self)

        self.__playback = Playback()  # create a playback object
        self.__playing = False

        self.title('Audio Playback')
        img = Image('photo', file='res/app.png')
        self.tk.call('wm', 'iconphoto', self._w, img)
        # self.protocol("WM_DELETE_WINDOW", self.on_close)

        # init window size
        init_wnd_cx = 640
        init_wnd_cy = 480
        scn_w, scn_h = self.maxsize()
        cen_x = (scn_w - init_wnd_cx) / 2
        cen_y = (scn_h - init_wnd_cy) / 2
        cen_y -= 30
        geometry_size_xy = '%dx%d+%d+%d' % (init_wnd_cx, init_wnd_cy, cen_x, cen_y)
        self.geometry(geometry_size_xy)

        s = Style()     # ttk.Style

        # all supported theme: winnative, clam, alt, default, classic, vista, xpnative
        s.theme_use('clam')

        # create menubar
        self.__menubar = Menu(self)

        file_menu = Menu(self, tearoff=0)
        file_menu.add_command(label="Load playlist...", command=self.__on_load_playlist)
        file_menu.add_command(label="Save playlist...", command=self.__on_save_playlist)
        file_menu.add_command(label="Add Files...", command=self.__on_add_files)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.__menubar.add_cascade(label='File', menu=file_menu)

        opr_menu = Menu(self, tearoff=0)
        opr_menu.add_command(label="Play", command=self.__on_play)
        opr_menu.add_command(label="Stop", command=self.__on_stop)
        opr_menu.add_command(label="Pause", command=self.__on_pause)
        self.__menubar.add_cascade(label='Playback', menu=opr_menu)

        help_menu = Menu(self, tearoff=0)
        help_menu.add_command(label="About...", command=MainFrame.__on_about)
        self.__menubar.add_cascade(label='Help', menu=help_menu)

        self.config(menu=self.__menubar)

        # load icons
        self.__imgtk_open = PIL.ImageTk.PhotoImage(PIL.Image.open("res/open.png"))
        self.__imgtk_save = PIL.ImageTk.PhotoImage(PIL.Image.open("res/save.png"))
        self.__imgtk_play = PIL.ImageTk.PhotoImage(PIL.Image.open("res/play.png"))
        self.__imgtk_stop = PIL.ImageTk.PhotoImage(PIL.Image.open("res/stop.png"))
        self.__imgtk_pause = PIL.ImageTk.PhotoImage(PIL.Image.open("res/pause.png"))

        # create toolbar
        self.__toolbar = Frame(self)
        self.__btn_open = Button(self.__toolbar, text="Load playlist", image=self.__imgtk_open, command=self.__on_load_playlist)
        self.__btn_open.pack(side=LEFT, padx=2, pady=2)
        self.__btn_save = Button(self.__toolbar, text="Save playlist", image=self.__imgtk_save, command=self.__on_save_playlist)
        self.__btn_save.pack(side=LEFT, padx=2, pady=2)
        sep = Separator(self.__toolbar)
        sep.pack(side=LEFT, fill=Y, padx=2, pady=2)
        self.__btn_play = Button(self.__toolbar, text="Play", image=self.__imgtk_play, command=self.__on_play)
        self.__btn_play.pack(side=LEFT, padx=2, pady=2)
        self.__btn_stop = Button(self.__toolbar, text="Stop", image=self.__imgtk_stop, command=self.__on_stop)
        self.__btn_stop.pack(side=LEFT, padx=2, pady=2)
        self.__btn_pause = Button(self.__toolbar, text="Pause", image=self.__imgtk_pause, command=self.__on_pause)
        self.__btn_pause.pack(side=LEFT, padx=2, pady=2)

        sep = Separator(self.__toolbar)
        sep.pack(side=LEFT, fill=Y, padx=2, pady=2)
        self.__volume = Scale(self.__toolbar, from_=0, to=100, orient=HORIZONTAL, length=100,
                              command=self.__on_volume_changed)
        self.__volume.set(50)
        self.__volume.pack(side=LEFT, fill=Y, padx=2, pady=2)

        sep = Separator(self.__toolbar)
        sep.pack(side=LEFT, fill=Y, padx=2, pady=2)
        self.__progress = Progressbar(self.__toolbar, orient=HORIZONTAL, mode='determinate')
        self.__progress.pack(side=LEFT, expand=True, fill=X, padx=2, pady=2)

        self.__toolbar.pack(side=TOP, fill=X)

        # create status bar
        self.__statusbar = Frame(self)
        self.__lab_progress = Label(self.__statusbar, text='Ready')
        self.__lab_progress.pack(side=LEFT)

        self.__statusbar.pack(side=BOTTOM, fill=X)

        # columns: set columns names
        self.__list = Treeview(self, columns=("col1", "col2"), selectmode="browse", show='headings', height=5)
        self.__list.pack(expand=True, fill=BOTH)

        # first parameter is the column name which defined in Treeview columns

        # to set the width of a column, we need set stretch property to NO
        # the unit of width is pixels  (might be scaled due to System\Display\Scale settings set by user)
        self.__list.column("col1", anchor=W, stretch=NO, width=500)
        self.__list.heading("col1", text="Filename")
        self.__list.column("col2", anchor=CENTER, stretch=YES)
        self.__list.heading("col2", text="Duration")

        self.__list.bind("<ButtonPress-1>", self.__on_list_left_button_down)
        self.__list.bind("<ButtonRelease-1>", self.__on_list_left_button_up)
        self.__list.bind("<Double-Button-1>", self.__on_list_left_button_double_click)
        self.__list.bind("<B1-Motion>", self.__on_list_left_button_move)

        self.__popup_menu = Menu(self.__list, tearoff=0)
        self.__popup_menu.add_command(label="Play", command=self.__on_play)
        self.__popup_menu.add_command(label="Stop", command=self.__on_stop)
        self.__popup_menu.add_command(label="Pause", command=self.__on_pause)
        self.__popup_menu.add_separator()
        self.__popup_menu.add_command(label="Remove", command=self.__on_remove_files)
        self.__list.bind('<Button-3>', self.__on_pop_context_menu)

        # set drag target
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.__on_drop_files)

        self.__left_button_down = False

        self.after(17, self.__on_audio_playback_frame)

    def __on_drop_files(self, event):
        files = []

        s = event.data
        while len(s) > 0:
            if s[0] == '{':
                idx = s.find('}')
                if idx > 0:
                    filename = s[1:idx]
                    files.append(filename)
                    s = s[idx+2:]
                else:
                    return  # error
            else:
                idx = s.find(' ')
                if idx > 0:
                    filename = s[0:idx]
                    files.append(filename)
                    s = s[idx+1:]
                else:
                    files.append(s)
                    break   # done

        for filename in files:
            # in windows platform, we need convert the filename to utf-8 codec
            if platform.system().lower() == 'windows':
                b = filename.encode('utf-8')
                filename = codecs.decode(b, 'utf-8')

            if filename.endswith(".wav") or filename.endswith(".mp3") or filename.endswith(".ogg"):
                duration = get_file_duration_str(filename)
                # the text attributes will be hidden
                self.__list.insert('', 'end', text="", values=(filename, duration), tags=[filename])

    def __on_audio_playback_frame(self):
        d = self.__playback.duration
        c = self.__playback.curr_pos
        if d > 0:
            p = c * 100 // d
            self.__progress['value'] = p

            c_str = format_time_str(int(c))
            d_str = format_time_str(int(d))

            self.__lab_progress.config(text=f'{c_str}/{d_str}')
        else:
            self.__progress['value'] = 0
            self.__lab_progress.config(text='Ready')

        self.after(17, self.__on_audio_playback_frame)  # continue

    def __on_load_playlist(self):
        path = askopenfilename(parent=self, title="Load playlist", filetypes=[('text file', '.txt')], initialdir='./')
        if path:
            # remove all old nodes in list widget
            for item in self.__list.get_children():
                self.__list.delete(item)

            try:
                f = open(path, 'r')
                if f:
                    lines = f.readlines()
                    for it in lines:
                        # remove line break
                        it = it.replace('\n', '')
                        it = it.replace('\r', '')

                        dur = get_file_duration_str(it)
                        self.__list.insert('', 'end', text="", values=(it, dur), tags=[it])

                if len(self.__list.children) > 0:
                    first_item = self.__list.get_children()[0]

                    self.__list.focus_set()
                    self.__list.see(first_item)
                    self.__list.focus(first_item)
                    self.__list.selection_set(first_item)
            except Exception as e:
                print(f'{e}')

    def __on_save_playlist(self):
        path = asksaveasfilename(parent=self, title="Save playlist", filetypes=[('text file', '.txt')], initialdir='./')
        if path:
            ext = os.path.splitext(path)[-1]
            if len(ext) == 0:
                path += '.txt'

            try:
                f = open(path, 'w')
                for item in self.__list.get_children():
                    attr = self.__list.item(item)
                    tags = attr["tags"]
                    filename = tags[0]

                    f.write(f"{filename}\n")
            except Exception as e:
                print(f'{e}')

    def __on_add_files(self):
        filenames = askopenfilenames(parent=self, filetypes=[('wav file', '.wav'),
                                                                      ('mp3 file', '.mp3'),
                                                                      ('ogg file', '.ogg'),
                                                                      ('all file', '.*')])

        for filename in filenames:
            if filename.endswith(".wav") or filename.endswith(".mp3") or filename.endswith(".ogg"):
                duration = get_file_duration_str(filename)
                # the text attributes will be hidden
                self.__list.insert('', 'end', text="", values=(filename, duration), tags=[filename])

    def __on_remove_files(self):
        sel = self.__list.focus()
        if sel:
            self.__list.delete(sel)

    def __on_play(self):
        self.__playing = True

        if self.__playback.paused:
            self.__playback.resume()
        else:
            cur_item = self.__list.focus()
            if cur_item:
                attr = self.__list.item(cur_item)
                tags = attr["tags"]
                filename = tags[0]

                self.__playback.load_file(filename)
                self.__playback.play()

    def __on_stop(self):
        self.__playing = False
        self.__playback.stop()

    def __on_pause(self):
        self.__playing = False
        self.__playback.pause()

    def __on_volume_changed(self, value):
        self.__playback.set_volume(float(value) * 0.01)

    def __on_pop_context_menu(self, event):
        sel = self.__list.focus()
        if not sel:
            return

        try:
            self.__popup_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.__popup_menu.grab_release()

    def __on_list_left_button_down(self, event):
        self.__left_button_down = True

        iid = self.__list.identify_row(event.y)
        if iid != '' and not iid not in self.__list.selection():
            self.__list.selection_set(iid)

    def __on_list_left_button_up(self, event):
        self.__left_button_down = False

    def __on_list_left_button_double_click(self, event):
        self.__on_play()

    def __on_list_left_button_move(self, event):
        if not self.__left_button_down:
            return

        iid = self.__list.identify_row(event.y)
        if iid == '':
            return

        moveto = self.__list.index(iid)
        for s in self.__list.selection():
            self.__list.move(s, '', moveto)

    @staticmethod
    def __on_about():
        showinfo('About', 'Audio Player 1.0')


def main():
    mainframe = MainFrame()
    mainframe.mainloop()


if __name__ == "__main__":
    main()
