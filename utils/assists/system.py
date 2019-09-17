"""
The system module: Provides functions which deals with Windows platform.

These functions help you deal with handling of system related events.

At a glance, the structure of the module is following:
 - list_windows():      Lists all currently active windows. It is recommended
                        to use this function in conjunction with
                        `minimize_window`.
 - minimize_window():   Minimizes the window frame. It is recommended to use
                        when the process starts and needs to be minimized.
 - check_internet():    Checks the internet connectivity of the system. If the
                        internet connection is available, it returns True else
                        False. It is recommended to use to this function where
                        internet connection is required.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.4 - Added `check_internet` function to check the internet connection.
#   1.0.0 - First code.

from sys import exc_info

from charlotte.utils.assists.generic import str_match

# Constant used by `check_internet` to ping google.
_URL = 'https://www.google.com/'


def list_windows() -> list:
    """Returns list of active windows.

    Lists all currently active windows.

    Note: It is recommended to use this function in conjunction with
    `minimize_window`.
    """
    # You can find the reference code here:
    # https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/
    import ctypes

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                         ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    titles = []

    def _each_window(hwnd, lParam):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            # Creating list of windows.
            titles.append(buff.value)
            titles
        return True
    # Listing all the active windows, includes windows which has no name too.
    ctypes.windll.user32.EnumWindows(EnumWindowsProc(_each_window), 0)
    # Returns list of only active windows with title names.
    return list(filter(None, titles))


def minimize_window(window_name: str, delay: float = 1.0) -> None:
    """Minimizes window.

    window_name: Name of the window that needs to be minimize.
                 The name can be fuzzy.
    delay:       Delay with which the window should be minimized.
                 Default: 1 sec.

    Minimizes the window frame.

    Note: It is recommended to use when the process starts and needs to be
    minimized.
    """
    # You can find the reference code here:
    # https://stackoverflow.com/questions/25466795/how-to-minimize-a-specific-window-in-python?noredirect=1&lq=1
    from time import sleep
    from win32con import SW_MINIMIZE
    from win32gui import FindWindow, ShowWindow

    # Delaying the window minimizing by 1 sec by default.
    if delay is None:
        sleep(1.0)
    else:
        sleep(delay)
    # Minimizes window using the `str_match` function (fuzzy string match).
    ShowWindow(FindWindow(None, str_match(window_name, list_windows())),
               SW_MINIMIZE)


def check_internet(timeout: int = 10) -> bool:
    """Checks internet.

    Checks the internet connectivity of the system. If the internet connection
    is available, it returns True else False.

    Note: It is recommended to use to this function where internet connection
    is required.
    """
    # You can find the reference code here:
    # https://gist.github.com/yasinkuyu/aa505c1f4bbb4016281d7167b8fa2fc2
    from requests import ConnectionError, get

    try:
        _ = get(_URL, timeout=timeout)
        return True
    except ConnectionError:
        return False
