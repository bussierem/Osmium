import json
import os
from tkinter import messagebox

from utils.settings import *

"""
BOOKMARKS JSON FORMAT

[
    "<DISPLAY_NAME>" : {
        "index" : int,
        "name" : str,
        "full_path" : str,
        "type" : ["folder"/"file"]
    },
    ...
]
"""

# This should only be necessary in a complete meltdown, or on first boot
DEFAULT_BOOKMARKS = [
    {
        "full_path": os.path.join(os.path.expanduser("~"), "Desktop"),
        "type": "folder",
        "name": "Desktop",
        "index": 0
    },
    {
        "full_path": os.path.join(os.path.expanduser("~"), "Downloads"),
        "type": "folder",
        "name": "Downloads",
        "index": 1
    },
    {
        "full_path": os.path.join(os.path.expanduser("~"), "Documents"),
        "type": "folder",
        "name": "Documents",
        "index": 2
    }
]


class BookmarkEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.to_json()
        except AttributeError:
            return json.JSONEncoder.default(self, obj)


class Bookmark():
    def __init__(self, json: dict):
        self.index = json['index']
        self.name = json['name']
        self.full_path = json['full_path']
        self.type = json['type']

    def to_json(self):
        return self.__dict__


class BookmarkManager():
    def __init__(self):
        settings_path = get_settings_path()
        self.bm_path = os.path.join(settings_path, "bookmarks")
        self.bm_backup_path = self.bm_path + ".bak"
        self.read_bookmarks()

    def read_bookmarks(self):
        try:
            with open(self.bm_path, "r") as bm_file:
                bookmarks = json.loads(bm_file.read())
        except json.JSONDecodeError:  # The config is wrong!
            with open(self.bm_backup_path, "r") as bm_file:
                bookmarks = json.loads(bm_file.read())
        except FileNotFoundError:  # config doesn't exist yet
            bookmarks = DEFAULT_BOOKMARKS
        self.bookmarks = [Bookmark(b) for b in bookmarks]
        self.save_bookmarks()
        self.backup_bookmarks()

    def get_bookmark_by_path(self, path):
        found = [b.name for b in self.bookmarks if b.full_path == path]
        if len(found) > 0:
            return found[0]
        else:
            return None

    def save_bookmarks(self):
        with open(self.bm_path, "w") as bm_file:
            bm_file.write(json.dumps(self.bookmarks, indent=2, cls=BookmarkEncoder))

    def backup_bookmarks(self):
        with open(self.bm_backup_path, "w") as bm_file:
            bm_file.write(json.dumps(self.bookmarks, indent=2, cls=BookmarkEncoder))

    def add_bookmark(self, path, name):
        if name in [b.name for b in self.bookmarks]:
            messagebox.showerror(
                "Bookmark already exists",
                "A bookmark named {} already exists".format(name)
            )
            return
        if path in [b.full_path for b in self.bookmarks]:
            name = [b.name for b in self.bookmarks if b.full_path == path][0]
            messagebox.showerror(
                "Bookmark path already exists",
                "A bookmark named \"{}\" already exists for:\n  {}".format(name, path)
            )
            return
        data = {
            'index': len(self.bookmarks),
            'name': name,
            'full_path': path,
            'type': 'folder' if os.path.isdir(path) else 'file'
        }
        self.bookmarks.append(Bookmark(data))
        self.save_bookmarks()

    def remove_bookmark_by_name(self, name):
        self.bookmarks = [b for b in self.bookmarks if b.name != name]
        self.save_bookmarks()

    def remove_bookmark_by_path(self, path):
        self.bookmarks = [b for b in self.bookmarks if b.full_path != path]
        self.save_bookmarks()
