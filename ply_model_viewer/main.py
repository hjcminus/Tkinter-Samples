"""@ package docstring
Program entrance

"""

from gui_mainframe import GUIMainframe


# -----------------------------------------------------------------------------#
# main
# -----------------------------------------------------------------------------#


def main():
    gui_mainframe = GUIMainframe()
    gui_mainframe.mainloop()


if __name__ == "__main__":
    main()
