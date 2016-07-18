import shutil
from enum import Enum
from multiprocessing import Pool
from tkinter import messagebox

from send2trash import *

from utils.utilities import *

# This would just be Paste, Move, Recycle, and Delete
RUNNING_OPERATIONS = []
CURRENT_COPY_OP = None


class OpType(Enum):
    cut = "cut"
    copy = "copy"
    paste = "paste"
    recycle = "recycle"
    delete = "delete"
    rename = "rename"
    move = "move"


class FileOperation():
    def __init__(self, func, source, destination=None, args=None, callback=None):
        self.src = source
        self.dst = destination
        self.callback = callback
        self.args = [] if args is None else args
        self.pool = Pool(processes=1)
        self.start_time = time.time()
        self.start(func)

    def start(self, func):
        try:
            self.op_result = self.pool.apply_async(func, self.args, callback=self.callback)
        except Exception as e:
            print("Error with operation:  {}".format(e))

    def get_run_time(self):
        return time.time() - self.start_time()


class CutOperation(FileOperation):
    def __init__(self, source, file=False):
        self.type = OpType.cut
        super().__init__(write_clipboard, source, args=[source, file])


class CopyOperation(FileOperation):
    def __init__(self, source, file=False):
        self.type = OpType.copy
        super().__init__(write_clipboard, source, args=[source, file])


class PasteOperation(FileOperation):
    def __init__(self, func, source, dest, callback):
        self.type = OpType.paste
        super().__init__(func, source, dest, [source, dest], callback)


# This is for both "Cut-Paste" AND "Rename"
class MoveOperation(FileOperation):
    def __init__(self, source, dest):
        self.type = OpType.move
        super().__init__(shutil.move, source, destination=dest, args=[source, dest])


class RecycleOperation(FileOperation):
    def __init__(self, source, callback=None):
        self.type = OpType.recycle
        super().__init__(send2trash, source, args=[source], callback=callback)


class DeleteOperation(FileOperation):
    def __init__(self, source, callback=None):
        self.type = OpType.delete
        func = shutil.rmtree if os.path.isdir(source) else os.remove
        super().__init__(func, source, args=[source], callback=callback)


# Cut
def cut_file(target):
    global CURRENT_COPY_OP
    op = CutOperation(target)
    CURRENT_COPY_OP = op


# Copy
def copy_file(target):
    global CURRENT_COPY_OP
    op = CopyOperation(target)
    CURRENT_COPY_OP = op


# Paste
def paste_file(target, cb_func=None):
    global CURRENT_COPY_OP, RUNNING_OPERATIONS
    if CURRENT_COPY_OP is None:
        return
    source = CURRENT_COPY_OP.src
    src = source.split(os.path.sep)[-1]
    dst = os.path.join(target, src)
    if os.path.exists(dst):
        replace = messagebox.askyesnocancel(
            "Destination already exists",
            "The {} you are trying to paste already exists in the target"
            " destination.\n Would you like to replace the file that already exists?".format(
                "file" if os.path.isfile(source) else "folder"
            )
        )
        if replace is None:
            return
        elif replace is True:
            func = paste_replace(source, dst)
        else:
            dst, func = paste_rename(source, dst)
    else:
        func = paste_to_existing(source)
    RUNNING_OPERATIONS.append(PasteOperation(func, source, dst, cb_func))


def get_copy_func(source):
    if os.path.isdir(source):
        func = shutil.copytree
    else:
        func = shutil.copy
    return func


def paste_to_existing(source):
    global CURRENT_COPY_OP
    if isinstance(CURRENT_COPY_OP, CutOperation):
        func = shutil.move
    else:
        func = get_copy_func(source)
    return func


def paste_replace(source, dest):
    global CURRENT_COPY_OP, RUNNING_OPERATIONS
    if isinstance(CURRENT_COPY_OP, CutOperation):
        if get_os_type() == "Windows":
            RUNNING_OPERATIONS.append(DeleteOperation(dest))
        func = shutil.move
    else:
        func = get_copy_func(source)
    return func


def paste_rename(source, dest):
    global CURRENT_COPY_OP
    copy_name = rename_copy(source, dest)
    if isinstance(CURRENT_COPY_OP, CutOperation):
        func = shutil.move
    else:
        func = get_copy_func(source)
    return copy_name, func


# Recycle
def recycle_file(target, cb_func):
    global RUNNING_OPERATIONS
    RUNNING_OPERATIONS.append(RecycleOperation(target, cb_func))


# Delete
def delete_file(target, cb_func):
    global RUNNING_OPERATIONS
    confirmed = messagebox.askyesno(
        "Confirm Delete File",
        "This will erase the file permanently, this cannot be undone.\n"
        "Are you absolutely sure?")
    if confirmed:
        RUNNING_OPERATIONS.append(DeleteOperation(target, cb_func))


# Rename
def rename_file(source, new_name):
    global RUNNING_OPERATIONS
    src_path = os.path.sep.join(source.split(os.path.sep)[:-1])
    new_file = os.path.join(src_path, new_name)
    if os.path.exists(new_file):
        replace = messagebox.askyesnocancel(
            "Destination already exists",
            "The {} you are trying to paste already exists in the target"
            " destination.\n Would you like to replace the file that already exists?".format(
                "file" if os.path.isfile(source) else "folder"
            )
        )
        if replace is None:  # Cancel Operation
            return
        elif replace is True:  # Replace existing file
            os = get_os_type()
            if os == "Windows":
                RUNNING_OPERATIONS.append(DeleteOperation(new_file))
        else:  # Auto-Rename File
            new_file = rename_copy(source, new_file)
    RUNNING_OPERATIONS.append(MoveOperation(source, new_file))
