"""
This module hosts functions which requires intervening with the system.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sys import exc_info

from charlotte.utils.assists.generic import string_match


def list_windows() -> list:
    """
    Definition
    ----------
        Lists all the currently open windows.

    Returns
    -------
        list(filter(None, titles)) : list, default
            List of all currently open windows.

    Notes
    -----
        This function should be use in conjunction with `window_minimizer`.
    """
    # https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/
    import ctypes

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                         ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    titles = []
    def each_window(hwnd, lParam):

        if ctypes.windll.user32.IsWindowVisible(hwnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            titles.append(buff.value)
            titles
        return True

    ctypes.windll.user32.EnumWindows(EnumWindowsProc(each_window), 0)

    return list(filter(None, titles))


def window_minimizer(window_name: str, delay: float = 1.0) -> None:
    """
    Definition
    ----------
        Minimizes the required window.

    Parameters
    ----------
        window_name : string, mandatory
            Name of the window that needs to be minimize. The name can be
            fuzzy.

        delay : float, optional
            Delay with which the window should be minimized.
            Global default: 1 sec.
    """
    # https://stackoverflow.com/questions/25466795/how-to-minimize-a-specific-window-in-python?noredirect=1&lq=1
    from time import sleep
    from win32con import SW_MINIMIZE
    from win32gui import FindWindow, ShowWindow

    if delay is None:
        sleep(1.0)
    else:
        sleep(delay)
    ShowWindow(FindWindow(None, string_match(window_name, list_windows())),
               SW_MINIMIZE)
