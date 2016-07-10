import os
from tkinter import *

import gui.toolbar as tb
import gui.top_menu as menu
import gui.tree_sidebar as sidebar
from gui.file_explorer import FileExplorer

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

    def get_full_cwd(self):
        return self.cwd

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
        self.CUT = False
        self.render_menu()
        self.render_toolbar()
        self.render_main_frame()
        self.pack()

    def render_menu(self):
        self.menu = menu.TopMenu(self.master)

    def render_toolbar(self):
        self.master.update()
        self.toolbar = tb.Toolbar(self.master, self)

    def render_main_frame(self):
        self.main_frame = Frame(self.master, background="red")
        self.render_tree_sidebar()
        self.render_file_grid()
        self.main_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=9)
        self.main_frame.rowconfigure(0, weight=1)

    def render_tree_sidebar(self):
        self.tree_sidebar = sidebar.TreeSidebar(self.main_frame, self)

    def render_file_grid(self):
        self.file_explorer = FileExplorer(self.main_frame, self)

    def change_dir(self, cwd):
        cwd += '\\'  # Needed for top-level paths like 'C:'
        self.file_explorer.load_dir(cwd)
        self.toolbar.set_dir(cwd)

    def on_changed_dir(self, cwd):
        if os.path.isdir(cwd):
            self.HISTORY.new_dir(cwd)
            self.change_dir(cwd)
        elif os.path.isfile(cwd):
            self.open_file(cwd)

    def open_file(self, filepath):
        if self.OS_TYPE == "Mac":
            command = "open"
        elif self.OS_TYPE == "Windows":
            command = "start"
        else:
            command = "xdg-open"
        os.system("{} {}".format(command, filepath))
