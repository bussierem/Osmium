import os
import time
import tkinter.ttk as ttk
from collections import OrderedDict
from os import path
from tkinter import *


class FileExplorer(Frame):
    def __init__(self, master, app):
        self.master = master
        self.app = app
        Frame.__init__(self, master)
        # self.pack(expand=True, fill=BOTH, side=RIGHT)
        if sys.platform.startswith('darwin'):
            self.OS_TYPE = "Mac"
        elif os.name == "nt":
            self.OS_TYPE = "Windows"
        else:
            self.OS_TYPE = "Unix"
        self.sort_desc = True
        self.create_widgets()
        self.load_data()
        self.bind_events()

    def selection(self):
        return self.main_tree.focus()

    def bind_events(self):
        self.main_tree.bind('<Return>', self.on_enter)

    def create_widgets(self):
        f = Frame(self.master)
        f.grid(row=0, column=1, sticky=NSEW)
        # tree and scrollbars
        self.col_headers = OrderedDict([('', 0.3), ('Name', 5), ('Size', 1), ('Type', 1), ('Last Modified', 2)])
        self.main_tree = ttk.Treeview(
            f,
            columns=self.col_headers.keys(),
            displaycolumns=self.col_headers.keys(),
            show='headings'
        )
        ysb = ttk.Scrollbar(f, orient=VERTICAL, command=self.main_tree.yview)
        xsb = ttk.Scrollbar(f, orient=HORIZONTAL, command=self.main_tree.xview)
        self.main_tree['yscroll'] = ysb.set
        self.main_tree['xscroll'] = xsb.set
        # add to frame
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

    def load_data(self):
        # TODO:  Load list of files/folders from cwd()
        for idx, name in enumerate(self.col_headers.keys()):
            self.main_tree.heading(
                idx,
                text=name,
                command=lambda c=name: self._column_sort(c, self.sort_desc)
            )
        self.load_dir(os.path.expanduser('~'))

    def load_dir(self, cwd):
        self.main_tree.delete(*self.main_tree.get_children())
        for item in sorted(os.listdir(cwd)):
            self.display_cwd_item(os.path.join(cwd, item))

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
        # Type (ext) OR "Folder"
        type = item_type if item_type == "Folder" else "{} File".format(ext.upper())
        # Last Modified
        mod_time = time.localtime(path.getmtime(f))
        last_modified_12 = time.strftime("%m/%d/%y %I:%M:%S %p", mod_time)
        last_modified_24 = time.strftime("%m/%d/%y %H:%M:%S", mod_time)
        data = ('', filename, size_str, type, last_modified_12)
        self.main_tree.insert('', 'end', iid=f, values=data)

    #                                           EVENTS
    # ------------------------------------------------
    def on_enter(self, event):
        self.app.on_changed_dir(event)