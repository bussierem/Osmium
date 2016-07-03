import os
import win32api
from collections import OrderedDict
from tkinter import *
from tkinter import ttk

from PIL import Image

# TODO:  ADD LINK TO https://icons8.com/ IN THE "ABOUT" PAGE!
#   Distributed through Creative Commons Attribution-NoDerivs 3.0 Unported License
#   https://creativecommons.org/licenses/by-nd/3.0/

# Colors
LIGHT_TEAL = "#00e6e6"
DARK_TEAL = "#009999"
BACKGROUND = "#6F807F"


def resize_img(path):
    img = Image.open(path)
    pal = img.getpalette()
    width, height = img.size
    actual_transp = img.info['actual_transparency']
    result = Image.new('LA', img.size)
    im = img.load()
    res = result.load()
    for x in range(width):
        for y in range(height):
            t = actual_transp[im[x, y]]
            color = pal[im[x, y]]
            res[x, y] = (color, t)
    result.resize((32, 32), Image.ANTIALIAS)
    return result


def get_used_drive_letters(os):
    drive_lbls = OrderedDict()
    if os == "Windows":
        #                           WINDOWS
        # ---------------------------------
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        for d in drives:
            drive_lbls[d] = d
            try:
                info = win32api.GetVolumeInformation(d)
                drive_lbls[d] = info[0] if info[0] != '' else d
            except:
                continue
    elif os == "Linux":
        #                             LINUX
        # ---------------------------------
        # Linux does not list drive letters
        drive_lbls = {'/': 'Root', '/home/': 'Home'}
    return drive_lbls


class MainApp(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master, background=BACKGROUND)
        self.get_os_type()
        self.current_dir = StringVar()
        self.current_search = StringVar()
        self.render_toolbar()
        self.render_main_frame()
        self.pack()

    def get_os_type(self):
        if sys.platform.startswith('darwin'):
            self.OS_TYPE = "Mac"
        elif os.name == "nt":
            self.OS_TYPE = "Windows"
        else:
            self.OS_TYPE = "Unix"

    def render_toolbar(self):
        self.master.update()
        self.toolbar = Frame(self.master, bd=1, relief=RAISED)
        self.create_buttons()
        self.nav_bar = Entry(self.toolbar, textvariable=self.current_dir, font=("Source Code Pro", "12"), relief=FLAT)
        self.current_dir.set(os.getcwd())
        self.nav_bar.pack(side=LEFT, padx=2, fill=X, expand=True)
        self.search_bar = Entry(self.toolbar, textvariable=self.current_search, font=("Source Code Pro", "12"),
                                foreground="grey")
        self.current_search.set("Search")
        self.search_bar.pack(side=RIGHT)
        self.toolbar.pack(side=TOP, fill=X)

    def render_main_frame(self):
        self.main_frame = Frame(self.master)
        self.tree_sidebar = ttk.Treeview(self.main_frame, show='tree')
        self.fill_treeview()
        self.tree_sidebar.pack(side=LEFT, pady=2, fill=BOTH, expand=True)
        self.main_frame.pack(side=TOP, fill=BOTH, expand=True)

    def get_subdirs(self, parent_dir):
        try:
            subdirs = [name for name in os.listdir(parent_dir)
                       if os.path.isdir(os.path.join(parent_dir, name))]
        except:
            return
        for sub in subdirs:
            self.tree_sidebar.insert(parent_dir, 'end', os.path.join(parent_dir, sub), text=sub)

    def fill_treeview(self):
        """
        Things to display top-level:
            - Bookmarks
                - Desktop
                - Documents
                - Downloads
            - Show all active mounted drives
            - LINUX:
                /home/
                /
            - WINDOWS:
                All drive letters [Name (Letter), or just Letter]
        """
        drives = get_used_drive_letters(self.OS_TYPE)
        for key in drives.keys():
            if key == drives[key]:
                self.tree_sidebar.insert('', 'end', key, text=drives[key])
            else:
                self.tree_sidebar.insert('', 'end', key, text="{} ({})".format(drives[key], key))
            self.get_subdirs(key)

    def create_buttons(self):
        #                              BACK
        # ---------------------------------
        # back_button_black = PhotoImage(file="icons/black_icons/Left-52.png")
        self.back_button = Button(self.toolbar, relief=FLAT, text="<-")
        self.back_button.pack(side=LEFT)
        # self.back_button.image = back_button_black
        #                           FORWARD
        # ---------------------------------
        # forward_button_black = PhotoImage(file="icons/black_icons/Right-52.png")
        self.forward_button = Button(self.toolbar, relief=FLAT, text="->")
        self.forward_button.pack(side=LEFT)
        # self.forward_button.grid(row=0, column=1)
        # self.forward_button.image = forward_button_black
