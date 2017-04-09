from tkinter import *
from tkinter import messagebox

from utils.utilities import *


class RenamePopup(Entry):
    def __init__(self, parent, text, app, **kw):
        super().__init__(parent, **kw)
        self.app = app
        self.root_path, target = os.path.split(text)
        self.cur_name, self.old_ext = os.path.splitext(target)
        self.insert(0, target)
        self['background'] = 'white'
        self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = False
        self.focus_force()
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())
        self.bind("<Return>", self.rename_selection)
        self.selection_range(0, len(self.cur_name))
        self.icursor(len(self.cur_name))

    def select_all(self, e):
        self.selection_range(0, 'end')
        return 'break'

    def rename_selection(self, event=None):
        new_name, ext = os.path.splitext(self.get())
        ext = ext or self.old_ext
        if is_valid_filename(new_name):
            old_path = os.path.join(self.root_path, self.cur_name + self.old_ext)
            full_path = os.path.join(self.root_path, new_name + ext)
            os.rename(old_path, full_path)
            self.app.refresh()
            self.destroy()
        else:
            invalid_chars = CompatibilityHandler.get_invalid_chars()
            messagebox.showerror(
                'Invalid Filename',
                'A file name cannot contain any of the following characters:\n'
                '{}'.format(invalid_chars)
            )
            self.selection_range(0, len(new_name))
            self.icursor(len(new_name))
