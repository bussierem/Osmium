import os
from tkinter import *
from tkinter import ttk

from gui.file_explorer import FileExplorer
from gui.tree_sidebar import TreeSidebar

LIGHT_TEAL = "#00e6e6"
DARK_TEAL = "#009999"
BACKGROUND = "#6F807F"


class MainApp(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master, background=BACKGROUND)
        if sys.platform.startswith('darwin'):
            self.OS_TYPE = "Mac"
        elif os.name == "nt":
            self.OS_TYPE = "Windows"
        else:
            self.OS_TYPE = "Unix"
        self.current_dir = StringVar()
        self.current_search = StringVar()
        self.render_toolbar()
        self.render_main_frame()
        self.pack()

    def render_toolbar(self):
        self.master.update()
        self.toolbar = Frame(self.master, bd=1, relief=RAISED)
        self.create_buttons()
        self.nav_bar = Entry(
            self.toolbar,
            textvariable=self.current_dir,
            font=("Source Code Pro", "12"),
            relief=FLAT
        )
        self.current_dir.set(os.getcwd())
        self.nav_bar.pack(side=LEFT, padx=2, fill=X, expand=True)
        self.search_bar = Entry(
            self.toolbar,
            textvariable=self.current_search,
            font=("Source Code Pro", "12"),
            foreground="grey"
        )
        self.current_search.set("Search {}".format(os.path.expanduser('~')))
        self.search_bar.bind('<Button-1>', self.clear_search_bar)
        self.search_bar.bind('<Return>', self.handle_enter)
        self.search_bar.pack(side=RIGHT)
        self.toolbar.pack(side=TOP, fill=X)

    def clear_search_bar(self, event):
        self.search_bar.delete(0, 'end')

    def handle_enter(self, event):
        f_widget = event.widget
        if f_widget == self.search_bar:
            # TODO:  Call searching here
            print("TODO:  Call search method")
        elif f_widget == self.nav_bar:
            # TODO:  Call "go to location" here
            print("TODO:  Call 'goto location' method")

    def create_buttons(self):
        self.back_button = Button(
            self.toolbar,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            text="<="
        )
        self.back_button.pack(side=LEFT)
        self.forward_button = Button(
            self.toolbar,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            text="=>"
        )
        self.forward_button.pack(side=LEFT)

    def render_main_frame(self):
        self.main_frame = Frame(self.master, background="red")
        self.render_tree_sidebar()
        self.render_file_grid()
        self.main_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=9)
        self.main_frame.rowconfigure(0, weight=1)

    def render_tree_sidebar(self):
        self.tree_frame = Frame(self.main_frame)
        self.tree_sidebar = TreeSidebar(self.tree_frame, show='tree')
        self.tree_y_scroll = ttk.Scrollbar(
            self.tree_frame, orient='vertical', command=self.tree_sidebar.yview
        )
        self.tree_x_scroll = ttk.Scrollbar(
            self.tree_frame, orient='horizontal', command=self.tree_sidebar.xview
        )
        self.tree_sidebar.configure(yscroll=self.tree_y_scroll.set, xscroll=self.tree_x_scroll.set)
        self.tree_sidebar.grid(row=0, column=0, sticky=NSEW)
        self.tree_y_scroll.grid(row=0, column=1, sticky=NS)
        self.tree_x_scroll.grid(row=1, column=0, sticky=EW)
        self.tree_frame.grid(row=0, column=0, sticky=NSEW)
        # Make sure it expands to fit frame
        self.tree_frame.rowconfigure(0, weight=1)
        self.tree_frame.columnconfigure(0, weight=1)

    def render_file_grid(self):
        self.file_explorer = FileExplorer(self.main_frame)
