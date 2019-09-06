"""
The generic module: Provides generic, low-level and high-level functions.

These functions help to perform certain tasks with relative ease and without
re-writing them. It also provides various functions that are useful to you
while working with project data.

At a glance, the structure of the module is following:
 - make_dir():          Creates a leaf directory and all intermediate ones.
                        If the target directory already exists, it will skip
                        this and resume with executing the rest code. Works
                        like mkdir, except that any intermediate path segment
                        will be created if it does not exist.
 - timestamp():         Returns current timestamp for logging purposes in
                        desired format. It is recommended to use this while
                        creating logs, files and folders which serve same
                        purpose but need to be distinct from one another.
 - make_log():          Creates log file. The output log file is created with
                        current file name under `./logs/` directory with
                        chosen timestamp. The function disables TensorFlow
                        warnings with `TF_CPP_MIN_LOG_LEVEL` metrics. It is
                        totally optional and you can choose to show it on
                        command line if needed.
 - show():              Prints statements with `?` prefix. This function is
                        simply for the looks of output statement on CMD.
 - quit():              Terminates the code with a confirmation.
 - write_to_csv():      Creates a csv file and writes data into it. Directory
                        hosting the csv file should exist, if not it will
                        raise an Exception for the same. The default delimiter
                        here is a `comma` or `,`.
 - extract_csv():       Extracts specific column from csv file and saves it in
                        another file. After extracting the column it sorts the
                        data. The target file can be any text handling file.
                        It is recommended to use for creating lookup tables.
 - sort_lines():        Sorts the lines in the file and saves it. This
                        function is used to debug any redundancies in NLU data.
 - randomize_lines():   Randomizes the lines in the file. This function is
                        used to make the dataset slightly random.
 - replace_data():      Randomly replaces the given words in the file with
                        required word and saves it. It is recommended to use
                        this to replace the common words OR patterns in your
                        dataset.
 - delete_lines():      Randomly deletes lines from the file and saves it. It
                        is recommended to use this function for shrinking the
                        dataset.
 - find_file():         Finds the matching file in the directory. This
                        function uses Fuzzy Logic for determining the best
                        possible match. Function can provide 3 best possible
                        matches but we use just 1 i.e. `The best match`.
 - str_match():         Finds the matching string in the list. This function
                        is similar to `find_file` function but it needs to be
                        used for searching file from directory while this
                        function can be used for guessing `text` from any
                        valid list like for ex. CSV columns.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info

from charlotte.utils.assists.inquiry import confirm
from charlotte.utils.paths.directories import ai_dir
from charlotte.utils.paths.files import ai_file

# Constant used by `write_to_csv`, `extract_csv`, `sort_lines, `replace_data`,
# `randomize_lines` and `delete_lines` to use default UTF-8 encoding.
_ENCODING = 'utf-8'
# Constant used by `find_file` and `str_match` to set default score when no
# match is found.
_NO_MATCH_SCORE = 0


def make_dir(dir_name: str, need_init: bool = None) -> None:
    """Creates directory.

    dir_name:  Name of the directory to be created.
    need_init: If made True, it will create `__init__.py` in the directory.
               Default: None

    Creates a leaf directory and all intermediate ones. If the target
    directory already exists, it will skip this and resume with executing the
    rest code. Works like mkdir, except that any intermediate path segment
    will be created if it does not exist.

    Note: If the target directory already exists, it will skip this and resume
    with executing the rest code.
    """
    from os import makedirs
    from os.path import exists, join

    try:
        if not exists(dir_name):
            makedirs(dir_name)
            if need_init is True:
                # Creates `__init__.py` file.
                init = open(join(dir_name, ai_file['init']), 'a+')
                init.close()
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def timestamp(format: str) -> str:
    """Returns timestamp.

    format: Timestamp format that you need to show the time.

    Returns current timestamp for logging purposes in desired format. It is
    recommended to use this while creating logs, files and folders which serve
    same purpose but need to be distinct from one another.

    Note: Here are some of the useful timestamp formats that you can use:
            * %d.%m.%Y                - 31.05.2019
            * %I:%M:%S %p             - 01:23:45 AM
            * %H:%M:%S                - 01:23:45
            * %d.%m.%Y %I:%M:%S %p    - 31.05.2019 01:23:45 AM
            * %d_%m_%Y_%I_%M_%S_%p    - 31_05_2019_01_23_45_AM
            * %d.%m.%Y %H:%M:%S       - 31.05.2019 01:23:45
            * %d_%m_%Y_%H_%M_%S       - 31_05_2019_01_23_45
    """
    from datetime import datetime

    try:
        # datetime.now() returns current time of execution.
        return str(datetime.now().strftime(format))
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def _plain(text: str) -> str:
    """Escapes ANSI sequence."""
    from re import compile

    try:
        # Most helpful while striping colors from colored text on command line.
        ansi_escape = compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def make_log(file: str, show_warning: bool = None) -> classmethod:
    """Creates log file.

    file:         Name of the current file.
    show_warning: If made True, it will print the TensorFlow deprecated
                  warnings while running.
                  Default: False

    The output log file is created with current file name under `./logs/`
    directory with chosen timestamp. The function disables TensorFlow warnings
    with `TF_CPP_MIN_LOG_LEVEL` metrics. It is totally optional and you can
    choose to show it on command line if needed.

    Note: Using `__file__` is advisable as input to the file argument.
    """
    from logging import DEBUG, FileHandler, Formatter, getLogger, StreamHandler
    from os.path import join
    from pathlib import Path
    from sys import stdout

    try:
        make_dir(ai_dir['logs'])
        log = getLogger(file)
        # Logging level is set to `debug` by default. You can change this if
        # needed.
        log.setLevel(DEBUG)
        log_file = Path(str(file).lower()).stem
        log_time = timestamp('%d_%m_%Y_%I_%M_%S_%p')
        # Log name will be <filename>_<current_timestamp>.log
        # For ex. If logging is used in cipher.py, it will create a log file
        # like cipher_31_05_2019_01_23_45_AM.log under ./logs/ directory.
        log_name = f'{log_file}_{timestamp(log_time)}.log'
        log_formatter = Formatter(f'%(asctime)s.%(msecs)06d    %(levelname)'
                                  '-8s    %(filename)s:%(lineno)-4s '
                                  '   %(message)-8s',
                                  '%Y-%m-%d %H:%M:%S')
        file_handler = FileHandler(join(ai_dir['logs'], log_name))
        file_handler.setFormatter(log_formatter)
        log.addHandler(file_handler)
        stream_handler = StreamHandler(stdout)
        stream_handler.setFormatter(log_formatter)
        log.addHandler(stream_handler)
        # This part of code is not required now as the deprecation warnings
        # have been taken care by Rasa itself.
        if show_warning is None:
            import os
            import tensorflow.python.util.deprecation as deprecation

            # Disables deprecation warnings.
            deprecation._PRINT_DEPRECATION_WARNINGS = False
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        return log
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def show(message: str) -> None:
    """Prints statements with `?` prefix."""
    print(f'? {message}')


def quit() -> None:
    """Terminates the code with a confirmation."""
    from sys import exit

    try:
        option = confirm('Are you sure you want to leave?')
        if option is True:
            exit()
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def write_to_csv(file: str, *args) -> None:
    """Creates and writes csv file.

    file: Path to the csv file.
    args: Objects to be added to the csv file.

    Creates a csv file and writes data into it. Directory hosting the csv file
    should exist, if not it will raise an Exception for the same.

    Note: The default delimiter here is a `comma` or `,`.
    """
    from csv import QUOTE_MINIMAL, writer

    try:
        with open(file, 'a', newline='', encoding=_ENCODING) as csv_file:
            write_to_csv = writer(csv_file,
                                  delimiter=',',
                                  quoting=QUOTE_MINIMAL)
            write_to_csv.writerow([*args])
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def extract_csv(src_file: str, tgt_file: str, column: str) -> None:
    """Extracts column from csv file.

    src_file: File name from which the data needs to be read.
    tgt_file: File name to which the sorted data needs to be written.
    column:   Column name to be extracted.

    Extracts specific column from csv file and saves it in another file. After
    extracting the column it sorts the data. The target file can be any text
    handling file.

    Note: It is recommended to use this for creating lookup tables.
    """
    from csv import DictReader

    try:
        with open(src_file, 'r', encoding=_ENCODING, errors='ignore') as source_file:
            csv_data = DictReader(source_file)
            data_dict = {}
            for index in csv_data:
                for header, value in index.items():
                    try:
                        data_dict[header].append(value)
                    except KeyError:
                        data_dict[header] = [value]
        extract = data_dict[column]
        extract.sort()
        for line in extract:
            write_to_csv(tgt_file, line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def sort_lines(file: str) -> None:
    """Sorts lines in file.

    file: File whose data needs to be sorted.

    Sorts the lines in the file and saves it. This function is used to debug
    any redundancies in the NLU data.
    """
    try:
        with open(file, encoding=_ENCODING) as source_file:
            new_list = list(set(source_file.readlines()))
            new_list.sort()
            source_file.close()
        with open(file, 'w', encoding=_ENCODING) as source_file:
            for line in new_list:
                source_file.write(line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def randomize_lines(file: str) -> None:
    """Randomizes lines.

    file: File whose lines need to be randomized.

    Randomizes the lines in the file. This function is used to make the
    dataset slightly random.
    """
    from random import shuffle

    try:
        with open(file, 'r', encoding=_ENCODING) as source_file:
            new_list = list(set(source_file.readlines()))
            shuffle(new_list)
            source_file.close()
        with open(file, 'w', encoding=_ENCODING) as source_file:
            for line in new_list:
                source_file.write(line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def replace_data(file: str,
                 find_words: list,
                 replace_words: list) -> None:
    """Replaces words or phrases.

    file:          File from which the words needs to be replaced.
    find_words:    List of words to be replaced from the opened file.
    replace_words: List of words to be replaced with in the opened file.

    Randomly replaces the given words in the file with required word and saves
    it.

    Note: It is recommended to use this to replace the common words OR patterns
    in your dataset.
    """
    from random import choice

    try:
        with open(file, 'r', encoding=_ENCODING) as source_file:
            lines = source_file.readlines()
            source_file.close()
        with open(file, 'w', encoding=_ENCODING) as source_file:
            for line in range(len(lines)):
                if any(word in lines[line] for word in find_words):
                    replaced_line = lines[line].replace(
                        choice(find_words), choice(replace_words))
                    source_file.write(replaced_line)
                else:
                    source_file.write(lines[line])
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def delete_lines(file: str, lines_to_retain: int = 1000) -> None:
    """Deletes lines randomly.

    file:            File from which the lines are to be deleted.
    lines_to_retain: Number of lines to keep in the file.
                     Default: 1000

    Randomly deletes lines from the file and saves it.

    Note: It is recommended to use this function for shrinking the dataset.
    """
    from random import choices, shuffle

    try:
        with open(file, 'r', encoding=_ENCODING) as source_file:
            new_list = list(set(source_file.readlines()))
            shuffle(new_list)
            source_file.close()
        with open(file, 'w', encoding=_ENCODING) as source_file:
            if int(lines_to_retain) is None:
                shrunked_list = choices(new_list, k=1000)
            else:
                shrunked_list = choices(new_list, k=int(lines_to_retain))
            for line in shrunked_list:
                source_file.write(line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def find_file(file: str, file_dir: str, min_score: int = 65) -> tuple:
    """Finds file in directory.

    file:      Approx. name of the file you need to search in the directory.
    file_dir:  Directory in which the file exists or needs to be searched in.
    min_score: Minimum score/Threshold score that should match while making as
               approximate guess.
               Default: 65

    Finds the matching file in the directory. This function uses Fuzzy Logic
    for determining the best possible match.

    Note: Function can provide 3 best possible matches but we use just 1
    i.e. `The best match`.
    """
    from os import walk
    from fuzzywuzzy.fuzz import partial_ratio
    from fuzzywuzzy.process import extract

    try:
        for _, _, files in walk(file_dir):
            # This will give us 3 best matches for our search query. Hence,
            # these are our best guesses.
            guessed_files = extract(file, files, limit=3, scorer=partial_ratio)
            no_match_found = f'Sorry, I could not find "{file}" in the directory.'
            # Using the list of guessed words we will consider a single match
            # whose Levenshtein distance score is near to 100.
            for best_guess in guessed_files:
                current_score = partial_ratio(file, best_guess)
                if current_score > min_score and current_score > _NO_MATCH_SCORE:
                    return best_guess[0], current_score
                else:
                    return no_match_found, _NO_MATCH_SCORE
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def str_match(text: str, text_list: list, min_score: int = 65) -> str:
    """Finds string in list.

    text:      Approximate text that you need to find from the list.
    text_list: List in which the text exists or needs to be searched in.
    min_score: Minimum score/Threshold score that should match while making as
               approximate guess.
               Default: 65

    Finds the matching string in the list. This function is similar to
    `find_file` function but it needs to be used for searching file from
    directory while `str_match` can be used for guessing `text` from any valid
    list like for ex. CSV columns.
    """
    from os import walk
    from fuzzywuzzy.fuzz import partial_ratio
    from fuzzywuzzy.process import extract

    try:
        # Similar to `find_file` functions, we will give get 3 best matches
        # for our search query.
        if text is not None:
            guessed = extract(text, text_list, limit=3, scorer=partial_ratio)
            no_match_found = f'Sorry, I could not find a match for "{text}".'
            # Using the list of guessed words we will consider a single match
            # whose Levenshtein distance score is near to 100.
            for best_guess in guessed:
                current_score = partial_ratio(text, best_guess)
                if current_score > min_score and current_score > _NO_MATCH_SCORE:
                    return best_guess[0]
                else:
                    return no_match_found
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')
