import tkinter.ttk as ttk
from collections import OrderedDict
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

from utils.utilities import *
from handlers.compatibility import CompatibilityHandler

if os.name == 'nt':
    import win32api

class TreeSidebar(Frame):
    def __init__(self, master, parent_win):
        self.master = master
        self.parent_win = parent_win
        Frame.__init__(self, master)
        style = ttk.Style(self.master)
        self.row_height = SIDEBAR_ROW_HEIGHT
        style.configure('Sidebar.Treeview', rowheight=self.row_height)
        self.render_treeview()
        self.bind_events()
        self.fill_treeview()

    def bind_events(self):
        # Drag-and-Drop flags and events
        self.CLICK_DOWN = False
        self.DRAG_START = False
        self.START_EVENT = None
        self.END_EVENT = None
        # Events
        self.tree.bind("<<TreeviewOpen>>", self.item_opened)
        self.tree.bind("<Double-1>", self.item_double_clicked)
        self.tree.bind("<Button-1>", self.left_mouse_down)
        self.tree.bind("<ButtonRelease-1>", self.left_mouse_up)
        # self.tree.bind("<B1-Motion>", self.mouse_move)
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
        drives = CompatibilityHandler.get_used_drive_letters()
        for key in drives.keys():
            if key == drives[key]:
                self.tree.insert('', 'end', key, text=drives[key])
            else:
                self.tree.insert('', 'end', key, text="{} ({})".format(drives[key], key))
            self.get_subdirs(key)

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
            messagebox.showerror('Invalid Permissions', 'You do not have sufficient privileges to access ' + parent)
            return
        for sub in subdirs:
            if os.path.isdir(os.path.join(parent, sub)):
                self.get_subdirs(os.path.join(parent, sub))

    def item_clicked(self, event):
        cwd = self.tree.identify('item', event.x, event.y)
        if os.path.isdir(cwd):
            self.parent_win.directory_changed(cwd)

    def item_double_clicked(self, event):
        cwd = self.tree.identify('item', event.x, event.y)
        if os.path.isfile(cwd):
            open_file(cwd)
        else:
            self.on_changed_dir(event)

    def on_changed_dir(self, event):
        cwd = self.tree.selection()[0]
        self.parent_win.directory_changed(cwd)

    def remove_bookmark(self, event=None):
        path = self.tree.selection()[0]
        if 'bookmark' in self.tree.item(path)['tags']:
            bm_man = BookmarkManager()
            name = bm_man.get_bookmark_by_path(path)
            if name is not None and messagebox.askyesno(
                    "Confirm Bookmark Removal",
                    "Are you sure you want to remove the bookmark \"{}\"?".format(name)
            ):
                bm_man.remove_bookmark_by_path(path)
                self.refresh()

    def left_mouse_down(self, event):
        self.CLICK_DOWN = True
        self.START_EVENT = event

    def left_mouse_up(self, event):
        self.CLICK_DOWN = False
        self.END_EVENT = event
        if not self.DRAG_START:
            return
        if hasattr(self, "line"):
            self.line.destroy()
        bm_man = BookmarkManager()
        start_row = self.tree.identify_row(self.START_EVENT.y)
        end_row = self.tree.identify_row(self.END_EVENT.y)
        if end_row not in [b.full_path for b in bm_man.bookmarks]:
            return
        loc = self.compare_mouse_loc_to_rows(event, end_row)
        row_idx = [i for i, c in enumerate(self.tree.get_children()) if c == end_row][0]
        bookmark = bm_man.get_bookmark_by_path(start_row)
        if loc == "middle":
            return
        elif loc == "top":
            new_idx = row_idx - (0 if row_idx == 0 else 1)
        else:
            new_idx = row_idx
        bm_man.change_bookmark_index(bookmark, new_idx)
        self.refresh()

    def mouse_move(self, event):
        if not self.CLICK_DOWN:
            return
        if self.DRAG_START:
            self.check_if_draw(event)
        elif event.x > self.START_EVENT.x + 3 or event.y > self.START_EVENT.y + 3:
            self.DRAG_START = True
            self.check_if_draw(event)

    def check_if_draw(self, event):
        if event.y <= 0:
            if hasattr(self, "line"):
                self.line.destroy()
            return
        bm_man = BookmarkManager()
        row = self.tree.identify_row(event.y)
        if row not in [b.full_path for b in bm_man.bookmarks]:
            if hasattr(self, "line"):
                self.line.destroy()
            return
        loc = self.compare_mouse_loc_to_rows(event, row)
        if loc == "top":
            self.draw_line_above(row)
        elif loc == "bottom":
            self.draw_line_below(row)

    def compare_mouse_loc_to_rows(self, e, row):
        x, y, rw, rh = self.tree.bbox(row)
        if e.y <= (y + (rh / 3)):
            return "top"
        elif e.y >= ((y + rh) - (rh / 3)):
            return "bottom"
        return "middle"

    def draw_line_above(self, row):
        _, y, width, _ = self.tree.bbox(row)
        if hasattr(self, "line"):
            self.line.destroy()
        self.line = Frame(self.tree, height=2, width=width, bg="black")
        self.line.place(x=width / 4, y=y, anchor=W, width=width / 2)

    def draw_line_below(self, row):
        _, y, width, height = self.tree.bbox(row)
        pady = height
        if hasattr(self, "line"):
            self.line.destroy()
        self.line = Frame(self.tree, height=2, width=width, bg="black")
        self.line.place(x=width / 4, y=y + pady, anchor=W, width=width / 2)
