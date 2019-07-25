"""
Charlotte Logging Module
========================

This module builds logs.
All the logs are stored in `./logs/` directory with the timestamp.

See https://github.com/xames3/charlotte for cloning the repository.
"""
from charlotte.utils.globals.constants import TIMESTAMP
from charlotte.utils.helpers.common import make_dir
from charlotte.utils.paths.directories import ai_dir


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

    make_dir(ai_dir['logs'], need_init=False)

    log = getLogger(file).setLevel(DEBUG)
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
