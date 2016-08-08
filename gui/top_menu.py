from tkinter import *
from tkinter import messagebox


class TopMenu(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, master)
        self.menu_bar = Menu(self.master, tearoff=0)
        self.master.config(menu=self.menu_bar)
        self.render_file_menu()
        self.render_edit_menu()
        self.render_tags_menu()
        self.render_help_menu()

    def render_file_menu(self):
        self.file_menu = Menu(self.menu_bar, tearoff=0)

        self.file_menu.add_command(label="New Window", command=self.TODO, accelerator="Ctrl+N")
        self.bind("<Control-n>", self.TODO)
        self.file_menu.add_command(label="New Tab", command=self.TODO, accelerator="Ctrl+T")
        self.bind("<Control-t>", self.TODO)

        self.file_menu.add_separator()

        self.file_menu.add_command(label="Next Tab", command=self.TODO, accelerator="Ctrl+Tab")
        self.bind("<Control-Tab>", self.TODO)
        self.file_menu.add_command(label="Previous Tab", command=self.TODO, accelerator="Ctrl+Shift+Tab")
        self.bind("<Control-Shift-Tab>", self.TODO)
        self.file_menu.add_command(label="Reopen Last Tab", command=self.TODO, accelerator="Ctrl+Shift+T")
        self.bind("<Control-Shift-t>", self.TODO)

        self.file_menu.add_separator()

        self.file_menu.add_command(label="Close Tab", command=self.TODO, accelerator="Ctrl+W")
        self.bind("<Control-w>", self.TODO)
        self.file_menu.add_command(label="Close Window", command=self.close_window, accelerator="Alt+F4")
        self.bind("<Alt-F4>", self.close_window)

        # Add File Menu to Menubar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

    def render_edit_menu(self):
        self.edit_menu = Menu(self.menu_bar, tearoff=0)

        self.edit_menu.add_command(label="Select All", command=self.TODO, accelerator="Ctrl+A")
        self.bind("<Control-a>", self.TODO)
        self.edit_menu.add_command(label="Cut", command=self.TODO, accelerator="Ctrl+X")
        self.bind("<Control-x>", self.TODO)
        self.edit_menu.add_command(label="Copy", command=self.TODO, accelerator="Ctrl+C")
        self.bind("<Control-c>", self.TODO)
        self.edit_menu.add_command(label="Paste", command=self.TODO, accelerator="Ctrl+V")
        self.bind("<Control-v>", self.TODO)
        self.edit_menu.add_command(label="Rename", command=self.TODO, accelerator="F2")
        self.bind("<F2>", self.TODO)

        self.edit_menu.add_separator()

        self.edit_menu.add_command(label="Undo", command=self.TODO, accelerator="Ctrl+Z")
        self.bind("<Control-z>", self.TODO)
        self.edit_menu.add_command(label="Redo", command=self.TODO, accelerator="Ctrl+Shift+Z")
        self.bind("<Control-Shift-z>", self.TODO)
        self.edit_menu.add_command(label="Send to Recycle Bin", command=self.TODO, accelerator="Delete")
        self.bind("<Delete>", self.TODO)
        self.edit_menu.add_command(label="Delete Permanently", command=self.TODO, accelerator="Shift+Delete")
        self.bind("<Shift-Delete>", self.TODO)

        self.edit_menu.add_separator()

        self.edit_menu.add_command(label="Preference", command=self.TODO, accelerator="Ctrl+,")
        self.bind("<Control-,>", self.TODO)

        # Add Edit Menu to Menubar
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

    def render_tags_menu(self):
        self.tags_menu = Menu(self.menu_bar, tearoff=0)

        self.tags_menu.add_command(label="Tag Selection", command=self.TODO, accelerator="Ctrl+D")
        self.bind("<Control-d>", self.TODO)
        self.tags_menu.add_command(label="Untag Selection", command=self.TODO, accelerator="Ctrl+Shift+D")
        self.bind("<Control-Shift-d>", self.TODO)

        self.tags_menu.add_separator()

        # TODO: ADD LIST OF USER-CREATED TAGS HERE, SELECTABLE
        self.tags_menu.add_command(label="TODO: User Tags", accelerator="")

        # Add Tags Menu to Menubar
        self.menu_bar.add_cascade(label="Tags", menu=self.tags_menu)

    def render_help_menu(self):
        self.help_menu = Menu(self.menu_bar, tearoff=0)

        self.help_menu.add_command(label="About", command=self.about_application)

        # Add File Menu to Menubar
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

    def TODO(self):
        print("TODO:  This event still needs to be completed/linked!")

    def about_application(self):
        messagebox.showinfo(
            "About Osmium",
            "This program is a work in progress.\n"
            "The source code is located at: http://github.com/bussierem/Osmium\n"
            "Copyright (c) 2016 Max Bussiere")

    def close_window(self):
        self.master.quit()
