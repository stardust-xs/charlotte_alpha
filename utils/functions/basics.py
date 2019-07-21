"""
Charlotte`s basic functions
===========================

It contains most generic functions that the AI would use.

See https://github.com/xames3/charlotte for complete documentation.
"""
from . questions import confirm
from .. fluids.constants import TIMESTAMP
from .. fluids.paths import DIR, FILE


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
    """
    from datetime import datetime

    return str(datetime.now().strftime(timestamp_format))


def make_dir(dir_name: str, need_init: bool = True) -> None:
    """
    Definition
    ----------
        Creates a directory if it doesn`t exists.
        The function also adds the `__init__.py` file during if chosen.

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
    import errno
    from os import makedirs
    from os.path import exists, join

    try:
        if not exists(dir_name):
            makedirs(dir_name)
            if need_init is True:
                init = open(join(dir_name, FILE['init']), 'a+')
                init.close()
    except OSError as error:
        if error.errno != errno.EEXIST:
            raise


def json_print(json_data: str, indentation: int = None) -> None:
    """
    Definition
    ----------
        Prints data in readable fashion.
        The data that needs to be printed should be in JSON format.

    Parameters
    ----------
        json_data : string, mandatory
            The data which would be parsed by the Rasa Interpreter after
            performing intent classification.

        indentation : integer, optional
            It adds the indentation to the printed JSON data.
            Global default: 2

    Notes
    -----
        Using this function for printing is totally optional.
        You can possibly get away with normal print function but you won't get
        any indentations. You can use pprint() as well. Works the same.
    """
    from json import dumps

    if indentation is None:
        print(dumps(json_data, indent=2))
    else:
        print(dumps(json_data, indent=indentation))


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

    ansi_escape = compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


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

    make_dir(DIR['logs'], need_init=False)

    log = getLogger(file).setLevel(DEBUG)
    log_file = basename(str(file).lower()).split('.py')[0]
    log_time = TIMESTAMP['datetime_12_hrs_log']
    log_name = f'{log_file}_{timestamp(log_time)}.log'

    log_formatter = Formatter(
        fmt=f'%(asctime)s.%(msecs)06d    %(levelname)-8s    %(filename)s:%(lineno)-4s    %(message)-8s', datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = FileHandler(join(DIR['logs'], log_name))
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


def model_check(model: str, model_dir: str = DIR['models']) -> None:
    """
    Definition
    ----------
        Checks if the model (`model`.tar.gz) exists in the ./models/ directory.

    Parameters
    ----------
        model : string, mandatory
            Name of the model that needs to be checked.

        model_dir : string, optional
            Path of the models directory
            Global default: ./models/

    Returns
    -------
        join(root, file) : None, default
            Name of the model in the set `model_dir` directory.
    """
    from os import walk
    from os.path import join

    for root, _, files in walk(model_dir):
        for file in files:
            if file.startswith(str(model).lower()) and file.endswith('tar.gz'):
                return join(root, file)


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


def line_randomizer(from_file: str, to_file: str) -> None:
    """
    Definition
    ----------

    Parameters
    ----------
        from_file : string, mandatory
            File name from which the data needs to be read.

        to_file : string, mandatory
            File name to which the randomized data needs to be written.

    Notes
    -----
        The function can be used for creating random dataset.
    """
    from random import random

    with open(from_file, 'r') as lines:
        source = [(random(), line) for line in lines]
    source.sort()
    with open(to_file, 'w') as target:
        for _, line in source:
            target.write(line)
