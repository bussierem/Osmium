import threading
from threading import Thread, Timer
from tkinter import *

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
            if get_os_type() == 'Windows':
                self.icon_path = './resources/icons/folder_ico.ico'
            else:
                self.icon_path = '@./resources/icons/folder_ico.xbm'
            self.png_path = './resources/icons/folder_large.gif'
        else:
            if get_os_type() == 'Windows':
                self.icon_path = './resources/icons/file_ico.ico'
            else:
                self.icon_path = '@./resources/icons/file_ico.xbm'
            self.png_path = './resources/icons/file_large.gif'
        self.iconbitmap(self.icon_path)
        self.render_base_frame()
        self.render_properties()
        self.bind("<Escape>", lambda *ignore: self.destroy())

    def destroy(self):
        if hasattr(self, "sc") and self.sc is not None and not self.sc.stopped():
            self.sc.stop()
            while not self.sc.get_progress()[0]:
                time.sleep(0.1)
        if hasattr(self, "cc") and self.cc is not None and not self.cc.stopped():
            self.cc.stop()
            while not self.cc.get_progress()[0]:
                time.sleep(0.1)
        super().destroy()

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
        self.size_value = Label(
            self.props_frame, font=("Source Code Pro", "10"), foreground="gray",
            text="0"
        )
        self.size_value.grid(row=3, column=1, columnspan=2, sticky=W)
        self.get_size()
        # Contents (folder only)
        if self.is_folder:
            self.contents_lbl = Label(
                self.props_frame, font=("Source Code Pro", "10", "bold"), text="Contents: "
            )
            self.contents_lbl.grid(row=4, column=0, sticky=E)
            self.contents_value = Label(
                self.props_frame, font=("Source Code Pro", "10"), foreground="gray",
                text="0 folders, 0 files"
            )
            self.contents_value.grid(row=4, column=1, columnspan=2, sticky=W)
            self.get_folder_contents()
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
        self.sc = SizeChecker(self.path)
        size_thread = Thread(target=self.sc.get_size, args=())
        size_thread.daemon = True
        size_thread.start()
        self.update_size()

    def update_size(self):
        if not hasattr(self, "sc"):
            return
        if self.sc is None:
            return
        done, size = self.sc.get_progress()
        idx = 0
        while size >= 1024.0:
            size /= 1024.0
            idx += 1
        size_t = ["B", "KB", "MB", "GB", "TB"]
        size_str = "{0:.2f} {1}".format(size, size_t[idx])
        if not self.sc.stopped():
            self.size_value.configure(text=size_str)
        if not done:
            Timer(1, self.update_size).start()
        elif not self.sc.stopped():
            self.size_value.configure(foreground="black")

    def get_folder_contents(self):
        self.cc = ContentsChecker(self.path)
        contents_thread = Thread(target=self.cc.get_contents, args=())
        contents_thread.daemon = True
        contents_thread.start()
        self.update_contents()

    def update_contents(self):
        if not hasattr(self, "cc"):
            return
        if self.cc is None:
            return
        done, folders, files = self.cc.get_progress()
        contents = "{} folders, {} files".format(folders, files)
        if not self.sc.stopped():
            self.contents_value.configure(text=contents)
        if not done:
            Timer(1, self.update_contents).start()
        elif not self.cc.stopped():
            self.contents_value.configure(foreground="black")


class ContentsChecker(Thread):
    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.folders = 0
        self.files = 0
        self.done = False
        Thread.__init__(self)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def get_contents(self):
        for item in os.walk(self.path):
            if self.stopped():
                self.done = True
                return
            self.folders += len(item[1])
            self.files += len(item[2])
        self.done = True

    def get_progress(self):
        return self.done, self.folders, self.files


class SizeChecker(Thread):
    def __init__(self, path, *args, **kwargs):
        self.cur_size = 0
        self.path = path
        self.done = False
        Thread.__init__(self)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def get_size(self):
        if os.path.isfile(self.path):
            self.cur_size += os.path.getsize(self.path)
            self.done = True
            return
        for item in os.walk(self.path):
            for file in item[2]:
                if self.stopped():
                    self.done = True
                    return
                self.cur_size += os.path.getsize(os.path.join(item[0], file))
        self.done = True

    def get_progress(self):
        return self.done, self.cur_size
