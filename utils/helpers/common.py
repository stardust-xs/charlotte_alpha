"""
Charlotte Common Functions
==========================

This module provides references to most common functions that are used in the
package.
The module has 9 functions:
    - make_dir          : Makes a directory
    - json_print        : Prints JSON data in readable fashion
    - model_check       : Checks if the model exists in that directory
    - display           : Prints statements with `?` prefix
    - quit              : Exits the program
    - line_randomizer   : Randomizes the lines in the file
    - csv_writer        : Creates CSV files and adds data to it
    - csv_extractor     : Extracts columns from csv file
    - lookup_sorter     : Sorts the lines alphabetically in the file

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

    try:
        if indentation is None:
            print(dumps(json_data, indent=2))
        else:
            print(dumps(json_data, indent=indentation))
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


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

    try:
        for root, _, files in walk(model_dir):
            for file in files:
                if file.startswith(str(model).lower()) and file.endswith('tar.gz'):
                    return join(root, file)
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


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

    try:
        with open(from_file, 'r') as source_file:
            source = [(random(), line) for line in source_file]
            source.sort()
            source_file.close()
        with open(to_file, 'w') as target_file:
            for _, line in source:
                target_file.write(line)
                target_file.close()
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')


def csv_writer(file: str, *args) -> None:
    """
    Definition
    ----------
        Creates and writes CSV files.

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
              f' {error}.')


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
              f' {error}.')


def lookup_sorter(from_file: str, to_file: str) -> None:
    """
    Definition
    ----------
        Sorts the lines alphabetically in the file and saves it in another
        file.

    Parameters
    ----------
        from_file : string, mandatory
            File name from which the data needs to be read.

        to_file : string, mandatory
            File name to which the sorted data needs to be written.
    """
    try:
        with open(from_file) as source_file:
            lines = source_file.readlines()
            lines.sort()
            for line in range(len(lines)):
                with open(to_file, 'a') as target_file:
                    target_file.write(lines[line])
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error}.')
