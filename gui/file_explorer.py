from tkinter import *
from utils.utilities import *

from gui.widgets.toolbar import Toolbar
from gui.widgets.top_menu import TopMenu
from gui.widgets.tree_sidebar import TreeSidebar
from gui.widgets.file_view import FileView

#TODO: Move these to a different location
# Dimensions
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 768
# Colors
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


class FileExplorer(Toplevel):
    def __init__(self, master, id):
        self.master = master
        self.id = id
        Toplevel.__init__(self, self.master, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
        self.configure_window()
        self.history = History()
        self.widgets = {}
        self.render_gui()

    def close_window(self):
        # Kill processes for this window
        if hasattr(self.toolbar, "search_thread") and self.toolbar.search_thread is not None:
            self.toolbar.search_thread.stop()
            self.toolbar.search_daemon.join()
            self.toolbar.destroy()
        self.master.destroy_child(self.id)

    def set_window_title(self, cwd):
        self.wm_title("{} - Osmium".format(cwd.split(os.path.sep)[-1]))

    def configure_window(self):
        # Window basics
        self.geometry('{}x{}'.format(DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        # Window Look 'n' Feel
        # TODO: Move these types of checks to a "compatibility handler"
        if get_os_type() == 'Windows':
            self.iconbitmap(r'./resources/icons/osmium.ico')
        else:
            self.iconbitmap('@./resources/icons/osmium.xbm')
        # Window Bindings
        self.bind("<FocusIn>", lambda _: self.lift)
        self.bind("<Control-n>", lambda _: self.master.create_child())
        # Apply Config
        self.update()

    def render_gui(self):
        self.tabs = None  #TODO: Get this working after refactor
        # Full Window
        self.window = Frame(self, background=BACKGROUND)
        # Menu
        self.top_menu = TopMenu(self, self.window)
        # Toolbar
        self.toolbar = Toolbar(self, self.window)
        # File View
        self.main_frame = Frame(self)
        self.tree_sidebar = TreeSidebar(self.main_frame, self)
        self.file_view = FileView(self.main_frame, self)
        self.main_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=9)
        self.main_frame.rowconfigure(0, weight=1)
        # Apply changes
        self.update()
        self.window.pack()
        self.set_directory(self.history.get_full_cwd())
        self.window.focus_force()

    def set_directory(self, cwd):
        self.set_window_title(cwd)
        "{}{}".format(cwd, os.path.sep)  # Needed for top-level paths like 'C:'
        self.file_view.load_dir(cwd)
        self.toolbar.set_dir(cwd)

    # TODO: RENAME "directory_changed"
    def on_changed_dir(self, cwd):
        if hasattr(self.toolbar, "search_thread") \
               and self.toolbar.search_thread is not None:
            self.toolbar.search_thread.stop()
        if os.path.isdir(cwd):
            self.history.new_dir(cwd)
            self.set_directory(cwd)
        elif os.path.isfile(cwd):
            open_file(cwd)

    # TODO: RENAME "refresh"
    def on_refresh_dir(self, item=None):
        self.set_directory(self.history.get_full_cwd())
        self.on_refresh_sidebar()

    # TODO: RENAME "refresh_sidebar"
    def on_refresh_sidebar(self):
        self.tree_sidebar.refresh()
