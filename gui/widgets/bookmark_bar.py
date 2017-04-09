import os
from tkinter import *
from utils.bookmarks import *
from PIL import Image, ImageTk
from collections import OrderedDict

class BookmarkBar(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, master)
        self.manager = BookmarkManager()
        self.bookmark_buttons = {}
        self.render_bookmarks()
        self.bind_events()
        self.pack(side=TOP, fill=X)

    def render_bookmark(self, bookmark):
        onclick = self.get_onclick_command(bookmark.full_path)
        button = Button(
            self,
            relief=FLAT,
            text=bookmark.name,
            image=self.folder,
            compound="left",
            command=onclick
        )
        button.pack(side=LEFT)
        button.bind('<Button-3>', self.render_right_click_menu)
        self.bookmark_buttons[bookmark.name] = button

    def render_bookmarks(self):
        #TODO:  Move resource acquisition to handler
        icon = Image.open('./resources/icons/folder.gif')
        self.folder = ImageTk.PhotoImage(icon)
        self.manager.read_bookmarks()
        for bookmark in self.manager.bookmarks:
            assert isinstance(bookmark, Bookmark)
            self.render_bookmark(bookmark)

    def refresh(self):
        self.manager.read_bookmarks()
        for name in [b.name for b in self.manager.bookmarks]:
            if name not in self.bookmark_buttons.keys():
                bookmark = self.manager.get_bookmark_by_attr("name", name)
                self.render_bookmark(bookmark)

    def get_onclick_command(self, path):
        def command():
            return self.change_dir(path)
        return command

    def bind_events(self):
        self.bind('<Button-3>', self.render_right_click_menu)

    def render_right_click_menu(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        if not isinstance(widget, Button):
            return
        name = widget['text'] # This will be used for the various function calls
        self.master.destroy_right_menus()
        self.right_menu = Menu(self.master, tearoff=0)
        menu = OrderedDict([
            ("Open in new tab", self.TODO),
            ("Open in new window", self.TODO),
            ("1", "SEP"),
            ("Edit", self.TODO),
            ("Delete", lambda: self.delete_bookmark_by_name(name)),
            ("2", "SEP"),
            ("Bookmark Manager", self.TODO)
        ])
        for lbl, cmd in menu.items():
            if cmd == "SEP":
                self.right_menu.add_separator()
            elif cmd == self.TODO:
                self.right_menu.add_command(label=lbl, command=cmd, state=DISABLED)
            else:
                self.right_menu.add_command(label=lbl, command=cmd)
        self.right_menu.post(event.x_root, event.y_root)

    def change_dir(self, path):
        if not os.path.exists(path):
            delete = messagebox.askyesno(
                "Bookmark Invalid",
                "This bookmarks location\n"
                "{}\nno longer exists.\n"
                "Would you like to remove this bookmark?".format(path)
            )
            if delete:
                self.delete_bookmark_by_path(path, auto_confirm=True)
            return
        self.master.set_directory(path)

    def delete_bookmark_by_name(self, name, auto_confirm=False):
        delete = True
        if not auto_confirm:
            delete = messagebox.askyesno(
                "Deleting {}".format(name),
                "Are you sure?"
            )
        if delete:
            self.manager.remove_bookmark_by_name(name)
            button = self.bookmark_buttons[name]
            button.destroy()
            self.update()
        self.master.destroy_right_menus()

    def delete_bookmark_by_path(self, path, auto_confirm=False):
        name = self.manager.get_bookmark_by_path(path)
        self.delete_bookmark_by_name(name, auto_confirm)

    def TODO(self, event=None):
        print("TODO:  This event still needs to be completed/linked!")