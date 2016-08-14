import os
import threading
import time
from threading import Thread, Timer
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

    def destroy(self):
        if hasattr(self, "search_thread"):
            self.search_thread.stop()
            while not self.search_thread.get_progress()[0]:
                time.sleep(0.1)
        if hasattr(self, "timer") and self.timer is not None:
            assert isinstance(self.timer, Timer)
            if self.timer.is_alive():
                self.timer.cancel()
        super().destroy()

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
        if "Search {}".format(self.app.HISTORY.get_current_dir()) == self.search_bar.get():
            self.search_bar.delete(0, 'end')

    def on_enter(self, event):
        search_term = self.search_bar.get()
        self.app.file_explorer.main_tree.delete(
            *self.app.file_explorer.main_tree.get_children()
        )
        if hasattr(self, "search_thread") and self.search_thread is not None:
            if not self.search_thread.stopped():
                self.search_thread.stop()
                while not self.search_thread.get_progress()[0]:
                    time.sleep(0.1)
        self.search_thread = SearchThread(self, self.app.HISTORY.cwd, search_term)
        self.search_daemon = Thread(target=self.search_thread.find_results, args=())
        self.search_daemon.daemon = True
        self.search_daemon.start()
        self.update_search()

    def update_search(self):
        if not hasattr(self, "search_thread"):
            return
        if self.search_thread is None:
            return
        done, found = self.search_thread.get_progress()
        if not self.search_thread.stopped():
            self.app.file_explorer.load_search_results(found)
        if not done:
            self.timer = Timer(1, self.update_search).start()

    def on_changed_dir(self, event):
        cwd = self.current_dir.get()
        self.app.on_changed_dir(cwd)

    def back(self):
        self.app.change_dir(self.app.HISTORY.back())

    def forward(self):
        self.app.change_dir(self.app.HISTORY.forward())

    def up_level(self):
        cur_path = self.app.HISTORY.cwd.split(os.path.sep)
        if len(cur_path) > 1:
            up_one = os.path.sep.join(cur_path[:-1])
            self.app.HISTORY.new_dir(up_one)
            self.app.change_dir(up_one)


class SearchThread(Thread):
    def __init__(self, parent, path, search_term, *args, **kwargs):
        self.parent = parent
        self.found = []
        self.path = path
        self.search = search_term
        self.done = False
        Thread.__init__(self)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def find_results(self):
        for item in os.walk(self.path):
            base = item[0]
            if self.stopped():
                self.done = True
                return
            for folder in item[1]:
                if self.search in folder:
                    self.found.append(os.path.join(base, folder))
            for file in item[2]:
                if self.search in file:
                    self.found.append(os.path.join(base, file))
        self.done = True

    def get_progress(self):
        return self.done, self.found
