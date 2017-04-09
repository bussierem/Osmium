import os
import threading
import time
from threading import Thread, Timer
from tkinter import *
from PIL import Image, ImageTk


class Toolbar(Frame):
    def __init__(self, master):
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
        back_icon = Image.open('./resources/icons/back.png')
        self.back_img = ImageTk.PhotoImage(back_icon)
        self.back_button = Button(
            self,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            # text="<=",
            image=self.back_img,
            command=self.back
        )
        self.back_button.pack(side=LEFT)
        fwd_icon = Image.open('./resources/icons/forward.png')
        self.fwd_img = ImageTk.PhotoImage(fwd_icon)
        self.forward_button = Button(
            self,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            # text="=>",
            image=self.fwd_img,
            command=self.forward
        )
        self.forward_button.pack(side=LEFT)
        up_icon = Image.open('./resources/icons/up_level.png')
        self.up_img = ImageTk.PhotoImage(up_icon)
        self.up_button = Button(
            self,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            # text=" ^ ",
            image=self.up_img,
            command=self.up_level
        )
        self.up_button.pack(side=LEFT)
        refresh_icon = Image.open('./resources/icons/refresh.png')
        self.refresh_img = ImageTk.PhotoImage(refresh_icon)
        self.refresh_button = Button(
            self,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            # text="@",
            image=self.refresh_img,
            command=self.refresh
        )
        self.refresh_button.pack(side=LEFT)

    def render_navbar(self):
        self.nav_bar = Entry(
            self,
            textvariable=self.current_dir,
            font=("Source Code Pro", "12"),
            relief=FLAT
        )
        self.current_dir.set(self.master.history.cwd)
        self.nav_bar.pack(side=LEFT, padx=2, fill=X, expand=True)

    def render_searchbar(self):
        self.search_bar = Entry(
            self,
            textvariable=self.current_search,
            font=("Source Code Pro", "12"),
            foreground="grey"
        )
        self.current_search.set("Search {}".format(self.master.history.get_current_dir()))
        self.search_bar.pack(side=RIGHT)

    def set_dir(self, cwd):
        self.current_dir.set(cwd)
        self.current_search.set(
            "Search {}".format(self.master.history.get_current_dir())
        )

    #                                           EVENTS
    # ------------------------------------------------
    def on_search_click(self, event):
        if "Search {}".format(self.master.history.get_current_dir()) == self.search_bar.get():
            self.search_bar.delete(0, 'end')

    def on_enter(self, event):
        search_term = self.search_bar.get()
        self.master.file_explorer.main_tree.delete(
            *self.master.file_explorer.main_tree.get_children()
        )
        if hasattr(self, "search_thread") and self.search_thread is not None:
            if not self.search_thread.stopped():
                self.search_thread.stop()
                while not self.search_thread.get_progress()[0]:
                    time.sleep(0.1)
        self.search_thread = SearchThread(self, self.master.history.cwd, search_term)
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
            self.master.file_explorer.load_search_results(found)
        if not done:
            self.timer = Timer(1, self.update_search).start()

    def on_changed_dir(self, event):
        cwd = self.current_dir.get()
        self.master.directory_changed(cwd)

    def back(self):
        self.master.set_directory(self.master.history.back())

    def forward(self):
        self.master.set_directory(self.master.history.forward())

    def up_level(self):
        cur_path = self.master.history.cwd.split(os.path.sep)
        if len(cur_path) > 1:
            up_one = os.path.sep.join(cur_path[:-1])
            self.master.history.new_dir(up_one)
            self.master.set_directory(up_one)

    def refresh(self):
        self.master.refresh()

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
