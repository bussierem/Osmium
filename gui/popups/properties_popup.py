from tkinter import *

import win32com.client as com

from utils.utilities import *


class PropertiesPopup(Toplevel):
    def __init__(self, parent, app, path, **kw):
        super().__init__(**kw)
        self.parent = parent
        self.app = app
        self.path = path
        self.wm_title("{} Properties".format(os.path.splitext(os.path.split(path)[1])[0]))
        self.is_folder = os.path.isdir(self.path)
        if self.is_folder:
            self.icon_path = r'./icons/folder_ico.ico'
            self.png_path = r'./icons/folder_large.gif'
        else:
            self.icon_path = r'./icons/file_ico.ico'
            self.png_path = r'./icons/file_large.gif'
        self.iconbitmap(self.icon_path)
        self.render_base_frame()
        self.render_properties()
        self.bind("<Escape>", lambda *ignore: self.destroy())
        self.bind("<Return>", lambda *ignore: self.destroy())

    def render_base_frame(self):
        self.form_frame = Frame(self, padx=10)
        self.form_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.img_name_frame = Frame(self.form_frame, padx=10, pady=10)
        self.img_name_frame.pack(side=TOP, fill=X, expand=True)
        self.gif_img = PhotoImage(file=self.png_path)
        self.icon_lbl = Label(self.img_name_frame, image=self.gif_img)
        self.icon_lbl.image = self.gif_img
        self.icon_lbl.pack(side=LEFT, expand=True)
        self.name = Entry(self.img_name_frame, width=50)
        self.name.pack(side=LEFT, padx=10)
        data = os.path.split(self.path)[1]
        self.name.insert(0, data)
        self.name.focus_force()
        self.name.selection_range(0, len(data))
        self.name.icursor(len(data))
        self.props_frame = Frame(self, padx=10, pady=5)
        self.props_frame.pack(side=TOP, fill=BOTH, expand=True)

    def render_properties(self):
        # Type
        self.type_lbl = Label(
            self.props_frame, font=("Source Code Pro", "10", "bold"), text="Type: "
        )
        self.type_lbl.grid(row=0, column=0, sticky=E)
        if self.is_folder:
            type = "Folder"
        else:
            type = "{} File".format(os.path.splitext(self.path)[1][1:].upper())
        self.type_value = Label(
            self.props_frame, font=("Source Code Pro", "10"), text=type
        )
        self.type_value.grid(row=0, column=1, columnspan=2, sticky=W)
        # Opens With (files only)
        # TODO: Do this one  (ROW 1)
        # TODO: "Change" button??  (COL 3)
        # Location
        self.location_lbl = Label(
            self.props_frame, font=("Source Code Pro", "10", "bold"), text="Location: "
        )
        self.location_lbl.grid(row=2, column=0, sticky=E)
        self.location_value = Label(
            self.props_frame, font=("Source Code Pro", "10"), text=self.path
        )
        self.location_value.grid(row=2, column=1, columnspan=2, sticky=W)
        # Size
        self.size_lbl = Label(
            self.props_frame, font=("Source Code Pro", "10", "bold"), text="Size: "
        )
        self.size_lbl.grid(row=3, column=0, sticky=E)
        size_str = self.get_size()
        self.size_value = Label(
            self.props_frame, font=("Source Code Pro", "10"), text=size_str
        )
        self.size_value.grid(row=3, column=1, columnspan=2, sticky=W)
        # Contents (folder only)
        if self.is_folder:
            self.contents_lbl = Label(
                self.props_frame, font=("Source Code Pro", "10", "bold"), text="Contents: "
            )
            self.contents_lbl.grid(row=4, column=0, sticky=E)
            folders, files = self.get_folder_contents()
            contents = "{} folders, {} files".format(folders, files)
            self.contents_value = Label(
                self.props_frame, font=("Source Code Pro", "10"), text=contents
            )
            self.contents_value.grid(row=4, column=1, columnspan=2, sticky=W)
        # Created Date
        self.created_lbl = Label(
            self.props_frame, font=("Source Code Pro", "10", "bold"), text="Created: "
        )
        self.created_lbl.grid(row=5, column=0, sticky=E)
        create_t = time.localtime(os.path.getctime(self.path))
        create_str = time.strftime("%A %B %d, %Y - %I:%M:%S %p", create_t)
        self.created_value = Label(
            self.props_frame, font=("Source Code Pro", "10"), text=create_str
        )
        self.created_value.grid(row=5, column=1, columnspan=2, sticky=W)
        # Modified Date
        self.modified_lbl = Label(
            self.props_frame, font=("Source Code Pro", "10", "bold"), text="Last Modified: "
        )
        self.modified_lbl.grid(row=6, column=0, sticky=E)
        mod_t = time.localtime(os.path.getmtime(self.path))
        mod_str = time.strftime("%A %B %d, %Y - %I:%M:%S %p", mod_t)
        self.modified_value = Label(
            self.props_frame, font=("Source Code Pro", "10"), text=mod_str
        )
        self.modified_value.grid(row=6, column=1, columnspan=2, sticky=W)

    def get_size(self):
        size = 0
        if self.is_folder:
            fso = com.Dispatch("Scripting.FileSystemObject")
            try:
                # TODO:  Stick this into a thread and query it every 1s
                folder = fso.GetFolder(self.path)
                size = folder.Size
            except:
                pass
        else:
            size = os.path.getsize(self.path)
        idx = 0
        while size >= 1024.0:
            size /= 1024.0
            idx += 1
        size_t = ["B", "KB", "MB", "GB", "TB"]
        size_str = "{0:.2f} {1}".format(size, size_t[idx])
        return size_str

    def get_folder_contents(self):
        folders = 0
        files = 0
        for item in os.walk(self.path):
            folders += len(item[1])
            files += len(item[2])
        return folders, files
