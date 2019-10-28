"""
The system module: Provides functions which deals with Windows platform.

These functions help you deal with handling of system related events.

At a glance, the structure of the module is following:
 - profiler():          A decorator that uses cProfile to profile a
                        function. This function is essentially developed
                        to test and optimise other functions.
 - list_windows():      Lists all currently active windows. It is
                        recommended to use this function in conjunction
                        with `minimize_window`.
 - minimize_window():   Minimizes the window frame. It is recommended to
                        use when the process starts and needs to be
                        minimized.
 - check_internet():    Checks the internet connectivity of the system.
                        If the internet connection is available, it
                        returns True else False. It is recommended to
                        use to this function where internet connection
                        is required.
 - resolve_days():      Returns day value (Sunday, Monday, ... , etc.)

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.1.1 - Added 2 new functions, `profiler` and `resolve_days`.
#           Improved the type hints by using the typing module.
#           Made the code more* PEP-8 compliant.
#   1.0.4 - Added `check_internet` function to check the internet
#           connection.
#   1.0.0 - First code.

from typing import Any, Callable, List, NoReturn, Optional, Text, Union

from charlotte.utils.assists.generic import str_match


def profiler(function: Callable) -> Any:
    """A decorator that uses cProfile to profile a function.

    function: Name of the function that needs the profiling.

    Note: Please use this function in case your script or method needs
    any optimization for improving its performance.
    """
    from cProfile import Profile
    from io import StringIO
    from pstats import Stats

    def inner(*args, **kwargs) -> Any:
        """Inner decorator function."""
        profile = Profile()
        profile.enable()
        ret_val = function(*args, **kwargs)
        profile.disable()
        string = StringIO()
        sortby = 'cumulative'
        stats = Stats(profile, stream=string).sort_stats(sortby)
        stats.print_stats()
        print(string.getvalue())
        return ret_val

    return inner


def list_windows() -> List:
    """Returns list of active windows.

    Lists all currently active windows.

    Note: It is recommended to use this function in conjunction with
    `minimize_window`.
    """
    # You can find the reference code here:
    # https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-all-window-titles/
    import ctypes

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                         ctypes.POINTER(ctypes.c_int),
                                         ctypes.POINTER(ctypes.c_int))
    titles = []

    def _each_window(hwnd: Any, lParam: Any) -> bool:
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


def minimize_window(window_name: Text,
                    delay: Union[float, int] = 1.0) -> NoReturn:
    """Minimizes window.

    window_name: Name of the window that needs to be minimize.
                 The name can be fuzzy.
    delay:       Delay with which the window should be minimized.
                 Default: 1 sec.

    Minimizes the window frame.

    Note: It is recommended to use when the process starts and needs to
    be minimized.
    """
    # You can find the reference code here:
    # https://stackoverflow.com/questions/25466795/how-to-minimize-a-specific-window-in-python?noredirect=1&lq=1
    from time import sleep
    from win32con import SW_MINIMIZE
    from win32gui import FindWindow, ShowWindow

    # Delaying the window minimizing by 1 sec by default.
    sleep(delay) if delay else sleep(1.0)
    # Minimizes window using the `str_match` function (fuzzy match).
    ShowWindow(FindWindow(None, str_match(window_name, list_windows())),
               SW_MINIMIZE)


def check_internet(timeout: Optional[Union[float, int]] = 10) -> bool:
    """Checks internet.

    timeout: Time in seconds before the function sends response if the
             internet is available or not.
             Default: 10 sec.

    Checks the internet connectivity of the system. If the internet
    connection is available, it returns True else False.

    Note: It is recommended to use to this function where internet
    connection is required.
    """
    # You can find the reference code here:
    # https://gist.github.com/yasinkuyu/aa505c1f4bbb4016281d7167b8fa2fc2
    from requests import ConnectionError, get

    url = 'https://www.google.com/'
    try:
        _ = get(url, timeout=timeout)
        return True
    except ConnectionError:
        return False


def resolve_days(days: Optional[int] = None) -> Text:
    """Returns day.

    days: Number of days in future that needs to be converted into
          actual days.
          Default: None
    """
    from datetime import date, datetime
    from itertools import cycle, islice

    week = ['monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
            'saturday',
            'sunday']
    today = datetime.now()
    if days == 0 or days is None:
        return 'today'
    elif days == 1:
        return 'tomorrow'
    elif days > 1 and days < 7:
        idx = date.weekday(today) + days
        # You can find the reference code here:
        # https://stackoverflow.com/a/27594943
        return list(islice(cycle(week), idx, idx+1))[0]
    else:
        return days
