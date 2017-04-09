import uuid
from tkinter import *

from gui.file_explorer import FileExplorer


class ChildWindowController():
    def __init__(self, controller):
        self.id = uuid.uuid1()
        self.controller = controller

    def create(self):
        self.window = FileExplorer(self.controller, self.id)

    def destroy(self):
        self.window.destroy()

    def update(self):
        #TODO: Fill this in
        pass


class WindowManager(Frame):
    def __init__(self, master):
        self.master = master
        Frame.__init__(self, self.master)
        self.win_controllers = {} # { uuid_str: ChildWindowController }
        self.pack()
        self.create_child()

    def destroy_child(self, child_id: str):
        if child_id not in self.win_controllers.keys():
            print("FATAL ERROR: Trying to destroy a non-existent child!")
            print("Child ID: {}".format(child_id))
            print("Controllers: {}".format([c for c in self.win_controllers.keys()]))
            exit(1)
        child = self.win_controllers.pop(child_id)
        child.destroy()
        if self.win_controllers == {}:  # No child windows remain, close application
            self.master.destroy()

    def create_child(self):
        child = ChildWindowController(self)
        self.win_controllers[child.id] = child
        child.create()