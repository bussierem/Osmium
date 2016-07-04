import os
import tkinter.ttk as ttk
import win32api
from collections import OrderedDict
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk


class TreeSidebar(Frame):
    def __init__(self, master, app):
        self.master = master
        self.app = app
        Frame.__init__(self, master)
        if sys.platform.startswith('darwin'):
            self.OS_TYPE = "Mac"
        elif os.name == "nt":
            self.OS_TYPE = "Windows"
        else:
            self.OS_TYPE = "Unix"
        self.render_treeview()
        self.bind_events()
        self.fill_treeview()

    def bind_events(self):
        self.tree.bind("<<TreeviewOpen>>", self.item_opened)
        self.tree.bind("<Button-1>", self.item_clicked)

    def render_treeview(self):
        self.tree = ttk.Treeview(self, show='tree')
        self.render_scrollbars()
        self.grid(row=0, column=0, sticky=NSEW)
        # Make sure the tree expands to fit frame
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def render_scrollbars(self):
        self.tree_y_scroll = ttk.Scrollbar(
            self, orient='vertical', command=self.tree.yview
        )
        self.tree_x_scroll = ttk.Scrollbar(
            self, orient='horizontal', command=self.tree.xview
        )
        self.tree.configure(yscroll=self.tree_y_scroll.set, xscroll=self.tree_x_scroll.set)
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.tree_y_scroll.grid(row=0, column=1, sticky=NS)
        self.tree_x_scroll.grid(row=1, column=0, sticky=EW)

    def get_subdirs(self, parent_dir):
        try:
            subdirs = [name for name in os.listdir(parent_dir)
                       if os.path.isdir(os.path.join(parent_dir, name))]
        except:
            return
        for sub in subdirs:
            self.tree.insert(parent_dir, 'end', os.path.join(parent_dir, sub), text=sub)

    def fill_treeview(self):
        icon = Image.open('./icons/folder.gif')
        self.folder = ImageTk.PhotoImage(icon)
        for loc in ['Desktop', 'Documents', 'Downloads']:
            path = os.path.join(os.path.expanduser('~'), loc)
            self.tree.insert('', 'end', path, image=self.folder, text=loc)
        drives = self.get_used_drive_letters(self.OS_TYPE)
        for key in drives.keys():
            if key == drives[key]:
                self.tree.insert('', 'end', key, text=drives[key])
            else:
                self.tree.insert('', 'end', key, text="{} ({})".format(drives[key], key))
            self.get_subdirs(key)

    def get_used_drive_letters(self, os):
        drive_lbls = OrderedDict()
        if os == "Windows":
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
            drive_lbls = {'/': 'Root', '/home/': 'Home'}
        return drive_lbls

    #                              EVENT CALLBACKS
    # --------------------------------------------
    def item_opened(self, event):
        parent = self.tree.selection()[0]
        try:
            subdirs = os.listdir(parent)
        except PermissionError:
            _ = messagebox.showerror('Invalid Permissions', 'You do not have sufficient privileges to access ' + parent)
            return
        for sub in subdirs:
            if os.path.isdir(os.path.join(parent, sub)):
                self.get_subdirs(os.path.join(parent, sub))
        self.on_changed_dir(event)

    def item_clicked(self, event):
        cwd = self.tree.identify('item', event.x, event.y)
        self.app.on_changed_dir(cwd)

    def on_changed_dir(self, event):
        cwd = self.tree.selection()[0]
        self.app.on_changed_dir(cwd)
