import ntpath
import os
import re
import sys
import time
import win32clipboard as wincb

import pyperclip

SIDEBAR_ROW_HEIGHT = 25
CUT_ENABLED = None
wincb_formats = {val: name for name, val in vars(wincb).items() if name.startswith('CF_')}


def get_os_type():
    if sys.platform.startswith('darwin'):
        os_type = "Mac"
    elif os.name == "nt":
        os_type = "Windows"
    else:
        os_type = "Unix"
    return os_type


def read_clipboard_win():
    wincb.OpenClipboard(None)
    data = None
    for k in wincb_formats.keys():
        try:
            data = wincb.GetClipboardData(k)
        except TypeError:
            continue
        if data != None:
            if isinstance(data, tuple):
                print("Format: {}".format(wincb_formats[k]))
                print(data)
                data = data[0]
            else:
                data = data.decode()
            break
    wincb.CloseClipboard()
    return data


def read_clipboard_unix():
    return pyperclip.paste()


def read_clipboard():
    if get_os_type() == "Windows":
        return read_clipboard_win()
    else:
        return read_clipboard_unix()


def write_clipboard(data: str, file=False):
    if not file:
        pyperclip.copy(data)
        return
    wincb.OpenClipboard(None)
    format = [k for k in wincb_formats.keys() if wincb_formats[k] == 'CF_HDROP'][0]
    try:
        wincb.SetClipboardData(format, data)
    except:
        pass
    wincb.CloseClipboard()

def thread_finished(thing):
    print("Finished copy thread!")
    print("thing = {}".format(thing))
    print("End:  {}".format(time.time()))


def rename_copy(src_path, dest_path):
    srcfile, ext = os.path.splitext(src_path.split(os.path.sep)[-1])
    copy_name = srcfile
    copy_count = 1
    dst = ntpath.split(dest_path)[0]
    while os.path.exists(os.path.join(dst, copy_name) + ext):
        copy_name = "{} ({})".format(srcfile, copy_count)
        copy_count += 1
    copy_name += ext
    return os.path.join(dst, copy_name)


def is_valid_filename(filename):
    has_invalid_chars = False
    uses_reserved_name = False
    OS_TYPE = get_os_type()
    if OS_TYPE == "Windows":
        # Lots of things banned in Windows...
        invalid_chars_regex = re.compile(r'((?![<>:"|?\/\\*]).)+')
        # Extra reserved names to check for
        reserved_names_regex = re.compile(
            r'^(COM[1-9])|(LPT[1-9])|(PRN|AUX|NUL|CON)$'
        )
        if re.match(reserved_names_regex, filename):
            uses_reserved_name = True
    elif OS_TYPE == "Mac":
        # Not many invalid characters in Mac...
        invalid_chars_regex = re.compile(r'((?![\/\:\x00]).)+')
    else:
        # Even less in Linux!
        invalid_chars_regex = re.compile(r'((?![\/\x00]).)+')
    if re.match(invalid_chars_regex, filename):
        has_invalid_chars = True
    return has_invalid_chars or uses_reserved_name


def get_invalid_chars():
    OS_TYPE = get_os_type()
    if OS_TYPE == "Windows":
        return r'/  \  <  >  :  "  *  |  ?'
    elif OS_TYPE == 'Mac':
        return r'/  :'
    else:
        return r'/'


def open_file(filepath):
    OS_TYPE = get_os_type()
    if OS_TYPE == "Mac":
        command = "open"
    elif OS_TYPE == "Windows":
        command = "start"
    else:
        command = "xdg-open"
    os.system("{} {}".format(command, filepath))
