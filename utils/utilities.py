import os
import sys

SIDEBAR_ROW_HEIGHT = 25


def get_os_type():
    if sys.platform.startswith('darwin'):
        os_type = "Mac"
    elif os.name == "nt":
        os_type = "Windows"
    else:
        os_type = "Unix"
    return os_type
