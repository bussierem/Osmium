from utils.utilities import *


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


def export_settings():
    # TODO: Implement this!
    pass
