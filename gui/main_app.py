import os
from tkinter import *


class MainApp(Frame):
    def __init__(self, master=None):
        self.master = master
        self.frame = Frame.__init__(self, master)
        self.pack()
        self.current_dir = StringVar()
        self.current_search = StringVar()
        self.createWidgets()

    def createWidgets(self):
        self.nav_frame = Frame(self.frame, bg="blue", padx=5)
        self.nav_frame.pack(side=TOP, fill=X, expand=1, )
        self.back_button = Button(self.nav_frame, text="<=")
        self.back_button.pack(side=LEFT, padx=3)
        self.forward_button = Button(self.nav_frame, text="=>")
        self.forward_button.pack(side=LEFT, padx=3)
        self.master.update()
        self.nav_bar = Entry(self.nav_frame, textvariable=self.current_dir)
        self.current_dir.set(os.getcwd())
        self.nav_bar.pack(side=LEFT, fill=X, expand=1, padx=3)
        self.search_bar = Entry(self.nav_frame, textvariable=self.current_search, foreground="grey")
        self.current_search.set("Search")
        self.search_bar.pack(side=LEFT, fill=X, ipadx=50, padx=3)
        self.bottom_frame = Frame(self.frame, bg="red", padx=5)
        self.bottom_frame.pack(side=TOP, fill=BOTH, expand=1)

    def say_hi(self):
        print("hi there, everyone!")
