import os
from tkinter import *
from tkinter import ttk

from gui.file_explorer import FileExplorer
from gui.tree_sidebar import TreeSidebar

LIGHT_TEAL = "#00e6e6"
DARK_TEAL = "#009999"
BACKGROUND = "#6F807F"


class History:
    def __init__(self):
        self.list = [os.path.expanduser('~')]
        self.index = 0
        self.update_cwd()

    def update_cwd(self):
        self.cwd = self.list[self.index]
        return self.cwd

    def back(self):
        self.index -= 1 if self.index > 0 else 0
        return self.update_cwd()

    def forward(self):
        self.index += 1 if self.index < (len(self.list) - 1) else 0
        return self.update_cwd()

    def get_current_dir(self):
        return self.cwd.split(os.path.sep)[-1]

    def new_dir(self, cwd):
        self.list = self.list[:self.index + 1]
        self.list.append(cwd)
        self.index += 1
        self.update_cwd()


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
        self.HISTORY = History()
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
        self.current_dir.set(self.HISTORY.cwd)
        self.nav_bar.pack(side=LEFT, padx=2, fill=X, expand=True)
        self.search_bar = Entry(
            self.toolbar,
            textvariable=self.current_search,
            font=("Source Code Pro", "12"),
            foreground="grey"
        )
        self.current_search.set("Search {}".format(self.HISTORY.get_current_dir()))
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

    def change_dir(self, cwd):
        self.current_dir.set(cwd)
        self.file_explorer.load_dir(cwd)
        self.current_search.set("Search {}".format(self.HISTORY.get_current_dir()))

    def on_changed_dir(self, event):
        if event.widget == self.nav_bar:
            cwd = self.current_dir
        elif event.widget == self.tree_sidebar:
            cwd = self.tree_sidebar.selection()[0]
        elif event.widget == self.file_explorer.main_tree:
            cwd = self.file_explorer.selection()
        else:
            return
        self.HISTORY.new_dir(cwd)  # EXPECTS FULL PATH
        print(self.HISTORY.list)
        self.change_dir(cwd)

    def create_buttons(self):
        self.back_button = Button(
            self.toolbar,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            text="<=",
            command=self.back
        )
        self.back_button.pack(side=LEFT)
        self.forward_button = Button(
            self.toolbar,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            text="=>",
            command=self.forward
        )
        self.forward_button.pack(side=LEFT)
        self.up_button = Button(
            self.toolbar,
            relief=FLAT,
            font=("Source Code Pro", "12"),
            text=" ^ ",
            command=self.up_level
        )
        self.up_button.pack(side=LEFT)

    def back(self):
        self.change_dir(self.HISTORY.back())

    def forward(self):
        self.change_dir(self.HISTORY.forward())

    def up_level(self):
        up_one = os.path.sep.join(self.HISTORY.cwd.split(os.path.sep)[:-1])
        self.HISTORY.new_dir(up_one)
        self.change_dir(up_one)

    def render_main_frame(self):
        self.main_frame = Frame(self.master, background="red")
        self.render_tree_sidebar()
        self.tree_sidebar.bind("<<TreeviewOpen>>", self.on_changed_dir)
        self.render_file_grid()
        self.main_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=9)
        self.main_frame.rowconfigure(0, weight=1)

    def render_tree_sidebar(self):
        self.tree_frame = Frame(self.main_frame)
        self.tree_sidebar = TreeSidebar(self.tree_frame, show='tree')
        # self.tree_sidebar.bind('<Double-1>', self.on_changed_dir)
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
        self.file_explorer.main_tree.bind('<Double-1>', self.on_changed_dir)
