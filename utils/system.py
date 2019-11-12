"""
The system module: Provides functions specific to Windows platform.

These functions help you deal with handling of system related events.

At a glance, the structure of the module is following:
 - make_dir():          Creates a leaf directory & all intermediate
                        ones. If the target directory already exists, it
                        will skip this & resume with executing the rest
                        code. Works like `mkdir`, except that any
                        intermediate path segment will be created if it
                        does not exist.
 - profiler():          A decorator that uses cProfile to profile a
                        function. This function is essentially developed
                        to test & optimise other functions. The
                        profiling is done at the later stage once the
                        bruteforced code is compliled.
 - active_windows():    Lists all currently active windows. It is
                        recommended to use this function in conjunction
                        with `minimize_window`.
 - minimize_window():   Minimizes active window frame. It is recommended
                        to use when the process starts & needs to be
                        minimized.
 - check_internet():    Checks the internet connectivity of the system.
                        If the internet connection is available, it
                        returns True else False. It is recommended to
                        use to this function where internet connection
                        is required.
 - find_file():         Finds the matching file in the directory. This
                        function uses Fuzzy Logic for determining the
                        best possible match. Function can provide 3 best
                        possible matches but we use just 1 i.e. The best
                        match.
 - get_drives():        Returns the drive letter from all the valid &
                        present partitions. This assures that the user
                        does not use any drive letter which is not
                        present on the system.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my GitHub repo for history & latest stable build >
#
#   2.0.0 - Reworked script.
#           Removed `resolve_days` func. & moved it to generic module.
#           Added `make_dir` & `find_file` from generic module.
#           Added `get_drives` function from paths module.
#   1.1.1 - Added 2 new functions, `profiler` & `resolve_days`.
#           Improved the type hints by using the typing module.
#           Made the code more* PEP-8 compliant.
#   1.0.4 - Added `check_internet` function to check the internet
#           connection.
#   1.0.0 - First code.

from typing import Any, Callable, List, NoReturn, Optional, Text, Union, Tuple

from charlotte.utils.generic import find_string
from charlotte.utils.paths import files


def make_dir(name: Text, init: Optional[bool] = False) -> NoReturn:
    """Creates directory.

    name: Name of the directory to be created.
    init: If made True, it will create `__init__.py` in directory.
          Default: None

    Creates a leaf directory & all intermediate ones. If the target
    directory already exists, it will skip this & resume with executing
    the rest code. Works like mkdir, except that any intermediate path
    segment will be created if it does not exist.

    Note: If the target directory already exists, it will skip this &
    resume with executing the rest code.
    """
    from os import makedirs
    from os.path import exists, join

    if not exists(name):
        makedirs(name)
        if init is True:
            init = open(join(name, files.get('init')), 'a+')
            init.close()


def profiler(function: Callable) -> Any:
    """Profiling & optimizing decorator.

    function: Name of the function that needs the profiling.

    A decorator that uses cProfile to profile a function. This function
    is essentially developed to test & optimise other functions. The
    profiling is done at the later stage once the bruteforced code is
    compliled.

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
        stats.print_stats(10)
        print(string.getvalue())
        return ret_val

    return inner


def active_windows() -> List:
    """Returns list of active windows.

    Lists all currently active windows.

    Note: It is recommended to use this function in conjunction with
    `minimize_window`.
    """
    # You can find the reference code here:
    # https://sjohannes.wordpress.com/2012/03/23/win32-python-getting-
    # all-window-titles/
    import ctypes

    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                         ctypes.POINTER(ctypes.c_int),
                                         ctypes.POINTER(ctypes.c_int))
    titles = []

    def _each_window(hwnd: Any, lParam: Any) -> bool:
        """Function which pulls boolean status of each active window."""
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            # Creating list of windows.
            titles.append(buff.value)
            titles
        return True

    # Listing all the active windows, includes windows which has no name
    # too.
    ctypes.windll.user32.EnumWindows(EnumWindowsProc(_each_window), 0)
    # Returns list of only active windows with title names.
    return list(filter(None, titles))


def minimize_window(window_name: Text,
                    delay: Union[float, int] = 1.0) -> NoReturn:
    """Minimizes active window.

    window_name: Name of the window that needs to be minimize.
                 The name can be fuzzy.
    delay:       Delay with which the window should be minimized.
                 Default: 1.0 sec.

    Note: It is recommended to use when the process starts and needs to
    be minimized.
    """
    # You can find the reference code here:
    # https://stackoverflow.com/questions/25466795/how-to-minimize-a-
    # specific-window-in-python?noredirect=1&lq=1
    from time import sleep
    from win32con import SW_MINIMIZE
    from win32gui import FindWindow, ShowWindow

    sleep(delay) if delay else sleep(1.0)
    # Minimizes window using the `find_string` function (fuzzy match).
    ShowWindow(FindWindow(None, find_string(window_name, active_windows())),
               SW_MINIMIZE)


def check_internet(timeout: Optional[Union[float, int]] = 10.0) -> bool:
    """Checks the internet.

    timeout: Time in seconds before the function sends response if the
             internet is available or not.
             Default: 10.0 secs.

    Checks the internet connectivity of the system. Returns True if the
    internet connection is available, else False.

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


def find_file(file: Text,
              dir_name: Text,
              min_score: Optional[int] = 70) -> Tuple[Text, int]:
    """Finds file in directory.

    file:      Approx. name of the file to search in the directory.
    dir_name:  Directory in which the file needs to be searched in.
    min_score: Minimum score needed to make an approximate guess.
               Default: 70

    Finds the matching file in the directory. This function uses Fuzzy
    Logic for determining the best possible match.

    Note: Function can provide 3 best possible matches but we use just 1
    i.e. The best match.
    """
    from os import listdir
    from fuzzywuzzy.fuzz import partial_ratio
    from fuzzywuzzy.process import extract

    # This will give us list of 3 best matches for our search query.
    guessed = extract(file, listdir(dir_name), limit=3, scorer=partial_ratio)
    for best_guess in guessed:
        # Finding the best match whose Levenshtein score is near to 100.
        current_score = partial_ratio(file, best_guess)
        if current_score > min_score and current_score > 0:
            return best_guess[0], current_score
        else:
            return f'Sorry, I could not find "{file}" in the directory.', 0


def get_drives(drive_letter: Text) -> Text:
    """Returns drive letter.

    drive_letter: Drive letter to be searched for.

    Returns the drive letter from all the valid and present partitions.
    This assures that the user does not use any drive letter which is
    not present on the system.
    """
    from pathlib import Path
    from win32api import GetLogicalDriveStrings

    partitions = GetLogicalDriveStrings().split('\000')[:-1]
    drive = {}
    try:
        for index in range(len(partitions)):
            keys = (Path(partitions[index]).parts[0].split(':\\')[0]).lower()
            values = partitions[index]
            drive[keys] = values
        return drive[drive_letter[0].lower()]
    except KeyError as error:
        missing_drive = str(error).strip('\'')
        print(f'Could not find {missing_drive.title()}:\\ drive.')
