"""
The generic module: Provides generic, low/high-level functions.

These functions help to perform certain tasks with relative ease and
without re-writing them. It also provides various functions that are
useful to you while working with project data.

At a glance, the structure of the module is following:
 - timestamp():         Returns current timestamp for logging purposes
                        in desired format. It is recommended to use this
                        while creating logs, files and folders which
                        serve same purpose but need to be distinct from
                        one another.
 - show():              Prints statements with `?` prefix. This function
                        is simply for the looks of output statement on
                        CMD.
 - quit():              Terminates the code with a confirmation.
 - find_string():       Finds the matching string in the list. This
                        function is similar to `find_file` function but
                        it needs to be used for searching file from
                        directory while this function can be used for
                        guessing text from any valid list like for
                        ex. CSV columns.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my GitHub repo for history and latest stable build >
#
#   2.0.0 - Reworked script.
#           Removed `make_log` function.
#           Removed `make_dir` & `find_file` and moved them to generic
#           module.
#           Removed `sort_lines`, `randomize_lines`, `replace_data`,
#           `delete_lines`, `write_to_csv` & `extract_csv` and moved
#           them to dataset module.
#   1.1.1 - Improved the type hints by using the typing module.
#           Added new `say` function.
#           Made the code more* PEP-8 compliant.
#   1.0.2 - Reduced unnecessary use of "`" in comments for simplicity.
#   1.0.0 - First code.

from typing import List, NoReturn, Optional, Text


def timestamp(format: Text) -> Text:
    """Returns timestamp.

    format: Timestamp format in which you need to show the time.

    Returns current timestamp for logging purposes in desired format.
    It is recommended to use this while creating logs, files and folders
    which serve same purpose but need to be distinct from one another.

    Note: Here are some of the useful timestamp formats that you can
          use:
            * %d.%m.%Y                - 31.05.2019
            * %I:%M:%S %p             - 01:23:45 AM
            * %H:%M:%S                - 01:23:45
            * %d.%m.%Y %I:%M:%S %p    - 31.05.2019 01:23:45 AM
            * %d_%m_%Y_%I_%M_%S_%p    - 31_05_2019_01_23_45_AM
            * %d.%m.%Y %H:%M:%S       - 31.05.2019 01:23:45
            * %d_%m_%Y_%H_%M_%S       - 31_05_2019_01_23_45
    """
    from datetime import datetime

    # datetime.now() returns current time of execution.
    return str(datetime.now().strftime(format))


def show(message: Text) -> NoReturn:
    """Prints statements with `?` prefix."""
    print(f'? {message}')


def quit() -> NoReturn:
    """Terminates the code with a confirmation."""
    from sys import exit
    from charlotte.utils.inquiry import confirm

    option = confirm('Are you sure you want to leave?')
    if option is True:
        exit()


def find_string(string: Text,
                string_list: List,
                min_score: Optional[int] = 70) -> Text:
    """Finds string in list.

    string:      Approximate text that you need to find from the list.
    string_list: List in which the text needs to be searched in.
    min_score:   Minimum score needed to make an approximate guess.
                 Default: 70

    Finds the matching string in the list. This function is similar to
    `find_file` function but it needs to be used for searching file from
    directory while `find_string` can be used for guessing text from any
    valid list like for ex. CSV columns.
    """
    from fuzzywuzzy.fuzz import partial_ratio
    from fuzzywuzzy.process import extract

    # This will give us list of 3 best matches for our search query.
    guessed = extract(string, string_list, limit=3, scorer=partial_ratio)
    for best_guess in guessed:
        # Finding the best match whose Levenshtein score is near to 100.
        current_score = partial_ratio(string, best_guess)
        if current_score > min_score and current_score > 0:
            return best_guess[0]
        else:
            return f'Sorry, I could not find "{string}" in given list.'
