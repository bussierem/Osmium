from tkinter import *

import gui.widgets.toolbar as tb
import gui.widgets.top_menu as menu
import gui.widgets.tree_sidebar as sidebar
from gui.widgets.file_view import FileView
from utils.utilities import *

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


class Window(Frame):
    def __init__(self, win_id, manager, master=None):
        self.id = win_id
        self.master = master
        self.manager = manager
        Frame.__init__(self, master, background=BACKGROUND)
        self.history = History()
        self.render_menu()
        self.render_toolbar()
        self.render_main_frame()
        self.pack()
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
        self.master.bind("<FocusIn>", lambda _: self.bring_to_front())
        self.bind("<Control-n>", lambda _: self.manager.open_new_window())

    def close_window(self):
        self.manager.close_window(self.id)

    def bring_to_front(self):
        self.manager.to_front(self.id)
        self.master.lift()

    def destroy(self):
        if hasattr(self.toolbar, "search_thread") and self.toolbar.search_thread is not None:
            self.toolbar.search_thread.stop()
            self.toolbar.search_daemon.join()
            self.toolbar.destroy()
        super().destroy()

    def render_menu(self):
        self.menu = menu.TopMenu(self.master, self)

    def render_toolbar(self):
        self.master.update()
        self.toolbar = tb.Toolbar(self.master, self)

    def render_main_frame(self):
        self.main_frame = Frame(self.master)
        self.render_tree_sidebar()
        self.render_file_grid()
        self.main_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=9)
        self.main_frame.rowconfigure(0, weight=1)

    def render_tree_sidebar(self):
        self.tree_sidebar = sidebar.TreeSidebar(self.main_frame, self)

    def render_file_grid(self):
        self.file_explorer = FileView(self.main_frame, self)

    # Purpose:  Edit which directory is displayed in the window
    def set_directory(self, cwd):
        title = "{} - Osmium".format(cwd.split(os.path.sep)[-1])
        cwd += os.path.sep  # Needed for top-level paths like 'C:'
        self.file_explorer.load_dir(cwd)
        self.toolbar.set_dir(cwd)
        self.master.wm_title(title)

    # Purpose:  Called when an object in the FileView is double-clicked
    def on_changed_dir(self, cwd):
        if hasattr(self.toolbar, "search_thread") and self.toolbar.search_thread is not None:
            self.toolbar.search_thread.stop()
        if os.path.isdir(cwd):
            self.history.new_dir(cwd)
            self.set_directory(cwd)
        elif os.path.isfile(cwd):
            open_file(cwd)

    # Purpose:  "Refreshes" the current directory view for the window
    def on_refresh_dir(self, item=None):
        self.set_directory(self.history.get_full_cwd())

    # Purpose:  "Refreshes" the Sidebar
    def on_refresh_sidebar(self):
        self.tree_sidebar.refresh()
