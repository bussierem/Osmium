from tkinter.ttk import Progressbar
from tkinter import *
from utils.utilities import *
from handlers.compatibility import CompatibilityHandler

class ProgressBarWindow(Toplevel):
    def __init__(self, master, id, maximum):
        self.master = master
        self.id = id
        self.maximum = maximum
        Toplevel.__init__(self, self.master, width=250, height=100)
        self.render()
        self.current = 0
        self.bind('<Control-p>', self.run_sim)

    def run_sim(self, event):
        self.simulate(500)

    def render(self):
        self.window = Frame(self)
        self.bar = Progressbar(
            self.window,
            orient="horizontal",
            length=200,
            mode="determinate",
            value=0,
            maximum=self.maximum
        )
        self.bar.pack(side=TOP)
        self.cancel_button = Button(self.window, text="Cancel", command=self.TODO)
        self.cancel_button.pack(side=TOP)
        self.window.pack()
        self.update()

    def simulate(self, num):
        self.current += num
        self.bar["value"] = self.current
        self.bar.update()
        if self.current < self.maximum:
            self.after(100, lambda: self.simulate(num))
        else:
            self.master.destroy_child(self.id)

    def TODO(self):
        pass
