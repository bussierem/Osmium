import tkinter.ttk as ttk
from collections import OrderedDict
import os
from os import path
from tkinter import *

if os.name == 'nt':
    import win32con
    import win32api

from PIL import Image, ImageTk

import handlers.file_operations as fileops
from gui.popups.bookmark_popup import BookmarkPopup
from gui.popups.properties_popup import PropertiesPopup
from gui.popups.rename_popup import RenamePopup
from utils.bookmarks import *


class FileView(Frame):
    def __init__(self, master, parent_win):
        self.master = master
        self.parent_win = parent_win
        self.right_click_coords = (0, 0)
        Frame.__init__(self, master)
        self.sort_desc = True
        self.create_widgets()
        self.load_data()
        self.bind_events()

    def selection(self):
        return self.main_tree.focus()

    def bind_events(self):
        self.main_tree.bind('<Return>', self.on_changed_dir)
        self.main_tree.bind('<Double-1>', self.on_changed_dir)
        self.main_tree.bind('<Button-3>', self.render_right_click_menu)
        # Refresh
        self.main_tree.bind('<F5>', self.parent_win.on_refresh_dir)
        # Right-click functions
        self.main_tree.bind("<Control-d>", self.TODO)  # Tag
        self.main_tree.bind("<Control-Shift-d>", self.TODO)  # Un-tag
        self.main_tree.bind("<Control-b>", self.init_bookmark)  # Bookmark
        self.main_tree.bind("<Control-x>", self.on_cut)
        self.main_tree.bind("<Control-c>", self.on_copy)
        self.main_tree.bind("<Control-v>", self.on_paste)
        self.main_tree.bind("<F2>", self.rename_target)
        self.main_tree.bind("<Delete>", self.recycle_target)
        self.main_tree.bind("<Shift-Delete>", self.delete_target)

    def create_widgets(self):
        f = Frame(self.master)
        f.grid(row=0, column=1, sticky=NSEW)
        # tree and scrollbars
        self.col_headers = OrderedDict([('Name', 5), ('Size', 1), ('Type', 1), ('Last Modified', 2)])
        self.main_tree = ttk.Treeview(
            f,
            columns=self.col_headers.keys(),
            show='tree headings'
        )
        ysb = ttk.Scrollbar(f, orient=VERTICAL, command=self.main_tree.yview)
        xsb = ttk.Scrollbar(f, orient=HORIZONTAL, command=self.main_tree.xview)
        self.main_tree['yscroll'] = ysb.set
        self.main_tree['xscroll'] = xsb.set
        # add everything to frame
        self.main_tree.grid(row=0, column=0, sticky=NSEW)
        ysb.grid(row=0, column=1, sticky=NS)
        xsb.grid(row=1, column=0, sticky=EW)
        # resize frame
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)
        self.main_tree.update()
        # resize treeview columns
        # TODO:  I hate this.  I need a better way to decide relative column widths
        for idx, name in enumerate(self.col_headers.keys()):
            col_width = int(75 * self.col_headers[name])
            self.main_tree.column(idx, minwidth=100, width=col_width, stretch=NO)
        self.main_tree.column('#0', minwidth=10, width=50, stretch=NO, anchor=CENTER)

    def load_data(self):
        # TODO:  "Sort" by folder vs. file, THEN sort by name in each set!
        for idx, name in enumerate(self.col_headers.keys()):
            self.main_tree.heading(
                idx,
                text=name,
                command=lambda c=name: self._column_sort(c, self.sort_desc)
            )
        self.load_dir(os.path.expanduser('~'))
        icon = Image.open('./resources/icons/folder.gif')
        self.folder = ImageTk.PhotoImage(icon)
        icon = Image.open('./resources/icons/file.gif')
        self.file = ImageTk.PhotoImage(icon)
        self.main_tree.tag_configure('folder', image=self.folder)
        self.main_tree.tag_configure('file', image=self.file)

    def load_dir(self, cwd):
        self.main_tree.delete(*self.main_tree.get_children())
        sorted_list = self.sort_by_folder_first(cwd)
        for item in sorted_list:
            path = os.path.join(cwd, item)
            try:
                attribute = win32api.GetFileAttributes(path)
                if not (attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)):
                    self.display_cwd_item(path)
            except:
                # TODO: Need to figure out stupid permission errors
                self.display_cwd_item(path)

    def load_search_results(self, found):
        # TODO: ONLY UPDATE THE PART OF THE RESULTS THAT HASN'T BEEN DISPLAYED YET
        current_results = self.main_tree.get_children()
        new_items = [f for f in found if f not in current_results]
        new_items = sorted(new_items)
        for idx, item in enumerate(new_items):
            try:
                attribute = win32api.GetFileAttributes(item)
                if not (attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)):
                    self.display_cwd_item(item)
            except:
                # TODO: Need to figure out stupid permission errors
                self.display_cwd_item(item)

    def sort_by_folder_first(self, cwd):
        folders = []
        files = []
        for item in sorted(os.listdir(cwd)):
            path = os.path.join(cwd, item)
            if os.path.isdir(path):
                folders.append(item)
            else:
                files.append(item)
        all_items = sorted(folders)
        all_items.extend(sorted(files))
        return all_items

    def _column_sort(self, col, descending=False):
        # grab values to sort as a list of tuples (column value, column id)
        data = [(self.main_tree.set(child, col), child) for child in self.main_tree.get_children('')]
        data.sort(reverse=descending)
        for idx, item in enumerate(data):
            self.main_tree.move(item[1], '', idx)  # item[1] = item Identifier
        # reverse sort direction for next sort operation
        self.sort_desc = not descending

    def display_cwd_item(self, f):
        if path.isfile(f):
            item_type = "File"
        elif path.isdir(f):
            item_type = "Folder"
        else:
            item_type = "Unknown"
        # Name
        filename, ext = path.splitext(f)
        filename = filename.split(path.sep)[-1] + ext
        ext = ext[1:]
        # Size if file
        size_str = ""
        if item_type == "File":
            size = path.getsize(f)
            size_t = ["B", "KB", "MB", "GB", "TB"]
            idx = 0
            while size >= 1024.0:
                size /= 1024.0
                idx += 1
            size_str = "{0:.2f} {1}".format(size, size_t[idx])
        # Type "<ext> File" OR "Folder"
        type = item_type if item_type == "Folder" else "{} File".format(ext.upper())
        # Last Modified
        mod_time = time.localtime(path.getmtime(f))
        last_modified_12 = time.strftime("%m/%d/%y %I:%M:%S %p", mod_time)
        # last_modified_24 = time.strftime("%m/%d/%y %H:%M:%S", mod_time)
        data = (filename, size_str, type, last_modified_12)
        if type == "Folder":
            self.main_tree.insert('', 'end', iid=f, tags='folder', values=data)
        else:
            self.main_tree.insert('', 'end', iid=f, tags='file', values=data)

    def build_right_click_menu(self, properties, coords):
        self.parent_win.destroy_right_menus()
        self.right_menu = Menu(self.master, tearoff=0)
        menu_items_full = OrderedDict([
            ("Tag", self.TODO),
            ("Untag", self.TODO),
            ("Bookmark", self.init_bookmark),
            ("1", "SEP"),
            ("Cut", self.on_cut),
            ("Copy", self.on_copy),
            ("Paste", self.on_paste),
            ("2", "SEP"),
            ("Delete", self.recycle_target),
            ("Rename", self.rename_target),
            ("3", "SEP"),
            ("Properties", self.render_target_properties)
        ])
        menu_items_no_file = OrderedDict([
            ("New Folder", self.TODO),
            ("New File", self.TODO),
            ("1", "SEP"),
            ("Paste", self.on_paste),
            ("2", "SEP"),
            ("Properties", self.TODO)
        ])
        if properties != {}:
            render_items = menu_items_full
        else:
            render_items = menu_items_no_file
        for lbl, cmd in render_items.items():
            if cmd == "SEP":
                self.right_menu.add_separator()
            elif cmd == self.TODO:
                self.right_menu.add_command(label=lbl, command=cmd, state=DISABLED)
            else:
                self.right_menu.add_command(label=lbl, command=cmd)
        x, y = coords
        self.right_menu.post(x, y)

    def TODO(self, event=None):
        print("TODO:  This event still needs to be completed/linked!")

    #                                           EVENTS
    # ------------------------------------------------
    def on_changed_dir(self, event):
        if len(self.main_tree.selection()) == 0:
            return
        cwd = self.main_tree.selection()[0]
        self.parent_win.on_changed_dir(cwd)

    def on_cut(self, event=None):
        item = self.main_tree.selection()[0]
        write_clipboard(item, os.path.isfile(item))
        fileops.cut_file(item)

    def on_copy(self, event=None):
        item = self.main_tree.selection()[0]
        write_clipboard(item, os.path.isfile(item))
        fileops.copy_file(item)

    def on_paste(self, event=None):
        if event is None:
            dest = self.master.history.get_current_dir()
        else:
            sel = self.main_tree.selection()
            dest = sel[0] if sel else self.master.history.get_full_cwd()
            if os.path.isfile(dest):
                dest = self.master.history.get_full_cwd()
        fileops.paste_file(dest, self.paste_thread_finished)

    def recycle_target(self, event=None):
        if event.widget == self.main_tree:
            sel = self.main_tree.selection()[0]
            fileops.recycle_file(sel, self.parent_win.on_refresh_dir)

    def delete_target(self, event=None):
        if event.widget == self.main_tree:
            sel = self.main_tree.selection()[0]
            fileops.delete_file(sel, self.parent_win.on_refresh_dir)

    def rename_target(self, event=None):
        if event is not None:  # Called with keyboard
            if event.widget != self.main_tree:
                return
            else:
                row = self.main_tree.selection()[0]
                col = "#1"
        else:  # Called from Right-click menu
            col = self.main_tree.identify_column(self.right_click_coords[0])
            row = self.main_tree.identify_row(self.right_click_coords[1])
        _, y, _, height = self.main_tree.bbox(row, col)
        padx = self.main_tree.column("#0")['width']  # don't need to overlap the icon
        pady = height // 2
        width = self.main_tree.column(col)['width']
        self.rename_popup = RenamePopup(self.main_tree, row, self.parent_win)
        self.rename_popup.place(x=0 + padx, y=y + pady, anchor=W, width=width)

    def init_bookmark(self, event=None):
        if event is not None and event.widget != self.main_tree:
            return
        sel = self.main_tree.selection()[0]
        popup = BookmarkPopup(self, self.parent_win, sel)
        self.master.wait_window(popup)

    def bookmark_target(self, path, name):
        bm_man = BookmarkManager()
        bm_man.add_bookmark(path, name)
        self.parent_win.refresh_bookmark_bar()

    def render_target_properties(self, event=None):
        if event is not None and event.widget != self.main_tree:
            return
        sel = self.main_tree.selection()[0]
        pop = PropertiesPopup(self, self.parent_win, sel)
        self.master.wait_window(pop)

    def paste_thread_finished(self, item):
        self.parent_win.on_refresh_dir()

    def render_right_click_menu(self, event):
        self.right_click_coords = (event.x, event.y)
        widget = self.winfo_containing(event.x_root, event.y_root)
        props = {}
        # Clicked one of the rows
        if widget.identify_region(event.x, event.y) in ['tree', 'cell']:
            item = widget.identify_row(event.y)
            widget.selection_set([item])
            # TODO:  Check for tags when implemented
            props['tag'] = False
            props['folder'] = True if self.main_tree.tag_has('folder', item) else False
        # Clicked on empty space in the tree
        elif widget.identify_region(event.x, event.y) == 'nothing':
            widget.selection_clear()
        # Clicked a header
        else:
            return
        self.build_right_click_menu(props, (event.x_root, event.y_root))
