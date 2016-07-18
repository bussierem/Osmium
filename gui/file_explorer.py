import tkinter.ttk as ttk
import win32api
from collections import OrderedDict
from os import path
from tkinter import *

import win32con
from PIL import Image, ImageTk

import handlers.file_operations as fileops
from utils.utilities import *


class FileExplorer(Frame):
    def __init__(self, master, app):
        self.master = master
        self.app = app
        Frame.__init__(self, master)
        self.OS_TYPE = get_os_type()
        self.sort_desc = True
        self.create_widgets()
        self.load_data()
        # self.build_right_click_menu()
        self.bind_events()

    def selection(self):
        return self.main_tree.focus()

    def bind_events(self):
        self.main_tree.bind('<Return>', self.on_changed_dir)
        self.main_tree.bind('<Double-1>', self.on_changed_dir)
        self.main_tree.bind('<Button-3>', self.render_right_click_menu)
        # Right-click functions
        self.main_tree.bind("<Control-d>", self.TODO)
        self.main_tree.bind("<Control-Shift-d>", self.TODO)
        self.main_tree.bind("<Control-b>", self.TODO)
        self.main_tree.bind("<Control-x>", self.on_cut)
        self.main_tree.bind("<Control-c>", self.on_copy)
        self.main_tree.bind("<Control-v>", self.on_paste)
        self.main_tree.bind("<Delete>", self.TODO)
        self.main_tree.bind("<Shift-Delete>", self.TODO)

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
        icon = Image.open('./icons/folder.gif')
        self.folder = ImageTk.PhotoImage(icon)
        icon = Image.open('./icons/file.gif')
        self.file = ImageTk.PhotoImage(icon)
        self.main_tree.tag_configure('folder', image=self.folder)
        self.main_tree.tag_configure('file', image=self.file)

    def load_dir(self, cwd):
        self.main_tree.delete(*self.main_tree.get_children())
        for item in sorted(os.listdir(cwd)):
            path = os.path.join(cwd, item)
            try:
                attribute = win32api.GetFileAttributes(path)
                if not (attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)):
                    self.display_cwd_item(path)
            except:
                # TODO: Need to figure out stupid permission errors
                self.display_cwd_item(path)

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
        data = (filename, size_str, type, last_modified_12)
        if type == "Folder":
            self.main_tree.insert('', 'end', iid=f, tags='folder', values=data)
        else:
            self.main_tree.insert('', 'end', iid=f, tags='file', values=data)

    def build_right_click_menu(self, properties, coords):
        self.b2_menu = Menu(self.master, tearoff=0)
        if properties['tag'] == False:
            self.b2_menu.add_command(label="Tag", command=self.TODO)
        else:
            self.b2_menu.add_command(label="Untag", command=self.TODO)
        if properties['folder'] == True:
            self.b2_menu.add_command(label="Bookmark", command=self.TODO)
        self.b2_menu.add_separator()
        self.b2_menu.add_command(label="Cut", command=self.on_cut)
        self.b2_menu.add_command(label="Copy", command=self.on_copy)
        self.b2_menu.add_command(label="Paste", command=self.on_paste)
        self.b2_menu.add_separator()
        self.b2_menu.add_command(label="Recycle", command=self.TODO)
        self.b2_menu.add_command(label="Delete", command=self.TODO)
        self.b2_menu.add_command(label="Rename", command=self.TODO)
        self.b2_menu.add_separator()
        self.b2_menu.add_command(label="Properties", command=self.TODO)
        x, y = coords
        self.b2_menu.post(x, y)

    def TODO(self, event=None):
        # TODO:  Linking all commands to here until implemented
        pass

    #                                           EVENTS
    # ------------------------------------------------
    def on_changed_dir(self, event):
        cwd = self.main_tree.selection()[0]
        self.app.on_changed_dir(cwd)

    def on_cut(self, event):
        item = self.main_tree.selection()[0]
        write_clipboard(item, os.path.isfile(item))
        fileops.cut_file(item)

    def on_copy(self, event):
        item = self.main_tree.selection()[0]
        write_clipboard(item, os.path.isfile(item))
        fileops.copy_file(item)

    def on_paste(self, event=None):
        if event is None:
            dest = self.app.HISTORY.get_current_dir()
        else:
            sel = self.main_tree.selection()
            dest = sel[0] if sel else self.app.HISTORY.get_full_cwd()
            if os.path.isfile(dest):
                dest = self.app.HISTORY.get_full_cwd()
        fileops.paste_file(dest, self.paste_thread_finished)

    def paste_thread_finished(self, item):
        self.app.on_changed_dir(self.app.HISTORY.get_full_cwd())

    def render_right_click_menu(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        # Make sure they didn't click the headers
        if widget.identify_region(event.x, event.y) in ['tree', 'cell']:
            item = widget.identify_row(event.y)
            widget.selection_set([item])
            props = {}
            # TODO:  Check for tags when implemented
            props['tag'] = False
            props['folder'] = True if self.main_tree.tag_has('folder', item) else False
            self.build_right_click_menu(props, (event.x_root, event.y_root))
