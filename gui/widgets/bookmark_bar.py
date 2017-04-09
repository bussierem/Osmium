import os
from tkinter import *
from utils.bookmarks import *
from PIL import Image, ImageTk

class BookmarkBar(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, master)
        self.bookmark_buttons = []
        self.render_bookmarks()
        self.pack(side=TOP, fill=X)

    def render_bookmarks(self):
        manager = BookmarkManager()
        #TODO:  Move resource acquisition to handler
        icon = Image.open('./resources/icons/folder.gif')
        self.folder = ImageTk.PhotoImage(icon)
        for bookmark in manager.bookmarks:
            assert isinstance(bookmark, Bookmark)
            self.bookmark_buttons.append(
                Button(
                    self,
                    relief=FLAT,
                    text=bookmark.name,
                    image=self.folder,
                    compound="left",
                    # TODO:  This is broken, all go to the "last" bookmark's path!
                    command=lambda: self.change_dir(bookmark.full_path)
                ).pack(side=LEFT)
            )

    def change_dir(self, path):
        self.master.set_directory(path)