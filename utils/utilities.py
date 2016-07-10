import os
import sys

SIDEBAR_ROW_HEIGHT = 25
CUT_ENABLED = None

def get_os_type():
    if sys.platform.startswith('darwin'):
        os_type = "Mac"
    elif os.name == "nt":
        os_type = "Windows"
    else:
        os_type = "Unix"
    return os_type


def read_clipboard(app):
    return app.selection_get(selection="CLIPBOARD")


def write_clipboard(app, data: str):
    app.clipboard_clear()
    app.clipboard_append(str(data))


def fast_copy(src, dest):
    pass


class CTError(Exception):
    def __init__(self, errors):
        self.errors = errors


try:
    O_BINARY = os.O_BINARY
except:
    O_BINARY = 0
READ_FLAGS = os.O_RDONLY | O_BINARY
WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | O_BINARY
BUFFER_SIZE = 128 * 1024


def copyfile(src, dst):
    try:
        fin = os.open(src, READ_FLAGS)
        stat = os.fstat(fin)
        fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
        for x in iter(lambda: os.read(fin, BUFFER_SIZE), ""):
            os.write(fout, x)
    finally:
        try:
            os.close(fin)
        except:
            pass
        try:
            os.close(fout)
        except:
            pass


def copytree(src, dst, symlinks=False, ignore=[]):
    names = os.listdir(src)

    if not os.path.exists(dst):
        os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignore:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                copyfile(srcname, dstname)
                # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        except CTError as err:
            errors.extend(err.errors)
    if errors:
        raise CTError(errors)
