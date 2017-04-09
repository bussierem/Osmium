import ntpath
import os
import re
import sys
import time
from handlers.compatibility import CompatibilityHandler

if os.name == 'nt':
    import win32clipboard as wincb
    wincb_formats = {val: name for name, val in vars(wincb).items() if name.startswith('CF_')}

import pyperclip

SIDEBAR_ROW_HEIGHT = 25
CUT_ENABLED = None


def read_clipboard():
    return CompatibilityHandler.read_clipboard()

def write_clipboard(data: str, file=False):
    CompatibilityHandler.write_clipboard(data, file)

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
    invalid_chars_regex = CompatibilityHandler.get_invalid_chars_regex()
    reserved_names_regex = CompatibilityHandler.get_reserved_names_regex()
    if re.match(reserved_names_regex, filename):
        uses_reserved_name = True
    if re.match(invalid_chars_regex, filename):
        has_invalid_chars = True
    return has_invalid_chars or uses_reserved_name


def open_file(filepath):
    command = CompatibilityHandler.get_open_command()
    os.system("{} {}".format(command, filepath))
