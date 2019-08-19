"""
This module hosts common functions that serve help throughout the package.

    Functions list:
        - make_dir          : Makes a directory
        - timestamp         : Creates timestamp for log files
        - plain             : Escapes the ANSI sequence
        - make_log          : Creates log file
        - display           : Prints statements with `?` prefix
        - quit              : Exits the program
        - csv_writer        : Creates CSV files and adds data to it
        - csv_extractor     : Extracts columns from csv file
        - line_sorter       : Sorts the lines alphabetically in the file
        - line_randomizer   : Randomizes the lines in the file
        - data_randomizer   : Randomizes the data in the file
        - random_line_delete: Deletes random lines from the file
        - find              : Finds files from directory using fuzzy match
        - string_match      : Finds string OR text from passed list

See https://github.com/xames3/charlotte for cloning the repository.
"""
from sys import exc_info

from charlotte.utils.assists.inquiry import confirm
from charlotte.utils.paths.directories import ai_dir
from charlotte.utils.paths.files import ai_file


def make_dir(dir_name: str, need_init: bool = True) -> None:
    """
    Definition
    ----------
        Creates a directory if it doesn`t exists.
        The function also adds the `__init__.py` file if chosen.

    Parameters
    ----------
        dir_name : string, mandatory
            Name of the directory to be created.

        need_init : boolean, optional
            If chosen as True, it will create `__init__.py` in the directory.
            Global default: True

    Notes
    -----
        If the directory exists, it will ignore and resume with rest of code
        execution.
    """
    from os import makedirs
    from os.path import exists, join

    try:
        if not exists(dir_name):
            makedirs(dir_name)
            if need_init is True:
                init = open(join(dir_name, ai_file['init']), 'a+')
                init.close()
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def timestamp(timestamp_format: str) -> str:
    """
    Definition
    ----------
        Returns timestamp in desired format.

    Parameter
    ---------
        timestamp_format : string, mandatory
            Timestamp that you need to display the time into

    Returns
    -------
        timestamp : string, default
            Returns the timestamp as string in desired format.

    Notes
    -----
        Timestamp formats
        -----------------
            - %d.%m.%Y                  : 31.05.2019
            - %I:%M:%S %p               : 01:23:45 AM
            - %H:%M:%S                  : 01:23:45
            - %d.%m.%Y %I:%M:%S %p      : 31.05.2019 01:23:45 AM
            - %d_%m_%Y_%I_%M_%S_%p      : 31_05_2019_01_23_45_AM
            - %d.%m.%Y %H:%M:%S         : 31.05.2019 01:23:45
            - %d_%m_%Y_%H_%M_%S         : 31_05_2019_01_23_45
    """
    from datetime import datetime

    try:
        return str(datetime.now().strftime(timestamp_format))
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def plain(text: str) -> str:
    """
    Definition
    ----------
        Escapes the ANSI sequence.

    Parameter
    ---------
        text : string, mandatory
            String from which ANSI sequence needs to be stripped out.

    Returns
    -------
        ansi_escape.sub('', message) : string, default
            String without ANSI characters
    """
    from re import compile

    try:
        ansi_escape = compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def make_log(file: str, show_tf_warnings: bool = None) -> classmethod:
    """
    Definition
    ----------
        Creates log file.

    Parameters
    ----------
        file : string, mandatory
            Name of the current file. Using `__file__` is advisable.

        show_tf_warnings : boolean, optional
            If chosen as True, it will show the TensorFlow warnings while
            operating.
            Global default: False

    Returns
    -------
        log : class object, default
            Returns `log` object.
            The output log file is created with current file name under ./logs
            directory with chosen timestamp.

    Notes
    -----
        The log suppresses TensorFlow warnings with `TF_CPP_MIN_LOG_LEVEL`
        metrics. It is totally optional and you can choose to display it on
        console if needed.
    """
    from logging import DEBUG, FileHandler, Formatter, getLogger, StreamHandler
    from os.path import join, basename
    from sys import stdout

    try:
        make_dir(ai_dir['logs'], need_init=False)

        log = getLogger(file)
        log.setLevel(DEBUG)
        log_file = basename(str(file).lower()).split('.py')[0]
        log_time = TIMESTAMP['datetime_12_hrs_log']
        log_name = f'{log_file}_{timestamp(log_time)}.log'

        log_formatter = Formatter(fmt=f'%(asctime)s.%(msecs)06d    %(levelname)'
                                  '-8s    %(filename)s:%(lineno)-4s '
                                  '   %(message)-8s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

        file_handler = FileHandler(join(ai_dir['logs'], log_name))
        file_handler.setFormatter(log_formatter)
        log.addHandler(file_handler)

        stream_handler = StreamHandler(stdout)
        stream_handler.setFormatter(log_formatter)
        log.addHandler(stream_handler)

        if show_tf_warnings is None:
            import os
            import tensorflow.python.util.deprecation as deprecation

            deprecation._PRINT_DEPRECATION_WARNINGS = False
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

        return log

    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def display(message: str) -> None:
    """
    Definition
    ----------
        Prints statements with `?` prefix.

    Parameter
    ---------
        message : string, mandatory
            Message that needs to be printed out.
    """
    print(f'? {message}')


def quit() -> None:
    """
    Definition
    ----------
        Asks for user`s permission before quitting the program.

    Notes
    -----
        Terminates the program.
    """
    from sys import exit

    option = confirm('Are you sure you want to leave?')
    if option is True:
        exit()


def csv_writer(file: str, *args) -> None:
    """
    Definition
    ----------
        Creates and writes to CSV files.

    Parameters
    ----------
        file : string, mandatory
            Path to the CSV file.

        *args : default, mandatory
            Elements to be added to the CSV file.
    """
    from csv import QUOTE_MINIMAL, writer

    try:
        with open(file, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = writer(csv_file, delimiter=',', quoting=QUOTE_MINIMAL)
            csv_writer.writerow([*args])
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def csv_extractor(from_file: str, to_file: str, column: str) -> None:
    """
    Definition
    ----------
        Extracts the particular column from CSV file and saves it in another
        file.

    Parameters
    ----------
        from_file : string, mandatory
            File name from which the data needs to be read.

        to_file : string, mandatory
            File name to which the sorted data needs to be written.

        column : string, mandatory
            Column name to be extracted.

    Notes
    -----
        This function is primarily used for extracting specific column from
        CSV file (this is needed for creating lookup tables).
    """
    from csv import DictReader

    try:
        with open(from_file, 'r', encoding='utf-8', errors='ignore') as source_file:
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
            csv_writer(to_file, line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def line_sorter(file: str) -> None:
    """
    Definition
    ----------
        Sorts the lines alphabetically in the file and saves it.

    Parameters
    ----------
        file : string, mandatory
            File whose data needs to be sorted.
    """
    try:
        with open(file, encoding='utf-8') as source_file:
            new_list = list(set(source_file.readlines()))
            new_list.sort()
            source_file.close()

        with open(file, 'w', encoding='utf-8') as source_file:
            for line in new_list:
                source_file.write(line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def line_randomizer(file: str) -> None:
    """
    Definition
    ----------
        Randomizes the lines in the file and saves it.

    Parameters
    ----------
        file : string, mandatory
            File whose lines need to be randomized.

    Notes
    -----
        The function is used for making dataset little random.
    """
    from random import shuffle

    try:
        with open(file, 'r', encoding='utf-8') as source_file:
            new_list = list(set(source_file.readlines()))
            shuffle(new_list)
            source_file.close()

        with open(file, 'w', encoding='utf-8') as source_file:
            for line in new_list:
                source_file.write(line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def data_randomizer(file: str,
                    find_words: list,
                    replace_words: list) -> None:
    """
    Definition
    ----------
        Randomly replaces the given words in the file with other word and
        saves it.

    Parameters
    ----------
        file : string, mandatory
            File from which the words needs to be replaced.

        find_words : list, mandatory
            List of words to be replaced from the opened file.

        replace_words : list, mandatory
            List of the words to be replaced with in the opened file.

    Notes
    -----
        Use this to replace the common words OR patterns in your dataset.
    """
    from random import choice

    try:
        with open(file, 'r', encoding='utf-8') as source_file:
            lines = source_file.readlines()
            source_file.close()

        with open(file, 'w', encoding='utf-8') as source_file:
            for line in range(len(lines)):
                if any(word in lines[line] for word in find_words):
                    replaced_line = lines[line].replace(
                        choice(find_words), choice(replace_words))
                    source_file.write(replaced_line)
                else:
                    source_file.write(lines[line])
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def random_line_delete(file: str, lines_to_retain: int = 1000) -> None:
    """
    Definition
    ----------
        Randomly deletes lines from the file and saves it.

    Parameters
    ----------
        file : string, mandatory
            File from which the lines are to be deleted.

        lines_to_retain : integer, optional
            Number of lines to keep in the file.
            Global default: 1000

    Notes
    -----
        Use this for shrinking the dataset.
    """
    from random import choices, shuffle

    try:
        with open(file, 'r', encoding='utf-8') as source_file:
            new_list = list(set(source_file.readlines()))
            shuffle(new_list)
            source_file.close()

        with open(file, 'w', encoding='utf-8') as source_file:
            if int(lines_to_retain) is None:
                shrunked_list = choices(new_list, k=1000)
            else:
                shrunked_list = choices(new_list, k=int(lines_to_retain))
            for line in shrunked_list:
                source_file.write(line)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def find(file: str, file_dir: str, min_score: int = 65) -> tuple:
    """
    Definition
    ----------
        Finds the matching file in the directory.

    Parameters
    ----------
        file : string, mandatory
            Approximate name of the file you need to search in the directory.

        file_dir : string, mandatory
            Directory in which the file exists or needs to be searched in.

        min_score : integer, optional
            Minimum score/Threshold score that should match while making as
            approximate guess.
            Global default: 65

    Returns
    -------
        best_guess[0], current_score : tuple, default
            Returns correctly guessed file name with matching score.

    Notes
    -----
        This function uses Fuzzy Logic for determining the best possible match.
        Function can provide 3 best possible matches but we use just 1 i.e.
        `The best match`.
    """
    from os import walk
    from fuzzywuzzy import fuzz
    from fuzzywuzzy.process import extract

    try:
        for root, _, files in walk(file_dir):
            guessed_files = extract(
                file, files, limit=3, scorer=fuzz.partial_ratio)
            no_match_score = 0
            no_match_found = f'Sorry, I could\'nt find \'{file}\' in the directory.'
            for best_guess in guessed_files:
                current_score = fuzz.partial_ratio(file, best_guess)
                if current_score > min_score and current_score > no_match_score:
                    return best_guess[0], current_score
                else:
                    return no_match_found, no_match_score
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')


def string_match(text: str, text_list: list, min_score: int = 65) -> str:
    """
    Definition
    ----------
        Finds the matching string in the list.

    Parameters
    ----------
        text : string, mandatory
            Approximate text that you need to find from the list.

        text_list : list, mandatory
            List in which the text exists or needs to be searched in.

        min_score : integer, optional
            Minimum score/Threshold score that should match while making as
            approximate guess.
            Global default: 65

    Returns
    -------
        best_guess[0] : string, default
            Returns correctly guessed text.

    Notes
    -----
        This function is similar to `find` function but `find` needs to be
        used for searching file from directory while `string_match` can be
        used for guessing `text` from any valid list (For e.g. CSV columns).
    """
    from os import walk
    from fuzzywuzzy import fuzz
    from fuzzywuzzy.process import extract

    try:
        if text is not None:
            guessed = extract(text, text_list, limit=3,
                              scorer=fuzz.partial_ratio)
            no_match_score = 0
            no_match_found = f'Sorry, I could\'nt find a match for \'{text}\'.'
            for best_guess in guessed:
                current_score = fuzz.partial_ratio(text, best_guess)
                if current_score > min_score and current_score > no_match_score:
                    return best_guess[0]
                else:
                    return no_match_found
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} on line {exc_info()[-1].tb_lineno}.')
