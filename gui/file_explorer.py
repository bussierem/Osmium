import os
import sys
import tkinter.ttk as ttk
from tkinter import *


class FileExplorer(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, master)
        # self.pack(expand=True, fill=BOTH, side=RIGHT)
        if sys.platform.startswith('darwin'):
            self.OS_TYPE = "Mac"
        elif os.name == "nt":
            self.OS_TYPE = "Windows"
        else:
            self.OS_TYPE = "Unix"
        self.sort_desc = True
        self.bind_events()
        self.create_widgets()
        self.load_data()

    def bind_events(self):
        # TODO: Bind events
        pass

    def create_widgets(self):
        f = Frame(self.master)
        f.grid(row=0, column=1, sticky=NSEW)
        # tree and scrollbars
        self.col_headers = ('Name', 'Size', 'Last Modified')
        self.main_tree = ttk.Treeview(f, columns=self.col_headers, show='headings')
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
        f.columnconfigure(0, weight=9)

    def load_data(self):
        # TODO:  Load list of files/folders from cwd()
        for c in self.col_headers:
            self.main_tree.heading(c, text=c.title(),
                                   command=lambda c=c: self._column_sort(c, self.sort_desc))
            self.main_tree.column(c)

    def _column_sort(self, col, descending=False):
        # grab values to sort as a list of tuples (column value, column id)
        data = [(self.main_tree.set(child, col), child) for child in self.main_tree.get_children('')]
        data.sort(reverse=descending)
        for idx, item in enumerate(data):
            self.main_tree.move(item[1], '', idx)  # item[1] = item Identifier
        # reverse sort direction for next sort operation
        self.sort_desc = not descending
