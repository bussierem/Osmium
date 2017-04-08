import uuid
import threading

from tkinter import *
from threading import Thread, Timer
from gui.main_window import Window
from utils.utilities import *


class WindowHistory(list):
    def __init__(self):
        super().__init__()

    def append(self, p_object):
        if p_object in self:
            self.remove(p_object)
        super().append(p_object)


class WindowManager(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, master)
        self.os_type = get_os_type()
        self.pack()
        self.windows = {}
        self.win_order = WindowHistory()
        self.open_new_window()

    def open_new_window(self):
        win_id = uuid.uuid1()
        win_tl = Toplevel(self, width=1024, height=768)
        win_tl.geometry('{}x{}'.format(1024, 768))
        if get_os_type() == 'Windows':
            win_tl.iconbitmap(r'./resources/icons/osmium.ico')
        else:
            win_tl.iconbitmap('@./resources/icons/osmium.xbm')
        win_tl.update()
        win_tl.wm_title("{} - Osmium".format(os.path.split(os.path.expanduser("~"))[1]))
        new_win = Window(win_id, self, win_tl)
        self.windows[win_id] = new_win
        self.win_order.append(win_id)
        new_win.focus_force()

    def close_window(self, win_id):
        window = self.windows.pop(win_id)
        window.master.destroy()
        if self.windows:
            self.win_order.remove(win_id)
            last = self.windows[self.win_order[-1]]
            last.focus_force()
        else:
            self.master.destroy()

    def to_front(self, win_id):
        self.win_order.append(win_id)


class WindowUpdateChecker(Thread):
    def __init__(self):
        self.active_windows = {}
        Thread.__init__(self)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def update_windows(self):
        self.timer = Timer(1, self.update_windows).start()
        for _, window in self.active_windows.items():
            window.on_refresh_dir()

    def add_window(self, id, win):
        if hasattr(self, "timer"):
            self.timer.cancel()
        self.active_windows[id] = win
        self.update_windows()

    def remove_window(self, id):
        if hasattr(self, "timer"):
            self.timer.cancel()
        self.active_windows.pop(id)
        if self.active_windows != {}:
            self.update_windows()