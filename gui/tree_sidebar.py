import os
import win32api
from collections import OrderedDict
from tkinter import *
from tkinter.ttk import *


class TreeSidebar(Treeview):
    def __init__(self, master, **kw):
        Treeview.__init__(self, master, **kw)
        if sys.platform.startswith('darwin'):
            self.OS_TYPE = "Mac"
        elif os.name == "nt":
            self.OS_TYPE = "Windows"
        else:
            self.OS_TYPE = "Unix"
        self.bind_events()
        self.fill_treeview()

    def bind_events(self):
        # self.bind("<<TreeviewOpen>>", self.item_opened)
        # self.bind("<Button-1>", self.item_clicked)
        pass

    def get_subdirs(self, parent_dir):
        try:
            subdirs = [name for name in os.listdir(parent_dir)
                       if os.path.isdir(os.path.join(parent_dir, name))]
        except:
            return
        for sub in subdirs:
            self.insert(parent_dir, 'end', os.path.join(parent_dir, sub), text=sub)

    def fill_treeview(self):
        for loc in ['Desktop', 'Documents', 'Downloads']:
            path = os.path.join(os.path.expanduser('~'), loc)
            self.insert('', 'end', path, text=loc)
        drives = self.get_used_drive_letters(self.OS_TYPE)
        for key in drives.keys():
            if key == drives[key]:
                self.insert('', 'end', key, text=drives[key])
            else:
                self.insert('', 'end', key, text="{} ({})".format(drives[key], key))
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
        parent = self.selection()[0]
        for d in [sub for sub in os.listdir(parent) if os.path.isdir(os.path.join(parent, sub))]:
            self.get_subdirs(os.path.join(parent, d))

    def item_clicked(self, event):
        loc = self.identify('item', event.x, event.y)
        # TODO:  Call "goto location" method
