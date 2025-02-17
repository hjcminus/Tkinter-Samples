
import os
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter.messagebox import *    # showdialog
from pathlib import Path
import PIL.Image
import PIL.ImageTk


doc_filename = ''


def on_new():
    global contents
    contents.delete(1.0, END)


def on_open():
    filename = filedialog.askopenfilename(parent=root, filetypes=[('text file', '.txt')])
    if filename:
        try:
            text = Path(filename).read_text(encoding="utf-8")

            global contents
            contents.delete(1.0, END)
            contents.insert(END, text)

            global lab_info
            lab_info.config(text=filename)

        except Exception as e:
            print(f'{e}')


def on_save():
    if doc_filename == '':
        on_save_as()
    else:
        global contents
        text = contents.get(1.0, END)
        Path(doc_filename).write_text(encoding="utf-8", data=text)


def on_save_as():
    filename = filedialog.asksaveasfilename(parent=root, filetypes=[('text file', '.txt')])
    if filename:
        try:
            global contents
            text = contents.get(1.0, END)
            Path(filename).write_text(encoding="utf-8", data=text)

        except Exception as e:
            print(f'{e}')


def on_about():
    showinfo('About', 'Simple Notepad')


root = Tk()
root.title("notepad")
root.geometry("640x480")

icon_new = PIL.ImageTk.PhotoImage(PIL.Image.open("res/new.png"))
icon_open = PIL.ImageTk.PhotoImage(PIL.Image.open("res/open.png"))
icon_save = PIL.ImageTk.PhotoImage(PIL.Image.open("res/save.png"))
icon_save_as = PIL.ImageTk.PhotoImage(PIL.Image.open("res/save_as.png"))

menubar = Menu(root)
root.config(menu=menubar)

# add file menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=on_new)
file_menu.add_command(label="Open", command=on_open)
file_menu.add_command(label="Save", command=on_save)
file_menu.add_command(label="Save As...", command=on_save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=file_menu)

# add help menu
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About...", command=on_about)
menubar.add_cascade(label='Help', menu=help_menu)

toolbar = Frame(root, bd=1, relief=FLAT)

btn_new = Button(toolbar, text="New", image=icon_new, bd=1, relief=FLAT, command=on_new)
btn_new.pack(side=LEFT, padx=1, pady=1)

btn_open = Button(toolbar, text="Open", image=icon_open, bd=1, relief=FLAT, command=on_open)
btn_open.pack(side=LEFT, padx=1, pady=1)

btn_save = Button(toolbar, text="Save", image=icon_save, bd=1, relief=FLAT, command=on_save)
btn_save.pack(side=LEFT, padx=1, pady=1)

btn_save_as = Button(toolbar, text="Save As..", image=icon_save_as, bd=1, relief=FLAT, command=on_save_as)
btn_save_as.pack(side=LEFT, padx=1, pady=1)

toolbar.pack(side=TOP, fill=X)


statusbar = Frame(root, bd=1, height=20, relief=SUNKEN)
lab_info = Label(statusbar, text="Ready")
lab_info.pack(side=LEFT)

statusbar.pack(side=BOTTOM, fill=X)

contents = scrolledtext.ScrolledText(root, wrap=NONE)
contents.pack(expand=1, fill=BOTH)

root.mainloop()

