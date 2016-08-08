import tkinter.ttk as ttk
import win32api
from collections import OrderedDict
from tkinter import *

from PIL import Image, ImageTk

from utils.bookmarks import *


class TreeSidebar(Frame):
    def __init__(self, master, app):
        self.master = master
        self.app = app
        Frame.__init__(self, master)
        self.OS_TYPE = get_os_type()
        style = ttk.Style(self.master)
        self.row_height = SIDEBAR_ROW_HEIGHT
        style.configure('Sidebar.Treeview', rowheight=self.row_height)
        self.render_treeview()
        self.bind_events()
        self.fill_treeview()

    def bind_events(self):
        self.tree.bind("<<TreeviewOpen>>", self.item_opened)
        self.tree.bind("<Button-1>", self.item_clicked)
        self.tree.bind("<Double-1>", self.item_double_clicked)
        self.tree.bind("<Control-F5>", self.refresh)
        self.tree.bind("<Delete>", self.remove_bookmark)

    def render_treeview(self):
        self.tree = ttk.Treeview(self, show='tree', style='Sidebar.Treeview')
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
            try:
                self.tree.insert(parent_dir, 'end', os.path.join(parent_dir, sub), text=sub)
            except Exception:
                pass
        self.tree.item(parent_dir)

    def fill_treeview(self):
        icon = Image.open('./icons/folder.gif')
        self.folder = ImageTk.PhotoImage(icon)
        icon = Image.open('./icons/file.gif')
        self.file = ImageTk.PhotoImage(icon)
        bm_man = BookmarkManager()
        for bm in bm_man.bookmarks:
            assert isinstance(bm, Bookmark)
            if bm.type == "folder":
                self.tree.insert('', 'end', bm.full_path, image=self.folder, text=bm.name, tags=('bookmark'))
            elif bm.type == "file":
                self.tree.insert('', 'end', bm.full_path, image=self.file, text=bm.name, tags=('bookmark'))
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

    def refresh(self, event=None):
        self.tree.delete(*self.tree.get_children())
        self.fill_treeview()

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
        if os.path.isdir(cwd):
            self.app.on_changed_dir(cwd)

    def item_double_clicked(self, event):
        cwd = self.tree.identify('item', event.x, event.y)
        if os.path.isfile(cwd):
            open_file(cwd)

    def on_changed_dir(self, event):
        cwd = self.tree.selection()[0]
        self.app.on_changed_dir(cwd)

    def remove_bookmark(self, event=None):
        path = self.tree.selection()[0]
        if 'bookmark' in self.tree.item(path)['tags']:
            bm_man = BookmarkManager()
            name = bm_man.get_bookmark_by_path(path)
            if name is not None and messagebox.askyesno(
                    "Confirm Bookmark Removal",
                    "Are you sure you want to remove the bookmark \"{}\"".format(name)
            ):
                bm_man.remove_bookmark_by_path(path)
                self.refresh()
