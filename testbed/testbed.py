import os
import subprocess
import sys
import time
from os import path

if os.name == "nt":
    from win32 import win32api
    import win32con

"""
TODO:
    list all files and folders with:
        --name
        --type (file or dir)
        --file ext
        --last modified (12 and 24 hr times)
        --size
            --Should be adjusted to the size (TB, GB, MB, Kb)
    --toggle hidden files
    copy files rapidly
    BASIC OPERATIONS:
        --copy
        --move
        --rename
        cut
            name appearance change
            store current path of file/folder
        paste
            if cut:
                move file from stored src to dst
            if copy:
                shutil.copy(src, dst)
    validate file/folder names
        linux
        windows
"""

"""
os stuff:
    os.chdir(path)
    os.getcwd()
    os.access(path)
    os.listdir(path='.')
    os.mkdir(path, mode=0o777)
    os.makedirs(name, mode=0o777, exist_ok=False)
        if not exist_ok, OSError is raised if dir exists
    os.remove(path)
        if path is dir, OSError is raised
        if file in use, OSError is raised
    os.removedirs(name)
    os.rename(src, dst)
        if dst is directory, OSError is raised
        if dst exists & is file, replaced silently
            ALWAYS CHECK IF EXISTS FIRST
    os.renames(old, new)
        recursive creation of folders to make a valid path happen
    os.rmdir(path)
        if directory is not empty, OSError is raised
        use shutil.rmtree() to recurse
    os.scandir(path='.')
        returns DirEntry object
            https://docs.python.org/3.5/library/os.html#os.DirEntry
    ---
    TRY PERMISSIONS BEFORE OPEN:
    try:
        fp = open("myfile")
    except PermissionError:
        return "some error"
    else:
        with fp:
            return fp.read()
    ---
"""


def is_hidden_file(path):
    if OS_TYPE == "Windows":
        attribute = win32api.GetFileAttributes(path)
        return attribute & (
        win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return path.startswith('.')


def display_files(testfile):
    filename, ext = path.splitext(testfile)
    filename = filename.split(path.sep)[-1] + ext
    ext = ext[1:]
    if path.isfile(testfile):
        type = "file"
    elif path.isdir(testfile):
        type = "folder"
    else:
        type = "unknown"
    size = path.getsize(testfile)
    size_t = ["B", "KB", "MB", "GB", "TB"]
    idx = 0
    while size >= 1024.0:
        size /= 1024.0
        idx += 1
    size_str = "{0:.2f} {1}".format(size, size_t[idx])
    mod_time = time.localtime(path.getmtime(testfile))
    last_modified_12 = time.strftime("%m/%d/%y %I:%M:%S %p", mod_time)
    last_modified_24 = time.strftime("%m/%d/%y %H:%M:%S", mod_time)
    print(
        "Name:  {}\nType:  {}\nExt:   {}\nSize:  {}\nMod12: {}\nMod24: {}".format(
            filename, type, ext, size_str, last_modified_12, last_modified_24
        ))


if __name__ == "__main__":
    if sys.platform.startswith('darwin'):
        OS_TYPE = "Mac"
    elif os.name == "nt":
        OS_TYPE = "Windows"
    else:
        OS_TYPE = "Unix"
    testfile = path.join(os.getcwd(), "explorer.txt")
    # display_files(testfile)
    print(os.name)
    if OS_TYPE == "Mac":
        subprocess.call(["open", testfile])
    elif OS_TYPE == "Windows":
        subprocess.call(["start", testfile])
    else:
        subprocess.call(["xdg-open", testfile])
