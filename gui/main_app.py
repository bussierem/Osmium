import os
from tkinter import *

from PIL import Image

# TODO:  ADD LINK TO https://icons8.com/ IN THE "ABOUT" PAGE!
#   Distributed through Creative Commons Attribution-NoDerivs 3.0 Unported License
#   https://creativecommons.org/licenses/by-nd/3.0/

# Colors
LIGHT_TEAL = "#00e6e6"
DARK_TEAL = "#009999"
BACKGROUND = "#6F807F"


def resize_img(path):
    img = Image.open(path)
    pal = img.getpalette()
    width, height = img.size
    actual_transp = img.info['actual_transparency']
    result = Image.new('LA', img.size)
    im = img.load()
    res = result.load()
    for x in range(width):
        for y in range(height):
            t = actual_transp[im[x, y]]
            color = pal[im[x, y]]
            res[x, y] = (color, t)
    result.resize((32, 32), Image.ANTIALIAS)
    return result


class MainApp(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master, background=BACKGROUND)
        self.frame = Frame(self, background=BACKGROUND)
        self.current_dir = StringVar()
        self.current_search = StringVar()
        self.createWidgets()
        self.frame.pack(side=TOP, expand=1, fill=BOTH)
        self.pack()

    def createWidgets(self):
        # self.nav_frame = Frame(self, padx=5, background="white")
        self.buttons()
        self.master.update()
        self.nav_bar = Entry(
            self.frame, textvariable=self.current_dir, font=("Source Code Pro", "12"), relief=FLAT)
        self.current_dir.set(os.getcwd())
        self.nav_bar.grid(row=0, column=2)
        self.search_bar = Entry(self.frame, textvariable=self.current_search, foreground="grey")
        self.current_search.set("Search")
        self.search_bar.grid(row=0, column=3)
        # self.nav_frame.pack(side=TOP, fill=X, pady=5)
        self.bottom_frame = Frame(self.frame, padx=5, bg=BACKGROUND)
        self.bottom_frame.grid(row=1, column=0, columnspan=4)

    def buttons(self):
        # Back Button
        # Image
        back_button_black = PhotoImage(file="icons/black_icons/Left-52.png")
        self.back_button = Button(self.frame, compound=TOP, image=back_button_black, relief=FLAT, bg=BACKGROUND)
        self.back_button.grid(row=0, column=0)
        self.back_button.image = back_button_black
        forward_button_black = PhotoImage(file="icons/black_icons/Right-52.png")
        self.forward_button = Button(self.frame, compound=TOP, image=forward_button_black, relief=FLAT, bg=BACKGROUND)
        self.forward_button.grid(row=0, column=1)
        self.forward_button.image = forward_button_black
