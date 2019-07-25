"""
Charlotte Common Functions
==========================

This module provides references to most common functions that are used in the
package.
The module has 6 functions:
    - make_dir          : Makes a directory
    - json_print        : Prints JSON data in readable fashion
    - model_check       : Checks if the model exists in that directory
    - display           : Prints statements with `?` prefix
    - quit              : Exits the program
    - line_randomizer   : Randomizes the lines in the file

See https://github.com/xames3/charlotte for cloning the repository.
"""
from charlotte.utils.helpers.questions import confirm
from charlotte.utils.paths.directories import ai_dir
from charlotte.utils.paths.files import ai_file


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
                init = open(join(dir_name, ai_file['init']), 'a+')
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


def model_check(model: str, model_dir: str = ai_dir['models']) -> None:
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
        Randomizes the lines in the file and saves it in another file.

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
