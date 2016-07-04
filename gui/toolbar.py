import os
from tkinter import *


class Toolbar(Frame):
    def __init__(self, master, app):
        self.app = app
        self.master = master
        self.current_dir = StringVar()
        self.current_search = StringVar()
        Frame.__init__(self, master)
        self.render_buttons()
        self.render_navbar()
        self.render_searchbar()
        self.bind_events()
        self.pack(side=TOP, fill=X)

    def bind_events(self):
        self.nav_bar.bind('<Return>', self.on_changed_dir)
        self.search_bar.bind('<Button-1>', self.on_search_click)
        self.search_bar.bind('<Return>', self.on_enter)

    def render_buttons(self):
        self.back_button = Button(
            self,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            text="<=",
            command=self.back
        )
        self.back_button.pack(side=LEFT)
        self.forward_button = Button(
            self,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            text="=>",
            command=self.forward
        )
        self.forward_button.pack(side=LEFT)
        self.up_button = Button(
            self,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            text=" ^ ",
            command=self.up_level
        )
        self.up_button.pack(side=LEFT)

    def render_navbar(self):
        self.nav_bar = Entry(
            self,
            textvariable=self.current_dir,
            font=("Source Code Pro", "12"),
            relief=FLAT
        )
        self.current_dir.set(self.app.HISTORY.cwd)
        self.nav_bar.pack(side=LEFT, padx=2, fill=X, expand=True)

    def render_searchbar(self):
        self.search_bar = Entry(
            self,
            textvariable=self.current_search,
            font=("Source Code Pro", "12"),
            foreground="grey"
        )
        self.current_search.set("Search {}".format(self.app.HISTORY.get_current_dir()))
        self.search_bar.pack(side=RIGHT)

    def set_dir(self, cwd):
        self.current_dir.set(cwd)
        self.current_search.set(
            "Search {}".format(self.app.HISTORY.get_current_dir())
        )

    #                                           EVENTS
    # ------------------------------------------------
    def on_search_click(self, event):
        self.search_bar.delete(0, 'end')

    def on_enter(self, event):
        print("TODO:  Implement 'Search' method")

    def on_changed_dir(self, event):
        cwd = self.current_dir.get()
        self.app.on_changed_dir(cwd)

    def back(self):
        self.app.change_dir(self.app.HISTORY.back())

    def forward(self):
        self.app.change_dir(self.app.HISTORY.forward())

    def up_level(self):
        up_one = os.path.sep.join(self.app.HISTORY.cwd.split(os.path.sep)[:-1])
        self.app.HISTORY.new_dir(up_one)
        self.app.change_dir(up_one)
