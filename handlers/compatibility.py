import os
import sys
import re
from collections import OrderedDict
if os.name == 'nt':
    import win32api
if os.name == 'nt':
    import win32clipboard as wincb
    wincb_formats = {val: name for name, val in vars(wincb).items() if name.startswith('CF_')}
import pyperclip

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

def write_clipboard_win(data: str, file=False):
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


class CompatibilityHandler():
    @staticmethod
    def get_os_type():
        return get_os_type()

    @staticmethod
    def get_app_icon():
        if get_os_type() == 'Windows':
            return r'./resources/icons/osmium.ico'
        else:
            return '@./resources/icons/osmium.xbm'

    @staticmethod
    def get_folder_icon():
        if get_os_type() == 'Windows':
            return './resources/icons/folder_ico.ico'
        else:
            return '@./resources/icons/folder_ico.xbm'

    @staticmethod
    def get_file_icon():
        if get_os_type() == 'Windows':
            return './resources/icons/file_ico.ico'
        else:
            return '@./resources/icons/file_ico.xbm'

    @staticmethod
    def get_used_drive_letters():
        drive_lbls = OrderedDict()
        os = get_os_type()
        if os == "Windows":
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            for d in drives:
                drive_lbls[d] = d
                try:
                    info = win32api.GetVolumeInformation(d)
                    drive_lbls[d] = info[0] if info[0] != '' else d
                except:
                    continue
        elif os == "Unix":
            drive_lbls = {'/': 'Root', '/home/': 'Home'}
        return drive_lbls

    @staticmethod
    def get_settings_path():
        OS_TYPE = get_os_type()
        if OS_TYPE == 'Windows':
            if os.getenv('USERPROFILE'):
                base_loc = os.getenv('USERPROFILE')
            else:
                base_loc = os.path.expanduser('~')
            base_loc = os.path.join(
                base_loc, 'AppData', 'Local', 'Osmium'
            )
        elif OS_TYPE == 'Mac':
            base_loc = os.path.join(
                os.path.expanduser('~'),
                'Library', 'Preferences', 'Osmium'
            )
        else:
            base_loc = os.path.join(os.path.expanduser('~'), '.osmium')
        return base_loc

    @staticmethod
    def get_invalid_chars():
        OS_TYPE = get_os_type()
        if OS_TYPE == "Windows":
            return r'/  \  <  >  :  "  *  |  ?'
        elif OS_TYPE == 'Mac':
            return r'/  :'
        else:
            return r'/'

    @staticmethod
    def get_invalid_chars_regex():
        OS_TYPE = get_os_type()
        if OS_TYPE == "Windows":
            invalid_chars_regex = re.compile(r'((?![<>:"|?\/\\*]).)+')
            # Extra reserved names to check for in Windows
        elif OS_TYPE == "Mac":
            invalid_chars_regex = re.compile(r'((?![\/\:\x00]).)+')
        else:
            invalid_chars_regex = re.compile(r'((?![\/\x00]).)+')
        return invalid_chars_regex

    @staticmethod
    def get_reserved_names_regex():
        OS_TYPE = get_os_type()
        if OS_TYPE == "Windows":
            return re.compile(r'^(COM[1-9])|(LPT[1-9])|(PRN|AUX|NUL|CON)$')

    @staticmethod
    def get_open_command():
        OS_TYPE = get_os_type()
        if OS_TYPE == "Mac":
            command = "open"
        elif OS_TYPE == "Windows":
            command = "start"
        else:
            command = "xdg-open"
        return command

    @staticmethod
    def read_clipboard():
        if get_os_type() == "Windows":
            return read_clipboard_win()
        else:
            return read_clipboard_unix()

    @staticmethod
    def write_clipboard(data, file):
        if get_os_type() == 'Windows':
            write_clipboard_win(data, file)
        else:
            pyperclip.copy(data)