from tkinter import *

from utils.utilities import *


class BookmarkPopup(Toplevel):
    def __init__(self, parent, app, path, **kw):
        super().__init__(**kw)
        self.parent = parent
        self.app = app
        self.path = path
        self.render_widgets()
        self.bind("<FocusOut>", lambda *ignore: self.destroy())
        self.bind("<Return>", lambda *ignore: self.save_bookmark())

    def render_widgets(self):
        self.form_frame = Frame(self, padx=10, pady=10)
        self.form_frame.pack(side=TOP, expand=True)
        self.lbl = Label(self.form_frame, text="Bookmark Label:  ")
        self.lbl.pack(side=LEFT)
        self.name = Entry(self.form_frame, width=50)
        self.name.pack(side=LEFT)
        data = os.path.split(self.path)[1]
        self.name.insert(0, data)
        self.name.focus_force()
        self.name.selection_range(0, len(data))
        self.name.icursor(len(data))
        self.btn_frame = Frame(self, padx=5, pady=5)
        self.btn_frame.pack(side=TOP, expand=True, fill=X)
        self.cancel_btn = Button(
            self.btn_frame, text="Cancel", width=10,
            command=self.destroy)
        self.cancel_btn.pack(side=LEFT, expand=True)
        self.submit_btn = Button(
            self.btn_frame, text="Save", width=10,
            command=self.save_bookmark)
        self.submit_btn.pack(side=LEFT, expand=True)

    def save_bookmark(self):
        name = self.name.get()
        self.parent.bookmark_target(self.path, name)
        self.destroy()
